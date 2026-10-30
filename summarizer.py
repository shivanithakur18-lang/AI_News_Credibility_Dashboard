import streamlit as st

@st.cache_resource(show_spinner=False)
def load_summarizer():
    """Load a free Hugging Face summarization pipeline once per Streamlit session."""
    from transformers import pipeline
    return pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

def summarize_text(text, max_input_chars=5000):
    """Summarize long enough text; gracefully fall back if model loading fails."""
    text = (text or "").strip()
    if not text:
        return "No text was provided for summarization."
    words = text.split()
    if len(words) < 35:
        return text if len(text) <= 500 else text[:497] + "..."

    try:
        summarizer = load_summarizer()
        safe_text = text[:max_input_chars]
        output = summarizer(
            safe_text,
            max_length=min(110, max(35, len(safe_text.split()) // 2)),
            min_length=20,
            do_sample=False,
            truncation=True,
        )
        summary = output[0].get("summary_text", "").strip()
        return summary or text[:500]
    except Exception:
        # The application still works without the optional model or internet access.
        sentences = [part.strip() for part in text.replace("!", ".").replace("?", ".").split(".") if part.strip()]
        if sentences:
            return " ".join(sentences[:2])[:500]
        return text[:500]
