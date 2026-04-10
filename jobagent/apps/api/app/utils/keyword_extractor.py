import re
from typing import List


def extract_keywords(text: str) -> List[str]:
    """
    Very simple keyword extractor for demo purposes.
    In production, use spaCy or a proper NLP model.
    """
    if not text:
        return []
    
    # Just a simple regex to pull out words, then filter by our common dict
    words = re.findall(r'\b[A-Za-z0-9+#]+\b', text)
    words = [w.lower() for w in words if len(w) > 2]
    
    found = []
    for hw in COMMON_JOB_KEYWORDS.all_keywords():
        if hw.lower() in text.lower():
            found.append(hw)
            
    # Deduplicate while preserving order
    return list(dict.fromkeys(found))


class COMMON_JOB_KEYWORDS:
    TECH = [
        "Python", "JavaScript", "TypeScript", "Java", "C++", "C#", "Go", "Rust", "Swift", "Kotlin",
        "React", "Angular", "Vue.js", "Node.js", "Next.js", "Django", "Flask", "FastAPI", "Spring Boot",
        "AWS", "GCP", "Azure", "Docker", "Kubernetes", "CI/CD", "Git", "Linux", "SQL", "PostgreSQL",
        "MongoDB", "Redis", "Kafka", "Elasticsearch", "GraphQL", "REST API", "Microservices",
        "Machine Learning", "AI", "Data Science", "TensorFlow", "PyTorch", "LLMs", "NLP"
    ]
    
    SOFT = [
        "Leadership", "Communication", "Problem Solving", "Teamwork", "Agile", "Scrum",
        "Project Management", "Time Management", "Critical Thinking", "Adaptability"
    ]

    @classmethod
    def all_keywords(cls) -> List[str]:
        return cls.TECH + cls.SOFT

    @classmethod
    def get_for_roles(cls, target_roles: List[str]) -> List[str]:
        """Mock function returning relevant keywords based on target roles."""
        role_str = " ".join(target_roles).lower()
        keywords = []
        if "frontend" in role_str or "ui" in role_str or "react" in role_str:
            keywords.extend(["JavaScript", "TypeScript", "React", "Next.js", "HTML", "CSS", "UI/UX", "REST API"])
        if "backend" in role_str or "server" in role_str or "python" in role_str or "java" in role_str:
            keywords.extend(["Python", "Java", "Go", "PostgreSQL", "MongoDB", "Redis", "Docker", "Kubernetes", "Microservices", "REST API"])
        if "data" in role_str or "machine learning" in role_str or "ai" in role_str:
            keywords.extend(["Python", "SQL", "Machine Learning", "Data Science", "TensorFlow", "PyTorch", "LLMs", "AWS", "GCP"])
        
        # If no specific match, return a general set
        if not keywords:
            keywords = ["Python", "JavaScript", "SQL", "Git", "Agile", "REST API", "Docker", "AWS"]
            
        return list(dict.fromkeys(keywords))
