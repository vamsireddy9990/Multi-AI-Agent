from dotenv import load_dotenv
import os
# FIX: Import 'List' for type hinting
from typing import List 

load_dotenv()

class Settings:
    """
    Application configuration settings, using environment variables 
    loaded from a .env file.
    """
    # API Keys
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY")
    TAVILY_API_KEY: str = os.getenv("TAVILY_API_KEY")

    # Allowed Model Names
    ALLOWED_MODEL_NAMES: List[str] = [
        # Production Models (More Stable)
        "llama-3.1-8b-instant",
        "llama-3.3-70b-versatile",
        "mixtral-8x7b-32768",
        "openai/gpt-oss-20b",
        
        # Preview Models (Potentially More Capable, but Less Stable)
        "meta-llama/llama-4-maverick-17b-128e-instruct",
        "meta-llama/llama-4-scout-17b-16e-instruct",
        "moonshotai/kimi-k2-instruct-0905",
        "qwen/qwen3-32b",
    ]
    
settings=Settings()
