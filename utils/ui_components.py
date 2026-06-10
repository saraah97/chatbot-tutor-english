import streamlit as st
import os

def inject_custom_css():
    """
    Inject premium custom CSS for styling the application with a modern,
    solid flat, and clean dark look using Google Fonts.
    This styling complies with non-gradient design guidelines.
    """
    st.markdown("""
    <style>
        /* Import Google Font */
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');
        
        /* Apply fonts only to text-based elements, avoiding overriding icon fonts by omitting !important */
        html, body, .stMarkdown, p, h1, h2, h3, h4, h5, h6, label, button, input, textarea, select {
            font-family: 'Outfit', sans-serif;
        }
        
        /* Main background - solid premium dark slate */
        .stApp {
            background-color: #0b0f19;
            color: #f1f5f9;
        }
        
        /* Custom Header Styling (Flat Solid Color) */
        .main-header {
            font-size: 2.8rem;
            font-weight: 700;
            color: #38bdf8;
            text-align: center;
            margin-bottom: 0.5rem;
        }
        
        .sub-header {
            font-size: 1.2rem;
            color: #94a3b8;
            text-align: center;
            margin-bottom: 2rem;
        }
        
        /* Glassmorphic/Modern Feature Cards (Flat Style) */
        .card-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2rem;
        }
        
        .feature-card {
            background-color: #131b2e;
            border: 1px solid #1e293b;
            border-radius: 12px;
            padding: 1.5rem;
            transition: all 0.2s ease;
            cursor: pointer;
            text-align: center;
            color: white !important;
            text-decoration: none !important;
        }
        
        .feature-card:hover {
            background-color: #1e293b;
            border-color: #38bdf8;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        }
        
        .card-icon {
            font-size: 2.5rem;
            margin-bottom: 0.8rem;
            display: inline-block;
        }
        
        .card-title {
            font-size: 1.3rem;
            font-weight: 600;
            color: #38bdf8;
            margin-bottom: 0.5rem;
        }
        
        .card-desc {
            font-size: 0.9rem;
            color: #cbd5e1;
            line-height: 1.4;
        }
        
        /* Streamlit Input fields and textareas flat styles override */
        div[data-baseweb="input"], div[data-baseweb="textarea"] {
            background-color: #131b2e !important;
            border: 1px solid #1e293b !important;
            border-radius: 8px !important;
        }
        
        /* Disable text cursor and keyboard input in selectbox to make it telunjuk-only (pure click) */
        div[data-baseweb="select"] input {
            cursor: pointer !important;
            caret-color: transparent !important;
            pointer-events: none !important;
        }
        
        /* Flat Buttons styling (Solid colors) */
        .stButton>button {
            background-color: #0ea5e9 !important;
            color: white !important;
            border: 1px solid #0ea5e9 !important;
            border-radius: 8px !important;
            padding: 0.6rem 1.8rem !important;
            font-weight: 600 !important;
            transition: all 0.2s ease !important;
            box-shadow: none !important;
        }
        
        .stButton>button:hover {
            background-color: #0284c7 !important;
            border-color: #0284c7 !important;
            transform: none !important;
        }
        
        /* Chat bubble styles customization - force light colored text for readability */
        div[data-testid="stChatMessage"] {
            background-color: #131b2e !important;
            border: 1px solid #1e293b !important;
            border-radius: 12px !important;
            margin-bottom: 0.8rem !important;
        }
        
        div[data-testid="stChatMessage"] p, div[data-testid="stChatMessage"] span, div[data-testid="stChatMessage"] div {
            color: #f1f5f9 !important;
        }
        
        div[data-testid="stChatMessage"] [data-testid="stChatMessageAvatar"] {
            background-color: #1e293b !important;
        }
        
        /* Sidebar container style */
        section[data-testid="stSidebar"] {
            background-color: #090d16 !important;
            border-right: 1px solid #1e293b !important;
        }
        
        /* Flat custom boxes */
        .premium-box {
            background-color: #131b2e;
            border: 1px solid #1e293b;
            border-radius: 12px;
            padding: 1.2rem;
            margin: 1rem 0;
        }
    </style>
    """, unsafe_allow_html=True)


def render_sidebar():
    """
    Renders a consistent sidebar across all pages.
    Manages API Key override, Model Selection, and Educational Section.
    """
    st.sidebar.title("🎓 AI English Tutor")
    st.sidebar.caption("English Learning Assistant Powered by Gemini")
    
    st.sidebar.markdown("---")
    
    # --- Configuration Section ---
    st.sidebar.subheader("⚙️ Konfigurasi Model & API")
    
    # 1. Model Selection
    default_model = "gemini-1.5-flash"
    try:
        if "GEMINI_MODEL" in st.secrets:
            default_model = st.secrets["GEMINI_MODEL"]
    except Exception:
        pass
        
    model_options = [
        "gemini-1.5-flash",
        "gemini-2.5-flash",
        "gemini-1.5-pro",
        "gemini-2.5-pro"
    ]
    if default_model not in model_options:
        model_options.insert(0, default_model)
        
    selected_model = st.sidebar.selectbox(
        "Pilih Model Gemini:",
        options=model_options,
        index=model_options.index(default_model)
    )
    st.session_state["selected_model"] = selected_model
    
    # 2. API Key input
    api_key_placeholder = ""
    api_key_configured = False
    
    try:
        if "GEMINI_API_KEY" in st.secrets and st.secrets["GEMINI_API_KEY"] != "YOUR_GEMINI_API_KEY_HERE":
            api_key_placeholder = "Konfigurasi terdeteksi di secrets.toml"
            api_key_configured = True
    except Exception:
        pass
        
    if os.environ.get("GEMINI_API_KEY"):
        api_key_placeholder = "Konfigurasi terdeteksi di Environment Variable"
        api_key_configured = True
        
    user_api_key = st.sidebar.text_input(
        "Masukkan Gemini API Key:",
        type="password",
        placeholder=api_key_placeholder if api_key_placeholder else "Masukkan API Key...",
        help="Masukkan API key Anda di sini jika belum dikonfigurasi di file secrets.toml. Data ini aman dan hanya disimpan sementara di sesi browser Anda."
    )
    
    if user_api_key.strip():
        st.session_state["api_key_override"] = user_api_key.strip()
    elif api_key_configured:
        # Clear override if set before but now empty, fallback to configured
        if "api_key_override" in st.session_state:
            del st.session_state["api_key_override"]
    else:
        # Warn user if no key is configured anywhere
        st.sidebar.warning("⚠️ API Key tidak terdeteksi. Silakan masukkan API Key Anda di atas untuk mengaktifkan fitur AI.")
        
    st.sidebar.markdown("---")
    
    # --- Educational Concept Section (Client's request) ---
    st.sidebar.subheader("📚 Pojok Edukasi AI")
    with st.sidebar.expander("🤖 Apa itu LLM? (Large Language Models)"):
        st.markdown("""
        **Large Language Models (LLM)** adalah sistem AI yang dilatih menggunakan data teks dalam jumlah sangat besar. 
        - **Contoh**: Google Gemini, ChatGPT.
        - **Kemampuan**: Bisa memahami konteks percakapan, menerjemahkan bahasa, menulis esai, hingga menjelaskan konsep tata bahasa Inggris dengan sangat baik.
        """)
        
    with st.sidebar.expander("🛠️ Prompt Engineering"):
        st.markdown("""
        **Prompt Engineering** adalah teknik merumuskan instruksi tertulis agar AI menghasilkan output yang sesuai keinginan kita.
        - **Pentingnya**: Kualitas jawaban AI ditentukan oleh seberapa spesifik instruksi (prompt) yang diberikan.
        - **Contoh di Aplikasi**: Kami memprogram instruksi khusus di belakang layar seperti *"berperanlah sebagai native speaker ramah bernama Alex"* agar AI merespons dengan gaya percakapan yang mendidik.
        """)
        
    with st.sidebar.expander("🧠 Natural Language Processing (NLP)"):
        st.markdown("""
        **NLP** adalah cabang AI yang mempelajari bagaimana komputer dapat mengerti, mengolah, dan memanipulasi bahasa manusia.
        - **Penerapan**: AI menganalisis tata bahasa (syntax), makna kata (semantics), dan mengoreksi kesalahan ketik/tata bahasa secara langsung (seperti fitur Grammar Correction).
        """)
        
    with st.sidebar.expander("💡 Cara Belajar yang Mudah"):
        st.markdown("""
        1. **Mulai dari Kecil**: Coba tulis kalimat sederhana di *Grammar Correction*.
        2. **Perluas Kosa Kata**: Cari definisi kata baru di *Vocabulary Helper*.
        3. **Praktik Langsung**: Lakukan obrolan santai di *Conversation Practice*.
        4. **Uji Pemahaman**: Latih ingatan lewat *Quiz* harian.
        """)

