from typing import List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Application Configuration Management.
    """
    GROQ_API_KEY: str
    TAVILY_API_KEY: str
    
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Enterprise RAG Copilot"
    
    # These are the MODELS (Llama 3) running on the PLATFORM (Groq)
    ALLOWED_MODEL_NAMES: List[str] = [
        "llama3-70b-8192",
        "llama-3.3-70b-versatile"
    ]

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()