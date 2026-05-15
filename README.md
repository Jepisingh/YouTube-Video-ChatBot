# 🎥 YouTube Video ChatBot

An AI-powered YouTube chatbot built with Streamlit, LangChain, OpenAI, and FAISS.

Users can paste any YouTube video URL and chat with the video using AI.

---

# 🚀 Features

* 🔗 Paste any YouTube video URL
* 📝 Extracts video transcript automatically
* 🤖 Chat with the video using OpenAI GPT
* ⚡ Fast semantic search using FAISS
* 💬 Beautiful Streamlit chat interface
* 🌐 Deployable on Streamlit Cloud

---

# 🛠️ Tech Stack

* Python
* Streamlit
* LangChain
* OpenAI API
* FAISS Vector Database
* YouTube Transcript API

---

# 📂 Project Structure

```bash
youtube-chatbot/

│── frontend.py
│── backend.py
│── requirements.txt
│── README.md
│── .gitignore
```

---

# ⚙️ Installation

## 1. Clone Repository

```bash
git clone [https://github.com/your-username/youtube-chatbot.git](https://github.com/Jepisingh/YouTube-Video-ChatBot)

cd youtube-chatbot
```

---

## 2. Create Virtual Environment

### Windows

```bash
python -m venv myvenv

myvenv\Scripts\activate
```

### Mac/Linux

```bash
python3 -m venv myvenv

source myvenv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Setup OpenAI API Key

Create a `.env` file:

```env
OPENAI_API_KEY=your_openai_api_key
```

---

# ▶️ Run Application

```bash
streamlit run frontend.py
```

---

# ☁️ Streamlit Deployment

1. Push project to GitHub
2. Open Streamlit Cloud
3. Create New App
4. Select:

   * Repository
   * Branch
   * Main File → `frontend.py`

---

# 🔐 Add Secrets in Streamlit Cloud

Go to:

```bash
Settings → Secrets
```

Add:

```toml
OPENAI_API_KEY="your_openai_api_key"
```

---

# 📸 Demo

* Paste YouTube URL
* Process Video
* Ask questions from the video

Example Questions:

* Summarize the video
* What is the main topic?
* Explain the video simply
* What are the key points?

---

# 👨‍💻 Author

Developed by Your Name
