# 🎓 AI English Tutor Chatbot

Aplikasi web bimbingan belajar (tutor) Bahasa Inggris berbasis kecerdasan buatan (AI) yang dirancang menggunakan **Python**, **Streamlit**, dan **Google Gemini API**. Aplikasi ini dibuat untuk mempermudah pemula dan pelajar tingkat menengah mempelajari tata bahasa (grammar), memperluas kosakata (vocabulary), berlatih percakapan santai, dan menguji pemahaman lewat kuis interaktif.

Aplikasi ini juga dirancang sebagai media pembelajaran konsep dasar kecerdasan buatan seperti **Natural Language Processing (NLP)**, **Large Language Models (LLM)**, dan **Prompt Engineering**.

---

## 🌟 Fitur Utama

Aplikasi ini memiliki 4 fitur pembelajaran interaktif:

1. **📝 Grammar Correction**: Tulis kalimat bahasa Inggris Anda, lalu AI akan menganalisis kesalahan grammar, menampilkan kalimat yang benar secara visual, memberikan penjelasan dalam Bahasa Indonesia, serta memberikan label tingkat kesulitan kalimat (Beginner/Intermediate/Advanced).
2. **📚 Vocabulary Helper**: Cari arti kata atau frasa bahasa Inggris untuk mendapatkan terjemahan bahasa Indonesia, kelas kata (noun/verb/adjective/dll.), penjelasan makna bahasa Inggris yang sederhana, sinonim, antonim, dan contoh penggunaan kalimat.
3. **💬 Conversation Practice**: Latihan percakapan santai dua arah bersama **Alex**, asisten AI native speaker bahasa Inggris yang ramah. Alex akan secara otomatis memberikan catatan perbaikan grammar (jika ada) di akhir pesannya secara halus, serta tips kosakata periodik.
4. **🧩 Quiz Basic English**: Latih pemahaman Anda melalui kuis Pilihan Ganda (MCQ) atau Isian Kalimat Rumpang (Fill in the Blank) yang di-generate secara dinamis sesuai tingkat kesulitan yang dipilih. Dilengkapi dengan sistem skoring serta pembahasan rinci.

---

## 🛠️ Tech Stack & Versi

- **Python** (>= 3.10)
- **Streamlit** (untuk UI Web Interaktif & Ringan)
- **google-generativeai** (Google Gemini API Client Library)

---

## 🚀 Panduan Setup & Menjalankan Aplikasi Secara Lokal

Ikuti langkah-langkah berikut untuk menjalankan aplikasi di komputer Anda:

### 1. Clone Repositori
```bash
git clone <url-repositori-anda>
cd chatbot-tutor
```

### 2. Buat & Aktifkan Virtual Environment (Direkomendasikan)
Di Windows (PowerShell):
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Di macOS / Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependensi
```bash
pip install -r requirements.txt
```

### 4. Konfigurasi API Key
Aplikasi memerlukan API Key dari Google Gemini. Anda bisa mendapatkan API Key secara gratis di [Google AI Studio](https://aistudio.google.com/).

1. Buat folder `.streamlit` di direktori root jika belum ada.
2. Buat file `.streamlit/secrets.toml` di dalam folder tersebut.
3. Isi file dengan baris berikut (ganti dengan API Key Anda):
   ```toml
   GEMINI_API_KEY = "MASUKKAN_GEMINI_API_KEY_ANDA"
   GEMINI_MODEL = "gemini-1.5-flash"
   ```
*(Catatan: `.streamlit/secrets.toml` telah ditambahkan di `.gitignore` agar tidak terunggah secara tidak sengaja ke Git publik).*

**Alternatif**: Jika Anda tidak memasukkan API Key di file `secrets.toml`, aplikasi menyediakan kolom input API Key di sidebar kiri secara dinamis, sehingga Anda bisa memasukkannya langsung dari browser secara aman.

### 5. Jalankan Aplikasi
```bash
streamlit run app.py
```
Aplikasi akan secara otomatis terbuka di peramban (browser) Anda pada alamat: `http://localhost:8501`.

---

## 🗂️ Struktur Proyek

```
chatbot-tutor/
│
├── .streamlit/
│   └── secrets.toml          # Konfigurasi API Key lokal (diabaikan oleh git)
│
├── pages/
│   ├── 1_📝_Grammar_Correction.py    # Modul Koreksi Grammar
│   ├── 2_📚_Vocabulary.py            # Modul Kamus & Kosa Kata
│   ├── 3_💬_Conversation_Practice.py  # Modul Latihan Percakapan
│   └── 4_🧩_Quiz.py                  # Modul Kuis Dinamis
│
├── utils/
│   ├── __init__.py
│   ├── gemini_client.py       # Wrapper koneksi API Gemini
│   ├── prompt_templates.py    # Template System Prompt & Prompt Engineering
│   └── ui_components.py       # Styling CSS kustom & Render Sidebar bersama
│
├── app.py                     # Halaman Beranda Utama
├── requirements.txt           # File daftar library dependensi
├── .gitignore                 # Daftar file yang diabaikan git
└── README.md                  # Dokumentasi proyek (file ini)
```

---

## ⚙️ Cara Mengubah Model AI

Jika Anda ingin mengganti model AI yang digunakan (misalnya menggunakan model pro `gemini-1.5-pro` atau versi terbaru `gemini-2.5-flash`), Anda dapat melakukannya dengan dua cara:
1. Memilih model langsung melalui menu dropdown di **Sidebar Kiri** aplikasi saat runtime.
2. Mengubah nilai parameter `GEMINI_MODEL` di file `.streamlit/secrets.toml`.

---

## 🛡️ Keamanan & Kepatuhan
- Tidak ada API Key yang ditulis secara hardcode di dalam kode.
- Semua data masukan pengguna diproses langsung secara terenkripsi ke API resmi Google Gemini.
- File konfigurasi lokal `.streamlit/secrets.toml` telah diabaikan melalui `.gitignore` demi keamanan kredensial.

---

## 🌐 Panduan Deploy ke Streamlit Cloud

Anda dapat meng-onlinekan aplikasi ini agar bisa diakses oleh publik/klien secara gratis dengan mengikuti panduan berikut:

### 1. Upload ke GitHub
1. Buat sebuah repository baru di akun GitHub Anda (misalnya: `chatbot-tutor`).
2. Jalankan perintah git untuk meng-upload kode lokal Anda:
   ```bash
   git init
   git add .
   git commit -m "initial commit"
   git branch -M main
   git remote add origin <url-repository-github-anda>
   git push -u origin main
   ```
*(Catatan: Direktori `venv` dan file `.streamlit/secrets.toml` tidak akan terunggah karena sudah diatur secara aman dalam `.gitignore`).*

### 2. Hubungkan ke Streamlit Cloud
1. Kunjungi [share.streamlit.io](https://share.streamlit.io/) dan login menggunakan akun GitHub Anda.
2. Klik tombol **"New app"** di kanan atas dasbor.
3. Masukkan informasi berikut pada form yang tersedia:
   - **Repository**: Nama repositori Anda (contoh: `username/chatbot-tutor`).
   - **Branch**: `main`
   - **Main file path**: `app.py`

### 3. Konfigurasi Secrets API Key
1. Klik tombol **"Advanced settings..."** di samping tombol Deploy.
2. Pada bagian **Secrets**, tempelkan konfigurasi API Key Anda seperti format berikut:
   ```toml
   GEMINI_API_KEY = "MASUKKAN_GEMINI_API_KEY_ANDA_DI_SINI"
   GEMINI_MODEL = "gemini-2.5-flash"
   ```
3. Klik **Save**.
4. Klik **Deploy** dan tunggu proses instalasi dependensi selama 1-2 menit. Aplikasi Anda sekarang sudah online secara publik!

