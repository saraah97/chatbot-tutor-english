import streamlit as st
from utils.ui_components import inject_custom_css, render_sidebar
from utils.gemini_client import send_single_prompt, MissingAPIKeyError
from utils.prompt_templates import VOCAB_SYSTEM_PROMPT

# Page Config
st.set_page_config(
    page_title="Vocabulary Helper",
    page_icon="📚",
    layout="wide"
)

# Inject CSS and Render Sidebar
inject_custom_css()
render_sidebar()

# Page Header
st.markdown('<div class="main-header">📚 Vocabulary Helper</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Perluas kosa kata Bahasa Inggris Anda lengkap dengan terjemahan, kelas kata, sinonim, antonim, dan contoh kalimat</div>', unsafe_allow_html=True)

# Initialize Session History for Vocab
if "vocab_history" not in st.session_state:
    st.session_state.vocab_history = []

# Layout split
col_input, col_result = st.columns([1, 1])

with col_input:
    st.markdown("### 🔍 Cari Kata / Frasa")
    word_input = st.text_input(
        "Masukkan kata atau frasa Bahasa Inggris:",
        placeholder="Contoh: Resilience, Break a leg, Serendipity...",
        help="Anda bisa memasukkan satu kata tunggal atau idiom bahasa Inggris."
    )
    
    col_btn_1, col_btn_2 = st.columns([1, 1])
    with col_btn_1:
        submit_button = st.button("🔎 Temukan Makna", use_container_width=True)
    with col_btn_2:
        clear_button = st.button("🧹 Bersihkan Riwayat", use_container_width=True)
        
    if clear_button:
        st.session_state.vocab_history = []
        st.success("Riwayat pencarian berhasil dibersihkan!")
        st.rerun()

with col_result:
    st.markdown("### 📖 Detail Kosakata")
    
    if submit_button:
        if not word_input.strip():
            st.warning("⚠️ Silakan masukkan kata atau frasa terlebih dahulu.")
        else:
            api_key_override = st.session_state.get("api_key_override")
            selected_model = st.session_state.get("selected_model")
            
            with st.spinner(f"📖 Sedang mencari penjelasan untuk '{word_input}'..."):
                try:
                    result = send_single_prompt(
                        prompt=f"Define the word or phrase: '{word_input}'",
                        system_instruction=VOCAB_SYSTEM_PROMPT,
                        api_key_override=api_key_override,
                        model_override=selected_model
                    )
                    
                    # Store in history
                    st.session_state.vocab_history.insert(0, {
                        "word": word_input,
                        "details": result
                    })
                except MissingAPIKeyError:
                    st.error("🔑 API Key tidak ditemukan. Silakan masukkan API Key Google Gemini Anda di sidebar sebelah kiri.")
                except ValueError as ve:
                    st.error(f"⚠️ {str(ve)}")
                except Exception as e:
                    st.error(f"❌ Terjadi kesalahan saat menghubungi server AI: {str(e)}")
                    st.info("Tips: Pastikan koneksi internet Anda stabil dan API Key yang dimasukkan sudah benar.")

    # Display the most recent word search
    if st.session_state.vocab_history:
        latest = st.session_state.vocab_history[0]
        st.markdown('<div class="premium-box">', unsafe_allow_html=True)
        st.markdown(f"### 🔤 Word: `{latest['word']}`")
        st.markdown("---")
        st.markdown(latest['details'])
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("💡 Penjelasan kosa kata akan tampil di sini setelah Anda mengklik tombol 'Temukan Makna'.")

# History Expanders (below)
if len(st.session_state.vocab_history) > 1:
    st.markdown("---")
    st.markdown("### ⏳ Riwayat Kosa Kata")
    
    for idx, item in enumerate(st.session_state.vocab_history[1:]):
        with st.expander(f"Kosa Kata #{len(st.session_state.vocab_history) - idx - 1}: {item['word']}"):
            st.markdown(item['details'])
