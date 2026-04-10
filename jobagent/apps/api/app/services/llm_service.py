"""
LLM Service — returns a configured LangChain LLM based on settings.
"""
from app.core.config import settings
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI


def get_llm():
    if settings.LLM_PROVIDER == "gemini":
        return ChatGoogleGenerativeAI(
            model=settings.LLM_MODEL or "gemini-1.5-pro",
            google_api_key=settings.GOOGLE_API_KEY,
            temperature=0.3,
        )
    # Default: OpenAI
    return ChatOpenAI(
        model=settings.LLM_MODEL or "gpt-4o-mini",
        api_key=settings.OPENAI_API_KEY,
        temperature=0.3,
    )
