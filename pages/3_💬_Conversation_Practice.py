import streamlit as st
from utils.ui_components import inject_custom_css, render_sidebar
from utils.gemini_client import send_chat_message, MissingAPIKeyError
from utils.prompt_templates import CONVERSATION_SYSTEM_PROMPT

# Page Config
st.set_page_config(
    page_title="Conversation Practice",
    page_icon="💬",
    layout="wide"
)

# Inject CSS and Render Sidebar
inject_custom_css()
render_sidebar()

# Page Header
st.markdown('<div class="main-header">💬 Conversation Practice</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Berlatih percakapan bahasa Inggris secara santai dan interaktif bersama Alex, tutor Native Speaker AI</div>', unsafe_allow_html=True)

# Initialize Chat Messages in Session State
INITIAL_GREETING = "Hello! I'm Alex, your English conversation partner. How are you doing today? We can talk about your hobbies, work, plans for the weekend, or anything you'd like to practice!"

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = [
        {"role": "assistant", "content": INITIAL_GREETING}
    ]

# Sidebar helper to clear/reset chat
col_reset, col_space = st.columns([1, 4])
with col_reset:
    if st.button("🧹 Reset Chat", use_container_width=True):
        st.session_state.chat_messages = [
            {"role": "assistant", "content": INITIAL_GREETING}
        ]
        st.success("Percakapan diatur ulang!")
        st.rerun()

# Display Chat History
st.markdown('<div class="premium-box" style="min-height: 400px; padding: 1.5rem; margin-top: 1rem;">', unsafe_allow_html=True)

for message in st.session_state.chat_messages:
    role = message["role"]
    avatar = "🧑‍💻" if role == "user" else "👱‍♂️"
    with st.chat_message(role, avatar=avatar):
        st.markdown(message["content"])

st.markdown('</div>', unsafe_allow_html=True)

# User Chat Input
if user_prompt := st.chat_input("Tulis balasan Anda di sini... (contoh: I am doing fine, thank you! How about you?)"):
    # Add User Message to History & Display Immediately
    st.session_state.chat_messages.append({"role": "user", "content": user_prompt})
    st.rerun()  # Rerun to render the user's message immediately and let the script run again to process AI response

# Process the response if the last message is from the user
if st.session_state.chat_messages[-1]["role"] == "user":
    user_prompt = st.session_state.chat_messages[-1]["content"]
    
    # Prepare history for Gemini API
    history_payload = []
    # Loop through history excluding the very last user message (which we will pass as the prompt)
    for msg in st.session_state.chat_messages[:-1]:
        role = "user" if msg["role"] == "user" else "model"
        history_payload.append({
            "role": role,
            "parts": [msg["content"]]
        })
    
    # Get configuration overrides
    api_key_override = st.session_state.get("api_key_override")
    selected_model = st.session_state.get("selected_model")
    
    # Generate Response
    avatar = "👱‍♂️"
    with st.chat_message("assistant", avatar=avatar):
        message_placeholder = st.empty()
        with st.spinner("Alex sedang mengetik..."):
            try:
                response_text, _ = send_chat_message(
                    prompt=user_prompt,
                    history=history_payload,
                    system_instruction=CONVERSATION_SYSTEM_PROMPT,
                    api_key_override=api_key_override,
                    model_override=selected_model
                )
                
                # Render response
                message_placeholder.markdown(response_text)
                # Save to history
                st.session_state.chat_messages.append({"role": "assistant", "content": response_text})
                
            except MissingAPIKeyError:
                st.error("🔑 API Key tidak ditemukan. Silakan masukkan API Key Google Gemini Anda di sidebar sebelah kiri.")
                # Remove user's last message so they can retry after entering key
                st.session_state.chat_messages.pop()
            except ValueError as ve:
                st.error(f"⚠️ {str(ve)}")
                st.session_state.chat_messages.pop()
            except Exception as e:
                st.error(f"❌ Terjadi kesalahan: {str(e)}")
                st.info("Pastikan API Key Anda sudah diaktifkan di sidebar.")
                st.session_state.chat_messages.pop()
                
    # Force another rerun to keep the layout in sync
    st.rerun()
