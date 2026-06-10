import os
import google.generativeai as genai
import streamlit as st

class MissingAPIKeyError(Exception):
    """Exception raised when the Gemini API key is missing."""
    pass

def get_api_key(api_key_override: str = None) -> str:
    """
    Resolve the Gemini API key.
    Checks:
    1. api_key_override (passed from UI input)
    2. st.secrets["GEMINI_API_KEY"]
    3. os.environ.get("GEMINI_API_KEY")
    """
    if api_key_override and api_key_override.strip():
        return api_key_override.strip()
    
    # Try st.secrets
    try:
        if "GEMINI_API_KEY" in st.secrets:
            return st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass
    
    # Try environment variable
    env_key = os.environ.get("GEMINI_API_KEY")
    if env_key:
        return env_key
        
    raise MissingAPIKeyError("Gemini API Key tidak ditemukan. Silakan isi di sidebar atau secrets.toml.")

def get_model_name(model_override: str = None) -> str:
    """
    Resolve the Gemini Model name.
    Checks:
    1. model_override (passed from UI input)
    2. st.secrets["GEMINI_MODEL"]
    3. Default to "gemini-2.5-flash"
    """
    if model_override and model_override.strip():
        return model_override.strip()
        
    try:
        if "GEMINI_MODEL" in st.secrets:
            return st.secrets["GEMINI_MODEL"]
    except Exception:
        pass
        
    return "gemini-2.5-flash"

def get_gemini_model(system_instruction: str = "", api_key_override: str = None, model_override: str = None):
    """
    Initialize and return the GenerativeModel.
    """
    api_key = get_api_key(api_key_override)
    model_name = get_model_name(model_override)
    
    genai.configure(api_key=api_key)
    
    # In older versions, system_instruction is passed to GenerativeModel.
    # We pass it if it's provided.
    if system_instruction:
        model = genai.GenerativeModel(
            model_name=model_name,
            system_instruction=system_instruction
        )
    else:
        model = genai.GenerativeModel(
            model_name=model_name
        )
    return model

def send_single_prompt(prompt: str, system_instruction: str = "", api_key_override: str = None, model_override: str = None) -> str:
    """
    Send a single prompt to Gemini and return the text response.
    Suitable for Grammar Correction, Vocabulary, and Quiz generation.
    """
    try:
        model = get_gemini_model(
            system_instruction=system_instruction,
            api_key_override=api_key_override,
            model_override=model_override
        )
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        # Re-raise API key issues specifically or general exceptions
        if "API_KEY_INVALID" in str(e) or "API key not valid" in str(e):
            raise ValueError("API Key Gemini tidak valid. Silakan periksa kembali API Key Anda.")
        raise e

def send_chat_message(prompt: str, history: list, system_instruction: str = "", api_key_override: str = None, model_override: str = None) -> tuple[str, list]:
    """
    Send a message in a chat session with history and return (response_text, updated_history).
    """
    try:
        model = get_gemini_model(
            system_instruction=system_instruction,
            api_key_override=api_key_override,
            model_override=model_override
        )
        
        # Format history to match Gemini API structure
        # history is expected to be list of dicts: {"role": "user"|"model", "parts": [str]}
        formatted_history = []
        for msg in history:
            role = "user" if msg["role"] == "user" else "model"
            # In case parts is already a list, use it; otherwise wrap it in a list
            parts = msg["parts"] if isinstance(msg.get("parts"), list) else [msg.get("content", "")]
            formatted_history.append({"role": role, "parts": parts})
            
        chat = model.start_chat(history=formatted_history)
        response = chat.send_message(prompt)
        
        # Get updated history from chat session
        updated_history = []
        for content in chat.history:
            role = "user" if content.role == "user" else "model"
            parts = [part.text for part in content.parts]
            updated_history.append({"role": role, "parts": parts, "content": parts[0] if parts else ""})
            
        return response.text, updated_history
    except Exception as e:
        if "API_KEY_INVALID" in str(e) or "API key not valid" in str(e):
            raise ValueError("API Key Gemini tidak valid. Silakan periksa kembali API Key Anda.")
        raise e
