import streamlit as st
import requests
# Import specific exception for connection handling
from requests.exceptions import ConnectionError 

from app.config.settings import settings
from app.common.logger import get_logger
from app.common.custom_exception import CustomException

logger = get_logger(__name__)

st.set_page_config(page_title="Multi AI Agent" , layout="centered")
st.title("Vamsi's Multi AI Agent")

# Ensure initial Streamlit execution does not cause errors
if 'response_text' not in st.session_state:
    st.session_state.response_text = ""
if 'error_message' not in st.session_state:
    st.session_state.error_message = ""

system_prompt = st.text_area("Define your AI Agent: " , height=70, key="system_prompt_input")
selected_model = st.selectbox("Select your AI model: ", settings.ALLOWED_MODEL_NAMES, key="model_select")

allow_web_search = st.checkbox("Allow web search", key="search_check")

user_query = st.text_area("Enter your query : " , height=150, key="query_input")

API_URL = "http://127.0.0.1:9999/chat"

if st.button("Ask Agent") and user_query.strip():
    # Clear previous state
    st.session_state.response_text = ""
    st.session_state.error_message = ""
    
    payload = {
        "model_name" : selected_model,
        "system_prompt" : system_prompt,
        "messages" : [user_query],
        "allow_search" : allow_web_search
    }

    try:
        logger.info("Sending request to backend")

        response = requests.post(API_URL , json=payload)

        if response.status_code == 200:
            agent_response = response.json().get("response","")
            logger.info("Successfully received response from backend")
            st.session_state.response_text = agent_response

        else:
            # Handle 4xx or 5xx HTTP errors received from the backend
            error_detail = response.json().get("detail", f"HTTP Status {response.status_code}")
            logger.error(f"Backend HTTP error: {error_detail}")
            st.session_state.error_message = f"Error from backend: {error_detail}"
            
    # Catch specific connection failure if the server is down
    except ConnectionError:
        error_message = f"Failed to connect to the backend server at {API_URL}. Ensure uvicorn is running."
        logger.error(error_message)
        st.session_state.error_message = error_message
        
    # Catch all other exceptions (e.g., JSON parsing error if response is malformed)
    except Exception as e:
        logger.error(f"Unexpected error while sending request to backend: {e}", exc_info=True)
        st.session_state.error_message = str(CustomException("Failed to communicate to backend", error_detail=e))

# Display response or error after the button click logic
if st.session_state.response_text:
    st.subheader("Agent Response")
    # Streamlit automatically handles Markdown, so we don't need to replace '\n' with '<br>'
    st.markdown(st.session_state.response_text) 

if st.session_state.error_message:
    st.error(st.session_state.error_message)
