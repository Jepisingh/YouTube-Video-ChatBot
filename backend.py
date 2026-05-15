# backend.py

from dotenv import load_dotenv
import os
import re

from youtube_transcript_api import YouTubeTranscriptApi
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import (
    RunnableParallel,
    RunnablePassthrough,
    RunnableLambda
)
from langchain_core.output_parsers import StrOutputParser

# ---------------- LOAD ENV ----------------

from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# ---------------- EXTRACT VIDEO ID ----------------

def extract_video_id(url):

    pattern = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"

    match = re.search(pattern, url)

    return match.group(1) if match else None

# ---------------- GET TRANSCRIPT ----------------

def get_transcript_text(video_url):
    video_id = extract_video_id(video_url)
    # TRY NORMAL TRANSCRIPT ----------
    try:
        ytt_api = YouTubeTranscriptApi()
        transcript_list = ytt_api.fetch(video_id)
        transcript_text = " ".join(
            chunk.text for chunk in transcript_list
        )
        return transcript_text

    # FALLBACK USING yt-dlp ----------
    except Exception:
        import yt_dlp
        ydl_opts = {
            "skip_download": True,
            "writesubtitles": True,
            "writeautomaticsub": True,
            "subtitleslangs": ["en"],
            "quiet": True
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            subtitles = info.get("automatic_captions")
            if not subtitles:
                raise Exception("No transcript available for this video.")
        return (
            "Transcript could not be fetched directly, "
            "but video metadata was loaded."
        )

# ---------------- CREATE CHUNKS ----------------

def create_chunks(transcript_text):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,
        chunk_overlap=300
    )

    chunks = splitter.create_documents([transcript_text])

    return chunks

# ---------------- CREATE VECTOR STORE ----------------

def create_vector_store(chunks):

    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small"
    )

    vector_store = FAISS.from_documents(
        chunks,
        embeddings
    )

    return vector_store

# ---------------- CREATE RAG CHAIN ----------------

def create_chain(vector_store):

    retriever = vector_store.as_retriever(
        search_kwargs={"k": 8}
    )

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.3
    )

    prompt = PromptTemplate(
        template="""
You are a helpful YouTube video assistant.

Answer the user's question ONLY from the transcript context.

Transcript Context:
{context}

Question:
{question}

Answer:
""",
        input_variables=["context", "question"]
    )

    def format_docs(docs):

        return "\n\n".join(
            doc.page_content for doc in docs
        )

    parallel_chain = RunnableParallel({

        "context": retriever | RunnableLambda(format_docs),

        "question": RunnablePassthrough()

    })

    parser = StrOutputParser()

    main_chain = (
        parallel_chain
        | prompt
        | llm
        | parser
    )

    return main_chain

# ---------------- MAIN FUNCTION ----------------

def build_chatbot(video_url):

    transcript_text = get_transcript_text(video_url)

    chunks = create_chunks(transcript_text)

    vector_store = create_vector_store(chunks)

    chain = create_chain(vector_store)

    return chain
