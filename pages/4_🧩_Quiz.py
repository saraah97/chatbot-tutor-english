import streamlit as st
import json
import re
from utils.ui_components import inject_custom_css, render_sidebar
from utils.gemini_client import send_single_prompt, MissingAPIKeyError
from utils.prompt_templates import get_mcq_quiz_prompt, get_fill_quiz_prompt

# Page Config
st.set_page_config(
    page_title="Basic English Quiz",
    page_icon="🧩",
    layout="wide"
)

# Inject CSS and Render Sidebar
inject_custom_css()
render_sidebar()

# Page Header
st.markdown('<div class="main-header">🧩 English Quiz</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Uji pemahaman bahasa Inggris Anda melalui kuis interaktif yang dihasilkan secara dinamis</div>', unsafe_allow_html=True)

# Helper function to parse JSON safely
def parse_quiz_response(raw_text: str) -> list:
    cleaned = raw_text.strip()
    # Remove markdown code blocks if present
    if cleaned.startswith("```"):
        match = re.search(r"```(?:json)?\s*(.*?)\s*```", cleaned, re.DOTALL)
        if match:
            cleaned = match.group(1).strip()
    
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        # Try finding array pattern using regex if direct JSON loads fails
        match = re.search(r"\[\s*\{.*\}\s*\]", cleaned, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(0))
            except json.JSONDecodeError:
                pass
        return []

# Initialize Quiz States
if "quiz_stage" not in st.session_state:
    st.session_state.quiz_stage = "setup"  # "setup", "playing", "completed"
if "quiz_questions" not in st.session_state:
    st.session_state.quiz_questions = []
if "quiz_current_index" not in st.session_state:
    st.session_state.quiz_current_index = 0
if "quiz_score" not in st.session_state:
    st.session_state.quiz_score = 0
if "quiz_user_answers" not in st.session_state:
    st.session_state.quiz_user_answers = []
if "quiz_answered" not in st.session_state:
    st.session_state.quiz_answered = False

# --- STAGE 1: SETUP ---
if st.session_state.quiz_stage == "setup":
    st.markdown('<div class="premium-box">', unsafe_allow_html=True)
    st.subheader("🛠️ Pengaturan Kuis Baru")
    
    col1, col2 = st.columns(2)
    with col1:
        quiz_type = st.selectbox(
            "Pilih Tipe Soal:",
            options=["mcq", "fill"],
            format_func=lambda x: "Pilihan Ganda (MCQ)" if x == "mcq" else "Isian (Fill in the Blank)"
        )
        level = st.selectbox(
            "Tingkat Kesulitan:",
            options=["beginner", "intermediate", "advanced"],
            format_func=lambda x: x.capitalize()
        )
    with col2:
        num_questions = st.slider(
            "Jumlah Pertanyaan:",
            min_value=3,
            max_value=10,
            value=5,
            step=1
        )
        
    start_btn = st.button("🚀 Buat Kuis Sekarang", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    if start_btn:
        api_key_override = st.session_state.get("api_key_override")
        selected_model = st.session_state.get("selected_model")
        
        # Prepare Prompt
        if quiz_type == "mcq":
            prompt = get_mcq_quiz_prompt(num_questions, level)
        else:
            prompt = get_fill_quiz_prompt(num_questions, level)
            
        with st.spinner("🧙‍♂️ AI sedang meracik kuis untuk Anda..."):
            try:
                raw_response = send_single_prompt(
                    prompt=prompt,
                    api_key_override=api_key_override,
                    model_override=selected_model
                )
                
                questions = parse_quiz_response(raw_response)
                
                if not questions:
                    st.error("⚠️ AI menghasilkan format kuis yang tidak valid. Silakan klik tombol buat kuis sekali lagi.")
                    # Show raw response inside an expander for debugging if needed
                    with st.expander("Detail Log Respon AI"):
                        st.code(raw_response)
                else:
                    st.session_state.quiz_questions = questions
                    st.session_state.quiz_current_index = 0
                    st.session_state.quiz_score = 0
                    st.session_state.quiz_user_answers = []
                    st.session_state.quiz_answered = False
                    st.session_state.quiz_stage = "playing"
                    st.success("Kuis berhasil dibuat!")
                    st.rerun()
            except MissingAPIKeyError:
                st.error("🔑 API Key tidak ditemukan. Silakan masukkan API Key Google Gemini Anda di sidebar sebelah kiri.")
            except ValueError as ve:
                st.error(f"⚠️ {str(ve)}")
            except Exception as e:
                st.error(f"❌ Gagal membuat kuis: {str(e)}")

# --- STAGE 2: PLAYING ---
elif st.session_state.quiz_stage == "playing":
    q_index = st.session_state.quiz_current_index
    questions = st.session_state.quiz_questions
    current_q = questions[q_index]
    total_q = len(questions)
    
    # Progress Info
    st.markdown(f"#### Pertanyaan {q_index + 1} dari {total_q}")
    st.progress((q_index) / total_q)
    
    # Question Card
    st.markdown('<div class="premium-box">', unsafe_allow_html=True)
    st.markdown(f"### `{current_q['question']}`")
    
    # Render based on question type
    if current_q["type"] == "mcq":
        # Options
        options = current_q["options"]
        # Use key with index to ensure uniqueness on reload
        user_answer = st.radio(
            "Pilih jawaban Anda:",
            options=options,
            key=f"q_{q_index}_opt",
            disabled=st.session_state.quiz_answered
        )
    else:
        # Fill in the blank
        if "hint" in current_q and current_q["hint"]:
            st.info(f"💡 **Petunjuk:** {current_q['hint']}")
        user_answer = st.text_input(
            "Masukkan jawaban Anda:",
            placeholder="Ketik jawaban...",
            key=f"q_{q_index}_fill",
            disabled=st.session_state.quiz_answered
        )
        
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Action buttons
    col_submit, col_next = st.columns([1, 1])
    
    with col_submit:
        confirm_btn = st.button(
            "👉 Konfirmasi Jawaban",
            use_container_width=True,
            disabled=st.session_state.quiz_answered or (not current_q["type"] == "mcq" and not user_answer.strip())
        )
        
    if confirm_btn:
        st.session_state.quiz_answered = True
        
        # Check answer
        correct_ans = current_q["answer"]
        
        if current_q["type"] == "mcq":
            is_correct = user_answer.strip().lower() == correct_ans.strip().lower()
        else:
            # Clean answers for fill in the blank
            is_correct = user_answer.strip().lower() == correct_ans.strip().lower()
            
        st.session_state.quiz_user_answers.append({
            "question": current_q["question"],
            "user_answer": user_answer,
            "correct_answer": correct_ans,
            "is_correct": is_correct,
            "explanation": current_q.get("explanation", "")
        })
        
        if is_correct:
            st.session_state.quiz_score += 1
            st.session_state.quiz_correct_feedback = True
        else:
            st.session_state.quiz_correct_feedback = False
            
        st.rerun()

    # If already answered, show the explanation and feedback card
    if st.session_state.quiz_answered:
        feedback = st.session_state.quiz_user_answers[-1]
        
        if feedback["is_correct"]:
            st.success("🎉 **Benar!** Jawaban Anda tepat sekali.")
        else:
            st.error(f"❌ **Kurang tepat.** Jawaban yang benar adalah: **{feedback['correct_answer']}**")
            
        st.markdown('<div class="premium-box">', unsafe_allow_html=True)
        st.markdown(f"**Penjelasan:**\n\n{feedback['explanation']}")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Show Next button
        with col_next:
            if q_index + 1 < total_q:
                next_btn = st.button("Pertanyaan Selanjutnya ➡️", use_container_width=True)
                if next_btn:
                    st.session_state.quiz_current_index += 1
                    st.session_state.quiz_answered = False
                    st.rerun()
            else:
                finish_btn = st.button("🏁 Selesaikan & Lihat Hasil", use_container_width=True)
                if finish_btn:
                    st.session_state.quiz_stage = "completed"
                    st.rerun()

# --- STAGE 3: COMPLETED ---
elif st.session_state.quiz_stage == "completed":
    st.markdown('<div class="premium-box" style="text-align: center; border: 2px solid #10b981;">', unsafe_allow_html=True)
    st.markdown("<h2>🏁 Kuis Selesai!</h2>", unsafe_allow_html=True)
    
    score = st.session_state.quiz_score
    total = len(st.session_state.quiz_questions)
    percentage = int((score / total) * 100)
    
    # Display Circular/Large Score
    st.markdown(f"<h1 style='color:#10b981; font-size: 4.5rem; margin-bottom: 0;'>{percentage}%</h1>", unsafe_allow_html=True)
    st.markdown(f"<h5>Anda menjawab <strong>{score}</strong> dari <strong>{total}</strong> pertanyaan dengan benar.</h5>", unsafe_allow_html=True)
    
    # Descriptive rating
    if percentage >= 90:
        st.balloons()
        st.success("🏆 Excellent! You are mastering English extremely well!")
    elif percentage >= 70:
        st.success("👏 Great job! You have a solid understanding.")
    elif percentage >= 50:
        st.warning("👍 Good try! Keep practicing to improve further.")
    else:
        st.error("📚 Don't give up! Review the grammar notes and try again.")
        
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Review list
    st.markdown("### 📋 Pembahasan Jawaban")
    for idx, f in enumerate(st.session_state.quiz_user_answers):
        status_icon = "✅" if f["is_correct"] else "❌"
        box_border = "border-left: 4px solid #10b981" if f["is_correct"] else "border-left: 4px solid #ef4444"
        
        st.markdown(f"""
        <div class="premium-box" style="{box_border}">
            <strong>Pertanyaan {idx+1}:</strong> {f['question']}<br>
            {status_icon} Jawaban Anda: <code>{f['user_answer']}</code><br>
            🎯 Jawaban Benar: <strong>{f['correct_answer']}</strong><br>
            <p style="margin-top:0.5rem; font-size:0.9rem; color:#cbd5e1;"><em>Penjelasan:</em> {f['explanation']}</p>
        </div>
        """, unsafe_allow_html=True)
        
    # Restart button
    restart_btn = st.button("🔄 Coba Kuis Lain / Buat Kuis Baru", use_container_width=True)
    if restart_btn:
        st.session_state.quiz_stage = "setup"
        st.session_state.quiz_questions = []
        st.session_state.quiz_current_index = 0
        st.session_state.quiz_score = 0
        st.session_state.quiz_user_answers = []
        st.session_state.quiz_answered = False
        st.rerun()
