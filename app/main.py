from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any

from app.core.ai_agent import get_response_from_ai_agents
from app.config.settings import settings
from app.common.logger import get_logger
from app.common.custom_exception import CustomException

logger = get_logger(__name__)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    docs_url="/docs",
    openapi_url="/openapi.json"
)

class RequestState(BaseModel):
    model_name: str
    system_prompt: str
    messages: List[str]
    allow_search: bool

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "enterprise-rag-copilot-backend"}

@app.post(f"{settings.API_V1_STR}/chat")
def chat_endpoint(request: RequestState) -> Dict[str, Any]:
    logger.info(f"Incoming request for model: {request.model_name}")

    if request.model_name not in settings.ALLOWED_MODEL_NAMES:
        raise HTTPException(status_code=400, detail="Invalid model name specified.")
    
    try:
        response_text = get_response_from_ai_agents(
            model_id=request.model_name,
            query=request.messages,
            allow_search=request.allow_search,
            system_prompt=request.system_prompt
        )
        return {"response": response_text}
    
    except Exception as e:
        logger.error(f"Execution failed: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=str(CustomException("Internal Agent Error", error_detail=e))
        )