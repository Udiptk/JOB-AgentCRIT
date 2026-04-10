from fastapi import FastAPI, Depends, HTTPException, Request, WebSocket, WebSocketDisconnect, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from sqlmodel import Session, select
from sqlalchemy.orm.attributes import flag_modified
from pydantic import BaseModel
from typing import Optional, List
import os, json
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

from app.core.db import init_db, get_session, engine
from app.models.models import UserProfile, JobMatch, ApplicationHistory
from app.agents.orchestrator import orchestrator
import asyncio

# ──────────────────────────────────────────
# Auth helpers
# ──────────────────────────────────────────
from jose import JWTError, jwt
from passlib.context import CryptContext

SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def create_access_token(data: dict) -> str:
    payload = data.copy()
    payload["exp"] = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> Optional[str]:
    """Returns email from token or None."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None


# ──────────────────────────────────────────
# Request/Response Schemas
# ──────────────────────────────────────────
class RegisterRequest(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


class ProfileUpdateRequest(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    headline: Optional[str] = None
    github_url: Optional[str] = None
    linkedin_url: Optional[str] = None
    skills: Optional[List[str]] = None
    experience: Optional[List[dict]] = None
    projects: Optional[List[dict]] = None
    education: Optional[List[dict]] = None
    github_repos: Optional[List[dict]] = None


class RepoAnalysisRequest(BaseModel):
    repo_links: List[str]
    email: str  # identify user


# ──────────────────────────────────────────
# App
# ──────────────────────────────────────────
app = FastAPI(title="Autonomous Job Application System API")

# In production set ALLOWED_ORIGINS="https://your-frontend.vercel.app"
_raw_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173")
ALLOWED_ORIGINS = [o.strip() for o in _raw_origins.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/api/health")
def health_check():
    return {"status": "ok"}


@app.get("/api/stats")
def get_stats(session: Session = Depends(get_session)):
    """Public endpoint — returns real activity stats for the landing page."""
    from sqlalchemy import func

    total_jobs = session.exec(select(JobMatch)).all()
    total_apps = session.exec(select(ApplicationHistory)).all()

    avg_ats = 0.0
    if total_apps:
        avg_ats = sum(a.ats_score for a in total_apps) / len(total_apps)

    platforms = list({j.platform for j in total_jobs if j.platform})

    return {
        "jobs_scanned": len(total_jobs),
        "applications_submitted": len(total_apps),
        "avg_ats_score": round(avg_ats, 1),
        "platforms_active": len(platforms) if platforms else 0,
        "system_status": "Operational",
    }


# ──────────────────────────────────────────
# AUTH ENDPOINTS
# ──────────────────────────────────────────
@app.post("/auth/register")
def register(req: RegisterRequest, session: Session = Depends(get_session)):
    existing = session.exec(select(UserProfile).where(UserProfile.email == req.email)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered.")

    hashed = hash_password(req.password)
    user = UserProfile(
        name=req.name,
        email=req.email,
        phone=req.phone,
        hashed_password=hashed,
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    token = create_access_token({"sub": user.email})
    return {"token": token, "profile": _profile_to_dict(user)}


@app.post("/auth/login")
def login(req: LoginRequest, session: Session = Depends(get_session)):
    user = session.exec(select(UserProfile).where(UserProfile.email == req.email)).first()
    if not user or not verify_password(req.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password.")

    token = create_access_token({"sub": user.email})
    return {"token": token, "profile": _profile_to_dict(user)}


@app.get("/profile/me")
def get_my_profile(token: str, session: Session = Depends(get_session)):
    email = decode_token(token)
    if not email:
        raise HTTPException(status_code=401, detail="Invalid token.")
    user = session.exec(select(UserProfile).where(UserProfile.email == email)).first()
    if not user:
        raise HTTPException(status_code=404, detail="Profile not found.")
    return _profile_to_dict(user)


@app.put("/profile/me")
def update_my_profile(
    req: ProfileUpdateRequest,
    token: str,
    session: Session = Depends(get_session),
):
    email = decode_token(token)
    if not email:
        raise HTTPException(status_code=401, detail="Invalid token.")
    user = session.exec(select(UserProfile).where(UserProfile.email == email)).first()
    if not user:
        raise HTTPException(status_code=404, detail="Profile not found.")

    if req.name is not None:
        user.name = req.name
    if req.phone is not None:
        user.phone = req.phone
    if req.headline is not None:
        user.headline = req.headline
    if req.github_url is not None:
        user.github_url = req.github_url
    if req.linkedin_url is not None:
        user.linkedin_url = req.linkedin_url
    if req.skills is not None:
        user.skills = list(req.skills)          # copy to force new reference
        flag_modified(user, "skills")
    if req.experience is not None:
        user.experience = list(req.experience)
        flag_modified(user, "experience")
    if req.projects is not None:
        user.projects = list(req.projects)
        flag_modified(user, "projects")
    if req.education is not None:
        user.education = list(req.education)
        flag_modified(user, "education")
    if req.github_repos is not None:
        user.github_repos = list(req.github_repos)
        flag_modified(user, "github_repos")

    user.updated_at = datetime.utcnow()
    session.add(user)
    session.commit()
    session.refresh(user)
    return _profile_to_dict(user)


# ──────────────────────────────────────────
# REPO INTELLIGENCE AGENT (SSE Stream)
# ──────────────────────────────────────────
@app.post("/profile/analyze-repos")
async def analyze_repos(req: RepoAnalysisRequest, session: Session = Depends(get_session)):
    """
    Streams terminal logs + Gemini analysis result for GitHub repo links.
    Returns SSE-compatible text/event-stream.
    """
    from app.agents.repo_agent import stream_repo_analysis

    user = session.exec(select(UserProfile).where(UserProfile.email == req.email)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    async def event_generator():
        async for chunk in stream_repo_analysis(req.repo_links):
            yield f"data: {chunk}\n\n"
            await asyncio.sleep(0)

    return StreamingResponse(event_generator(), media_type="text/event-stream")


# ──────────────────────────────────────────
# LEGACY PROFILE ENDPOINT (backward compat)
# ──────────────────────────────────────────
@app.post("/profile")
def create_profile(profile: UserProfile, session: Session = Depends(get_session)):
    existing = session.exec(select(UserProfile).where(UserProfile.email == profile.email)).first()
    if existing:
        existing.skills = profile.skills
        existing.experience = profile.experience
        existing.projects = profile.projects
        existing.education = profile.education
        session.add(existing)
        profile = existing
    else:
        session.add(profile)
    session.commit()
    session.refresh(profile)
    return profile


async def recalculate_job_queue_scores(profile_id: int):
    with Session(engine) as session:
        user = session.get(UserProfile, profile_id)
        if not user:
            return
        jobs = session.exec(select(JobMatch)).all()
        if not jobs:
            return
        from app.agents.job_finder_agent import rank_job_snippets
        jobs_dict_list = [
            {"title": j.title, "company": j.company, "platform": j.platform, "url": j.url, "snippet": j.description}
            for j in jobs
        ]
        rescored_jobs = await rank_job_snippets(jobs_dict_list, user.dict())
        for scored_job in rescored_jobs:
            db_job = next(
                (j for j in jobs if j.title == scored_job.get("title") and j.company == scored_job.get("company")),
                None,
            )
            if db_job:
                db_job.match_score = scored_job.get("match_score", 0)
                db_job.justification = scored_job.get("justification")
                db_job.key_requirements = scored_job.get("key_requirements", [])
        session.commit()


@app.put("/profile/{profile_id}")
def update_profile(
    profile_id: int,
    profile_data: UserProfile,
    background_tasks: BackgroundTasks,
    session: Session = Depends(get_session),
):
    user = session.get(UserProfile, profile_id)
    if not user:
        raise HTTPException(status_code=404)
    user.projects = profile_data.projects
    user.experience = profile_data.experience
    session.commit()
    session.refresh(user)
    background_tasks.add_task(recalculate_job_queue_scores, user.id)
    return user


# ──────────────────────────────────────────
# JOB / RESUME / APPLY ENDPOINTS
# ──────────────────────────────────────────
@app.get("/fetch-jobs")
async def get_jobs(session: Session = Depends(get_session)):
    from app.agents.job_finder_agent import run_job_finder_agent
    user = session.exec(select(UserProfile)).first()
    if not user:
        raise HTTPException(status_code=404, detail="Complete your profile first before scanning for jobs.")

    # Clear stale job listings + any orphaned application history
    old_jobs = session.exec(select(JobMatch)).all()
    old_job_ids = {j.id for j in old_jobs}
    for j in old_jobs:
        session.delete(j)

    # Delete applications that referenced the now-deleted jobs
    old_apps = session.exec(select(ApplicationHistory)).all()
    for a in old_apps:
        if a.job_id in old_job_ids:
            session.delete(a)

    session.commit()

    # Smart job role — use first skill, headline, or fallback
    profile_dict = _profile_to_dict(user)
    skills = profile_dict.get("skills") or []
    headline = profile_dict.get("headline") or ""

    if skills:
        job_role = skills[0]
    elif headline:
        # Use first 2 words of headline as role (e.g. "ML Engineer at Google" → "ML Engineer")
        job_role = " ".join(headline.split()[:3])
    else:
        job_role = "Software Developer"

    print(f"[fetch-jobs] Searching for: '{job_role}'")
    jobs_data = await run_job_finder_agent(job_role=job_role, user_profile=profile_dict)

    saved_jobs = []
    for job_dict in jobs_data:
        try:
            job = JobMatch(**job_dict)
            session.add(job)
            saved_jobs.append(job)
        except Exception as e:
            print(f"[fetch-jobs] Skipping malformed job: {e}")

    session.commit()
    for j in saved_jobs:
        session.refresh(j)
    return saved_jobs


@app.get("/jobs")
def list_saved_jobs(session: Session = Depends(get_session)):
    """Return all saved jobs from DB, sorted by match_score descending."""
    jobs = session.exec(select(JobMatch).order_by(JobMatch.match_score.desc())).all()
    return jobs


@app.get("/applications")
def list_applications(session: Session = Depends(get_session)):
    """Return application history with enriched job title/company."""
    apps = session.exec(select(ApplicationHistory).order_by(ApplicationHistory.applied_at.desc())).all()
    result = []
    for app in apps:
        job = session.get(JobMatch, app.job_id)
        result.append({
            "id": app.id,
            "job_id": app.job_id,
            "job_title": job.title if job else "Unknown",
            "company": job.company if job else "Unknown",
            "platform": app.platform,
            "status": app.status,
            "ats_score": app.ats_score,
            "applied_at": str(app.applied_at),
        })
    return result


class ResumeRequest(BaseModel):
    job_id: int
    critic_comment: Optional[str] = None


@app.post("/generate-resume")
async def generate_resume(req: ResumeRequest = None, job_id: int = 1, critic_comment: Optional[str] = None, session: Session = Depends(get_session)):
    # Support both body and query param
    if req:
        job_id = req.job_id
        critic_comment = req.critic_comment

    job = session.get(JobMatch, job_id)
    user = session.exec(select(UserProfile)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User profile not found")

    job_target = (
        job.dict()
        if job
        else {"id": job_id, "title": "Target Role", "company": "Target Company", "description": "Target job description."}
    )

    initial_state = {
        "user_profile": user.dict(),
        "selected_job": job_target,
        "jobs": [],
        "resume_md": "",
        "ats_score": 0.0,
        "critic_feedback": critic_comment or "",
        "status": "start",
        "logs": [],
    }
    result = await orchestrator.ainvoke(initial_state)
    return {
        "resume_md": result["resume_md"],
        "ats_score": result["ats_score"],
        "logs": result["logs"],
        "improvements": result.get("improvements", []),
    }



@app.post("/apply")
async def apply_job(job_id: int, session: Session = Depends(get_session)):
    job = session.get(JobMatch, job_id)
    user = session.exec(select(UserProfile)).first()
    if not job or not user:
        raise HTTPException(status_code=404, detail="Job or User not found")

    resume_md = f"# Resume for {user.name}\nApplied for {job.title}"
    history = ApplicationHistory(
        job_id=job.id,
        status="Applied",
        resume_md=resume_md,
        ats_score=90.0,
        platform=job.platform,
    )
    session.add(history)
    session.commit()
    return {"message": "Application submitted", "status": "success"}


@app.websocket("/logs")
async def websocket_logs(websocket: WebSocket):
    from app.utils.log_generator import generate_agent_logs
    await websocket.accept()
    try:
        async for msg in generate_agent_logs():
            await websocket.send_json({"log": msg})
    except WebSocketDisconnect:
        print("Client disconnected")


# ──────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────
def _profile_to_dict(user: UserProfile) -> dict:
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "phone": user.phone,
        "headline": user.headline,
        "github_url": user.github_url,
        "linkedin_url": user.linkedin_url,
        "skills": user.skills,
        "experience": user.experience,
        "projects": user.projects,
        "education": user.education,
        "github_repos": user.github_repos,
        "created_at": str(user.created_at),
        "updated_at": str(user.updated_at),
    }
