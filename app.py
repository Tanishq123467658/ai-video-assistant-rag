# app.py
import streamlit as st
from dotenv import load_dotenv
from utils.audio_processor import process_input
from core.transcriber import transcribe_all
from core.summarize import summarize, generate_title
from core.extractor import (
    extract_action_items,
    extract_key_decisions,
    extract_questions,
)
from core.rag_engine import build_rag_chain, ask_question

load_dotenv()

# ---------- Page Config ----------
st.set_page_config(
    page_title="AI Video Assistant",
    page_icon="🎥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Custom CSS ----------
st.markdown(
    """
    <style>
        .main-header {
            text-align: center;
            padding: 1rem 0;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 10px;
            margin-bottom: 2rem;
        }
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }
        .stTabs [data-baseweb="tab"] {
            border-radius: 8px;
            padding: 10px 20px;
            background-color: #f0f2f6;
        }
        .stTabs [aria-selected="true"] {
            background-color: #667eea;
            color: white;
        }
        .chat-user {
            background-color: #e3f2fd;
            padding: 10px 15px;
            border-radius: 12px;
            margin: 5px 0;
        }
        .chat-bot {
            background-color: #f3e5f5;
            padding: 10px 15px;
            border-radius: 12px;
            margin: 5px 0;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- Session State Init ----------
if "result" not in st.session_state:
    st.session_state.result = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "processing" not in st.session_state:
    st.session_state.processing = False


# ---------- Pipeline Function ----------
def run_pipeline(source: str, language: str, progress_callback=None) -> dict:
    steps = [
        ("Processing input (downloading / chunking audio)", 0.15),
        ("Transcribing audio", 0.40),
        ("Generating title", 0.55),
        ("Summarizing transcript", 0.70),
        ("Extracting action items", 0.80),
        ("Extracting key decisions", 0.87),
        ("Extracting open questions", 0.93),
        ("Building RAG chain", 1.0),
    ]

    if progress_callback:
        progress_callback(steps[0][1], steps[0][0])
    chunks = process_input(source)

    if progress_callback:
        progress_callback(steps[1][1], steps[1][0])
    transcript = transcribe_all(chunks, language)

    if progress_callback:
        progress_callback(steps[2][1], steps[2][0])
    title = generate_title(transcript)

    if progress_callback:
        progress_callback(steps[3][1], steps[3][0])
    summary = summarize(transcript)

    if progress_callback:
        progress_callback(steps[4][1], steps[4][0])
    action_items = extract_action_items(transcript)

    if progress_callback:
        progress_callback(steps[5][1], steps[5][0])
    decisions = extract_key_decisions(transcript)

    if progress_callback:
        progress_callback(steps[6][1], steps[6][0])
    questions = extract_questions(transcript)

    if progress_callback:
        progress_callback(steps[7][1], steps[7][0])
    rag_chain = build_rag_chain(transcript)

    return {
        "title": title,
        "transcript": transcript,
        "summary": summary,
        "action_items": action_items,
        "key_decisions": decisions,
        "open_questions": questions,
        "rag_chain": rag_chain,
    }


# ---------- Header ----------
st.markdown(
    """
    <div class="main-header">
        <h1>🎥 AI Video Assistant</h1>
        <p>Transcribe • Summarize • Extract Insights • Chat with your meetings</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------- Sidebar ----------
with st.sidebar:
    st.header("⚙️ Configuration")

    input_mode = st.radio(
        "Input source",
        ["YouTube URL", "Upload File"],
        help="Choose between a YouTube link or upload a local audio/video file.",
    )

    source = None
    if input_mode == "YouTube URL":
        source = st.text_input(
            "🔗 YouTube URL",
            placeholder="https://www.youtube.com/watch?v=...",
        )
    else:
        uploaded_file = st.file_uploader(
            "📁 Upload audio/video file",
            type=["mp3", "mp4", "wav", "m4a", "mkv", "webm", "mov"],
        )
        if uploaded_file is not None:
            import tempfile, os

            suffix = os.path.splitext(uploaded_file.name)[1]
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                tmp.write(uploaded_file.getbuffer())
                source = tmp.name
            st.success(f"✅ Uploaded: {uploaded_file.name}")

    language = st.selectbox(
        "🌐 Language",
        ["english", "hinglish"],
        help="Select the language spoken in the audio.",
    )

    st.markdown("---")
    process_btn = st.button(
        "🚀 Process",
        type="primary",
        use_container_width=True,
        disabled=st.session_state.processing or not source,
    )

    if st.session_state.result is not None:
        if st.button("🔄 Reset / New Analysis", use_container_width=True):
            st.session_state.result = None
            st.session_state.chat_history = []
            st.rerun()

    st.markdown("---")
    st.caption("💡 Tip: Larger files take longer to transcribe.")


# ---------- Processing ----------
if process_btn and source:
    st.session_state.processing = True
    st.session_state.chat_history = []

    progress_bar = st.progress(0.0, text="Starting…")
    status_text = st.empty()

    def update_progress(pct, msg):
        progress_bar.progress(pct, text=msg)
        status_text.info(f"⏳ {msg}")

    try:
        with st.spinner("Working on your file…"):
            st.session_state.result = run_pipeline(source, language, update_progress)
        progress_bar.progress(1.0, text="Done!")
        status_text.success("✅ Processing complete!")
    except Exception as e:
        status_text.error(f"❌ Error: {e}")
        st.exception(e)
    finally:
        st.session_state.processing = False


# ---------- Results ----------
if st.session_state.result:
    result = st.session_state.result

    st.markdown(f"## 📌 {result['title']}")
    st.markdown("---")

    tab_summary, tab_actions, tab_decisions, tab_questions, tab_transcript, tab_chat = (
        st.tabs(
            [
                "📋 Summary",
                "✅ Action Items",
                "🔑 Key Decisions",
                "❓ Open Questions",
                "📝 Transcript",
                "💬 Chat",
            ]
        )
    )

    with tab_summary:
        st.subheader("Summary")
        st.write(result["summary"])
        st.download_button(
            "⬇️ Download Summary",
            result["summary"],
            file_name="summary.txt",
            mime="text/plain",
        )

    with tab_actions:
        st.subheader("Action Items")
        st.write(result["action_items"])

    with tab_decisions:
        st.subheader("Key Decisions")
        st.write(result["key_decisions"])

    with tab_questions:
        st.subheader("Open Questions")
        st.write(result["open_questions"])

    with tab_transcript:
        st.subheader("Full Transcript")
        with st.expander("Preview (first 500 characters)", expanded=True):
            st.write(
                result["transcript"][:500]
                + ("…" if len(result["transcript"]) > 500 else "")
            )
        with st.expander("Show full transcript"):
            st.text_area(
                "Transcript",
                result["transcript"],
                height=400,
                label_visibility="collapsed",
            )
        st.download_button(
            "⬇️ Download Transcript",
            result["transcript"],
            file_name="transcript.txt",
            mime="text/plain",
        )

    with tab_chat:
        st.subheader("💬 Chat with your meeting")
        st.caption("Ask any question about the content. Powered by RAG.")

        # Display chat history
        chat_container = st.container()
        with chat_container:
            for msg in st.session_state.chat_history:
                with st.chat_message(msg["role"]):
                    st.write(msg["content"])

        # Chat input
        if user_question := st.chat_input("Ask something about the meeting…"):
            st.session_state.chat_history.append(
                {"role": "user", "content": user_question}
            )
            with st.chat_message("user"):
                st.write(user_question)

            with st.chat_message("assistant"):
                with st.spinner("Thinking…"):
                    try:
                        answer = ask_question(result["rag_chain"], user_question)
                    except Exception as e:
                        answer = f"⚠️ Error: {e}"
                    st.write(answer)
            st.session_state.chat_history.append(
                {"role": "assistant", "content": answer}
            )

        if st.session_state.chat_history:
            if st.button("🗑️ Clear chat"):
                st.session_state.chat_history = []
                st.rerun()

else:
    # Landing / empty state
    st.info(
        "👈 Configure your input in the sidebar and click **Process** to get started."
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("### 🎬 Step 1")
        st.write("Paste a YouTube URL **or** upload an audio/video file.")
    with col2:
        st.markdown("### 🧠 Step 2")
        st.write("AI transcribes, summarizes, and extracts insights automatically.")
    with col3:
        st.markdown("### 💬 Step 3")
        st.write("Chat with your content using natural language questions.")
