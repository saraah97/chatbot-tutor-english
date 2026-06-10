# 📘 PLAN.MD — AI English Tutor Chatbot
> Dokumen perencanaan lengkap untuk Junior Developer / AI Agent

---

## 📋 Ringkasan Proyek

| Item | Detail |
|---|---|
| **Nama Proyek** | AI English Tutor Chatbot |
| **Tujuan** | Website chatbot untuk belajar bahasa Inggris berbasis AI |
| **Tech Stack** | Python, Streamlit, Google Gemini API |
| **Deployment** | Streamlit Cloud (gratis, publik) |
| **Bahasa UI** | Campuran (UI → Bahasa Indonesia, Konten → Bahasa Inggris) |
| **Target Pengguna** | Pelajar bahasa Inggris level pemula hingga menengah |

---

## 🎯 Fitur Utama

| # | Fitur | Deskripsi |
|---|---|---|
| 1 | **Grammar Correction** | User mengirim kalimat bahasa Inggris → AI mengoreksi grammar + penjelasan |
| 2 | **Vocabulary** | User input kata/kalimat → AI jelaskan arti, sinonim, antonim, dan contoh kalimat |
| 3 | **Conversation Practice** | User chat bebas dengan AI yang berperan sebagai native speaker |
| 4 | **Quiz Basic English** | Soal MCQ (pilihan ganda) + Fill in the blank, di-generate oleh AI secara dinamis |

---

## 🗂️ Struktur Folder Proyek

```
english-tutor-chatbot/
│
├── .streamlit/
│   └── secrets.toml          # ⚠️ API Key lokal — JANGAN di-commit ke Git!
│
├── pages/
│   ├── 1_📝_Grammar_Correction.py
│   ├── 2_📚_Vocabulary.py
│   ├── 3_💬_Conversation_Practice.py
│   └── 4_🧩_Quiz.py
│
├── utils/
│   ├── __init__.py
│   ├── gemini_client.py       # Wrapper koneksi ke Gemini API
│   └── prompt_templates.py    # Semua template prompt engineering
│
├── app.py                     # Halaman utama / Home
├── requirements.txt           # Daftar library Python
├── .gitignore                 # Pastikan secrets.toml masuk di sini
└── README.md                  # Dokumentasi singkat untuk publik
```

---

## ⚙️ Tech Stack & Versi

```
Python        >= 3.10
Streamlit     >= 1.35.0
google-generativeai >= 0.7.0
```

**`requirements.txt`** harus berisi:
```
streamlit>=1.35.0
google-generativeai>=0.7.0
```

---

## 🔐 Konfigurasi API Key (PENTING — Baca Dulu!)

> ⚠️ **JANGAN pernah menulis API Key langsung di dalam kode (hardcode).**
> Gunakan sistem secrets di bawah ini.

### Untuk Development Lokal
Buat file `.streamlit/secrets.toml`:
```toml
GEMINI_API_KEY = "masukkan-api-key-kamu-di-sini"
```

### Untuk Streamlit Cloud (Production)
1. Push kode ke GitHub (pastikan `secrets.toml` ada di `.gitignore`)
2. Buka dashboard [share.streamlit.io](https://share.streamlit.io)
3. Masuk ke **Settings → Secrets**
4. Tambahkan:
```
GEMINI_API_KEY = "masukkan-api-key-kamu-di-sini"
```

### Cara Mengakses di Kode Python
```python
import streamlit as st
api_key = st.secrets["GEMINI_API_KEY"]
```

---

## 🧱 Implementasi Per File

### 1. `utils/gemini_client.py`
File ini adalah **wrapper** untuk semua komunikasi dengan Gemini API.

**Yang harus diimplementasikan:**
- Fungsi `get_gemini_model()` → inisialisasi koneksi ke model `gemini-1.5-flash`
- Fungsi `send_message(prompt: str, history: list) -> str` → kirim pesan dan terima balasan
- Fungsi `send_single_prompt(prompt: str) -> str` → untuk quiz dan vocabulary (tidak butuh history)
- Gunakan model: **`gemini-1.5-flash`** (gratis, cepat, cukup untuk use case ini)

**Contoh skeleton:**
```python
import google.generativeai as genai
import streamlit as st

def get_gemini_model(system_instruction: str = ""):
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=system_instruction
    )
    return model

def send_single_prompt(prompt: str, system_instruction: str = "") -> str:
    model = get_gemini_model(system_instruction)
    response = model.generate_content(prompt)
    return response.text
```

---

### 2. `utils/prompt_templates.py`
File ini menyimpan **semua prompt engineering templates**. Ini adalah inti dari skill "Prompt Engineering".

**Empat prompt system yang harus dibuat:**

#### A. Grammar Correction
```
System Prompt:
"You are an expert English grammar teacher. 
When the user sends a sentence:
1. Identify if it has grammar errors
2. Show the corrected sentence (bold the corrections)
3. Explain each correction briefly in Indonesian
4. Give the corrected sentence a difficulty label: Beginner / Intermediate / Advanced
Format your response in a clear, friendly way."
```

#### B. Vocabulary Helper
```
System Prompt:
"You are a helpful English vocabulary tutor.
When the user inputs a word or phrase:
1. Provide the Indonesian translation
2. Explain the meaning in simple English
3. Show the word class (noun/verb/adjective/etc.)
4. Give 2 example sentences using the word
5. List 2 synonyms and 2 antonyms if applicable
Format the output in a structured, easy-to-read layout."
```

#### C. Conversation Practice
```
System Prompt:
"You are a friendly, patient native English speaker.
Your role is to have a natural conversation with an Indonesian learner.
Rules:
- Keep your sentences clear and not too complex
- If the user makes grammar mistakes, gently correct them at the end of your reply
- Keep the conversation engaging and positive
- If user writes in Indonesian, kindly encourage them to try in English
- Add a small vocabulary tip once every 3 messages"
```

#### D. Quiz Generator
```
Prompt Template untuk MCQ:
"Generate {n} multiple-choice English quiz questions for beginner level.
Topics can include: grammar, vocabulary, tenses, prepositions.
Format strictly as JSON:
[
  {
    "type": "mcq",
    "question": "She ___ to school every day.",
    "options": ["go", "goes", "going", "gone"],
    "answer": "goes",
    "explanation": "We use 'goes' because the subject is third person singular (She)."
  }
]
Return ONLY the JSON array. No extra text."

Prompt Template untuk Fill in the Blank:
"Generate {n} fill-in-the-blank English quiz questions for beginner level.
Format strictly as JSON:
[
  {
    "type": "fill",
    "question": "I ___ a student.",
    "answer": "am",
    "hint": "verb to be, first person",
    "explanation": "'Am' is used with 'I' in present tense."
  }
]
Return ONLY the JSON array. No extra text."
```

---

### 3. `app.py` — Halaman Utama
**Yang harus diimplementasikan:**
- Judul: "🎓 AI English Tutor"
- Deskripsi singkat fitur dalam Bahasa Indonesia
- Navigasi ke tiap fitur (Streamlit sudah auto-handle via folder `pages/`)
- Tampilkan 4 kartu fitur sebagai panduan visual

**Layout yang direkomendasikan:**
```
[Header: AI English Tutor - Belajar Bahasa Inggris dengan AI]

Selamat datang! Pilih fitur belajar di sidebar:

[Kartu 1: 📝 Grammar Correction]  [Kartu 2: 📚 Vocabulary]
[Kartu 3: 💬 Conversation]        [Kartu 4: 🧩 Quiz]
```

---

### 4. `pages/1_📝_Grammar_Correction.py`
**Yang harus diimplementasikan:**
- Text area untuk input kalimat user
- Tombol "Koreksi Sekarang"
- Tampilkan hasil koreksi dari AI dalam card/expander
- Simpan riwayat koreksi dalam `st.session_state`

**Flow:**
```
User input kalimat → Klik tombol → Kirim ke Gemini dengan Grammar Prompt
→ Tampilkan hasil (kalimat asli vs kalimat benar + penjelasan)
```

---

### 5. `pages/2_📚_Vocabulary.py`
**Yang harus diimplementasikan:**
- Input field untuk kata/frasa
- Tombol "Cari Arti"
- Tampilkan hasil dalam format terstruktur (definisi, contoh, sinonim)
- Fitur opsional: tombol 🔊 (catatan: TTS tidak native di Streamlit, bisa skip)

**Flow:**
```
User input kata → Klik tombol → Kirim ke Gemini dengan Vocabulary Prompt
→ Tampilkan dalam layout card yang rapi
```

---

### 6. `pages/3_💬_Conversation_Practice.py`
**Yang harus diimplementasikan:**
- Chat interface menggunakan `st.chat_message` dan `st.chat_input`
- Simpan history percakapan di `st.session_state.messages`
- Sertakan system prompt "native English speaker" di setiap sesi
- Tombol "Reset Percakapan" untuk mulai ulang
- Tampilkan indikator typing (opsional: `st.spinner`)

**Penting tentang Chat History:**
```python
# Inisialisasi session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Format history untuk Gemini
history = [
    {"role": msg["role"], "parts": [msg["content"]]}
    for msg in st.session_state.messages
]
```

**Catatan:** Gemini menggunakan role `"user"` dan `"model"` (bukan `"assistant"`).

---

### 7. `pages/4_🧩_Quiz.py`
**Yang harus diimplementasikan:**
- Pilihan mode quiz: MCQ atau Fill in the Blank (atau keduanya)
- Pilihan jumlah soal: 5 / 10 / 15
- Tombol "Generate Soal" → panggil Gemini → parse JSON response
- Tampilkan soal satu per satu
- Tracking skor di `st.session_state`
- Tampilkan hasil akhir + review jawaban

**Flow Lengkap:**
```
User pilih mode & jumlah soal
→ Klik "Generate Soal"
→ Gemini generate soal dalam format JSON
→ Parse JSON → tampilkan soal
→ User jawab → validasi → tampilkan feedback
→ Setelah semua soal → tampilkan skor akhir
```

**Penanganan Error JSON:**
```python
import json, re

def parse_quiz_response(raw_text: str) -> list:
    # Hapus markdown code fence jika ada
    cleaned = re.sub(r"```json|```", "", raw_text).strip()
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        return []  # Fallback: return list kosong, tampilkan pesan error ke user
```

---

## 🚀 Tahapan Pengerjaan (Estimasi 5-7 Hari)

### Fase 1 — Setup Proyek (Hari 1)
- [ ] Buat folder struktur seperti di atas
- [ ] Install dependencies: `pip install streamlit google-generativeai`
- [ ] Buat `.streamlit/secrets.toml` dan isi dengan API Key
- [ ] Buat `.gitignore` (pastikan `secrets.toml` masuk)
- [ ] Test koneksi Gemini API dengan script sederhana
- [ ] Buat `requirements.txt`
- [ ] Push ke GitHub (repo public/private sesuai kebutuhan)

**Test koneksi Gemini (jalankan manual dulu):**
```python
import google.generativeai as genai
genai.configure(api_key="API_KEY_KAMU")
model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content("Say hello in English!")
print(response.text)
```

---

### Fase 2 — Backend / Utils (Hari 2)
- [ ] Implementasi `utils/gemini_client.py`
- [ ] Implementasi semua prompt di `utils/prompt_templates.py`
- [ ] Test setiap fungsi secara manual (bisa pakai file `test_utils.py` sementara)

---

### Fase 3 — Halaman Fitur (Hari 3-4)
- [ ] Buat `app.py` (halaman home)
- [ ] Implementasi `pages/1_📝_Grammar_Correction.py`
- [ ] Implementasi `pages/2_📚_Vocabulary.py`
- [ ] Implementasi `pages/3_💬_Conversation_Practice.py`
- [ ] Implementasi `pages/4_🧩_Quiz.py`
- [ ] Test manual setiap halaman

---

### Fase 4 — UI & Polish (Hari 5)
- [ ] Tambahkan CSS custom via `st.markdown` untuk mempercantik tampilan
- [ ] Pastikan semua label UI dalam Bahasa Indonesia
- [ ] Tambahkan loading spinner di setiap pemanggilan AI
- [ ] Pastikan error handling jika API gagal (try-except di semua API call)
- [ ] Cek responsive tampilan di mobile

**Contoh CSS custom untuk Streamlit:**
```python
st.markdown("""
<style>
    .main { background-color: #f0f4ff; }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)
```

---

### Fase 5 — Deployment ke Streamlit Cloud (Hari 6)
- [ ] Pastikan semua kode sudah di-push ke GitHub
- [ ] Buka [share.streamlit.io](https://share.streamlit.io) → Login dengan GitHub
- [ ] Klik "New app" → pilih repo → pilih `app.py` sebagai entrypoint
- [ ] Masuk ke **Advanced settings → Secrets** → Paste API Key
- [ ] Deploy → tunggu proses build (±3-5 menit)
- [ ] Test semua fitur di URL publik yang diberikan

---

### Fase 6 — Testing & Serah Terima (Hari 7)
- [ ] Test setiap fitur dengan beberapa skenario input
- [ ] Test edge case: input kosong, karakter aneh, kalimat sangat panjang
- [ ] Dokumentasikan URL Streamlit Cloud di README.md
- [ ] Buat README.md yang menjelaskan cara penggunaan

---

## 🛡️ Checklist Keamanan

- [ ] `secrets.toml` ada di `.gitignore`
- [ ] Tidak ada API Key yang hardcode di kode manapun
- [ ] Semua pemanggilan API dibungkus `try-except`
- [ ] Input user di-sanitize (hindari prompt injection: jangan langsung pass input user sebagai system prompt)

---

## ⚠️ Hal yang Perlu Diperhatikan

### Rate Limit Gemini Free Tier
- Gemini 1.5 Flash gratis tier: ~15 request/menit, 1 juta token/hari
- Cukup untuk demo/testing, tapi tambahkan pesan error yang informatif jika kena limit

### Session State di Streamlit
- Setiap refresh halaman = session state reset
- Data percakapan TIDAK persisten antar sesi (ini normal untuk scope proyek ini)
- Jika ingin persisten, butuh database (di luar scope proyek ini)

### Handling Response JSON untuk Quiz
- Gemini kadang menambahkan teks di luar JSON meskipun sudah diminta format JSON
- Selalu gunakan fungsi `parse_quiz_response()` yang sudah include regex cleaning
- Jika parse gagal, tampilkan tombol "Generate Ulang" agar user bisa coba lagi

---

## 📁 File `.gitignore` yang Direkomendasikan

```gitignore
# Secrets
.streamlit/secrets.toml

# Python
__pycache__/
*.py[cod]
*.pyo
.env
venv/
.venv/

# OS
.DS_Store
Thumbs.db
```

---

## 📝 README.md (Untuk Publik)

Isi README.md minimal harus mencakup:
1. Nama & deskripsi proyek
2. Link Streamlit Cloud (setelah deploy)
3. Daftar fitur
4. Screenshot/GIF demo (opsional tapi sangat direkomendasikan)
5. Cara setup lokal (untuk developer lain)

---

## ✅ Definition of Done (Kriteria Selesai)

Proyek dianggap **selesai dan siap diserahkan ke client** jika:

- [ ] Semua 4 fitur dapat diakses dan berjalan di Streamlit Cloud
- [ ] Grammar Correction memberikan koreksi + penjelasan dalam Bahasa Indonesia
- [ ] Vocabulary menampilkan arti, contoh kalimat, dan sinonim/antonim
- [ ] Conversation Practice bisa bercakap-cakap minimal 10 pesan tanpa error
- [ ] Quiz berhasil generate soal MCQ + Fill in the blank dan menampilkan skor
- [ ] Tidak ada API Key yang ter-expose di kode publik
- [ ] Aplikasi bisa diakses melalui URL publik Streamlit Cloud
- [ ] UI menggunakan Bahasa Indonesia untuk navigasi/label, konten tetap English

---

*Dokumen ini dibuat sebagai panduan pengerjaan proyek AI English Tutor Chatbot.*
*Versi: 1.0 | Terakhir diperbarui: Juni 2026*