from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from typing import List
import traceback # Import the traceback module for debugging
from app.core.ai_agent import get_response_from_ai_agents
from app.config.settings import settings
from app.common.logger import get_logger
from app.common.custom_exception import CustomException

logger = get_logger(__name__)

app = FastAPI(title="MULTI AI AGENT")

class RequestState(BaseModel):
    model_name:str
    system_prompt:str
    messages:List[str]
    allow_search: bool

@app.post("/chat")
def chat_endpoint(request:RequestState):
    logger.info(f"Received request for model : {request.model_name}")

    if request.model_name not in settings.ALLOWED_MODEL_NAMES:
        logger.warning("Invalid model name")
        raise HTTPException(status_code=400 , detail="Invalid model name")
    
    try:
        response = get_response_from_ai_agents(
            request.model_name,
            request.messages,
            request.allow_search,
            request.system_prompt
        )

        logger.info(f"Sucesfully got response from AI Agent {request.model_name}")

        return {"response" : response}
    
    except Exception as e:
        # --- MODIFIED ERROR HANDLING FOR DEBUGGING ---
        # 1. Log the error with exc_info=True to print the full traceback via the logger
        logger.error("Some error occurred during response generation. See traceback below.", exc_info=True)
        
        # 2. Print the traceback directly to the console (for quick visibility)
        traceback.print_exc() 
        
        # 3. Raise the HTTP exception for the frontend
        raise HTTPException(
            status_code=500 , 
            detail=str(CustomException("Failed to get AI response" , error_detail=e))
            )
