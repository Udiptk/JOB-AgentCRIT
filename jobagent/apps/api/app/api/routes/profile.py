from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.session import get_db
from app.schemas.profile import ProfileCreate, ProfileOut, ProfileUpdate
# from app.repositories.profile_repo import ProfileRepository

router = APIRouter()

@router.get("/{user_id}", response_model=dict)
async def get_profile(user_id: int, db: AsyncSession = Depends(get_db)):
    # Mock for scaffolding
    return {"message": "Profile fetched", "user_id": user_id}

@router.post("/", response_model=dict)
async def create_profile(profile: ProfileCreate, db: AsyncSession = Depends(get_db)):
    return {"message": "Profile created"}

@router.put("/{user_id}", response_model=dict)
async def update_profile(user_id: int, profile: ProfileUpdate, db: AsyncSession = Depends(get_db)):
    return {"message": "Profile updated", "user_id": user_id}
