# AI Video Assistant with RAG

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python)
![LangChain](https://img.shields.io/badge/LangChain-RAG-green?style=for-the-badge)
![Whisper](https://img.shields.io/badge/OpenAI-Whisper-black?style=for-the-badge)
![ChromaDB](https://img.shields.io/badge/VectorDB-ChromaDB-purple?style=for-the-badge)
![Mistral AI](https://img.shields.io/badge/LLM-Mistral-orange?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

AI-powered Video & Meeting Assistant that processes YouTube videos and recorded meetings, transcribes audio using Whisper, translates Hindi/Hinglish to English using Sarvam AI, generates summaries and titles, builds a vector database with ChromaDB, and enables conversational Q&A over transcripts using Retrieval-Augmented Generation (RAG).

---

## Features

- YouTube video audio extraction using `yt-dlp`
- Audio chunking and preprocessing with `pydub`
- Local speech-to-text using OpenAI Whisper
- Hindi/Hinglish → English translation using Sarvam AI
- AI-generated:
  - Meeting summaries
  - Smart titles
  - Key insights
- Retrieval-Augmented Generation (RAG) pipeline using:
  - LangChain
  - ChromaDB
  - HuggingFace embeddings
- Conversational Q&A over video/meeting transcripts
- PDF export support
- Local vector database storage

---

## Tech Stack

- Python
- LangChain
- ChromaDB
- Whisper
- Sarvam AI
- Mistral AI
- HuggingFace Embeddings
- yt-dlp
- PyTorch

---

## Project Structure

```bash
ai-video-assistant-rag/
│
├── core/                 # Core AI pipeline logic
├── utils/                # Audio/video utility functions
├── downloads/            # Downloaded audio files
├── vector_db/            # ChromaDB vector storage
├── main.py               # Main execution pipeline
├── requirements.txt
├── .env
└── README.md
```

---

## How It Works

1. User provides:
   - YouTube video URL
   - or meeting recording

2. Audio is extracted and chunked.

3. Whisper transcribes the audio locally.

4. Sarvam AI translates Hinglish/Hindi content into English.

5. Transcript is:
   - summarized
   - embedded
   - stored in ChromaDB

6. RAG pipeline retrieves relevant chunks and answers user questions contextually.

---

## Installation

Clone the repository:

```bash
git clone https://github.com/Tanishq123467658/ai-video-assistant-rag.git

cd ai-video-assistant-rag
```

Create virtual environment:

```bash
python -m venv .venv
```

Activate virtual environment:

### Windows

```bash
.venv\Scripts\activate
```

### Linux / Mac

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file:

```env
MISTRAL_API_KEY=your_mistral_api_key
SARVAM_API_KEY=your_sarvam_api_key
WHISPER_MODEL=small
SARVAM_STT_MODEL=saaras:v2.5
```

---

## FFmpeg Setup (Windows)

Whisper requires `ffmpeg` and `ffprobe`.

Create a folder:

```bash
binaries/
```

Add:

```bash
ffmpeg.exe
ffprobe.exe
```

Then configure PATH dynamically in code.

---

## Run the Project

```bash
python main.py
```

---

## Example Use Cases

- Meeting assistant
- YouTube video chatbot
- Podcast summarizer
- Lecture notes generator
- AI learning assistant
- Video knowledge retrieval system

---

## Future Improvements

- Speaker diarization
- Multi-video knowledge base
- Timestamp-based retrieval
- Real-time meeting assistant
- Docker deployment
- Authentication system
- Cloud vector database support

---

## References

- LangChain
- ChromaDB
- OpenAI Whisper
- Sarvam AI
- Mistral AI

---

## Author

### Tanishq Battul

- LinkedIn: https://www.linkedin.com/in/tanishq-battul/
- GitHub: https://github.com/Tanishq123467658
