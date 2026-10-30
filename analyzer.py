import re
from textblob import TextBlob
from preprocessing import preprocess_text
from summarizer import summarize_text

CLICKBAIT_PHRASES = [
    "you won't believe", "you will not believe", "shocking", "secret revealed",
    "must watch", "breaking", "viral", "unbelievable", "what happens next",
    "doctors hate this", "urgent", "exposed",
]
EXTREME_WORDS = ["always", "never", "everyone", "guaranteed", "miracle"]
MANIPULATIVE_WORDS = ["disaster", "scandal", "outrage", "fear", "panic"]
VAGUE_ATTRIBUTION = ["experts say", "sources reveal", "insiders say", "people are saying"]
SOURCE_TERMS = ["according to", "report", "study", "data"]

def get_sentiment(text):
    """Return the TextBlob polarity and the requested three-class sentiment label."""
    polarity = float(TextBlob(text).sentiment.polarity)
    if polarity > 0.1:
        label = "Positive"
    elif polarity < -0.1:
        label = "Negative"
    else:
        label = "Neutral"
    return label, polarity

def analyze_warning_signals(text):
    """Detect transparent text patterns; these are signals, not proof of misinformation."""
    lower = text.lower()
    warnings = []
    clickbait_hits = [phrase for phrase in CLICKBAIT_PHRASES if phrase in lower]

    exclamation_count = text.count("!")
    if exclamation_count > 3:
        warnings.append(f"Excessive exclamation marks ({exclamation_count}).")

    letters = [ch for ch in text if ch.isalpha()]
    uppercase_count = sum(ch.isupper() for ch in letters)
    uppercase_ratio = uppercase_count / len(letters) if letters else 0
    excessive_uppercase = len(letters) >= 10 and uppercase_ratio >= 0.35
    if excessive_uppercase:
        warnings.append("Excessive uppercase text detected.")

    extreme_hits = sorted(set(word for word in EXTREME_WORDS if re.search(rf"\b{re.escape(word)}\b", lower)))
    manipulative_hits = sorted(set(word for word in MANIPULATIVE_WORDS if re.search(rf"\b{re.escape(word)}\b", lower)))
    if extreme_hits:
        warnings.append("Absolute/extreme wording: " + ", ".join(extreme_hits) + ".")
    if manipulative_hits:
        warnings.append("Emotionally charged wording: " + ", ".join(manipulative_hits) + ".")

    vague_hits = [phrase for phrase in VAGUE_ATTRIBUTION if phrase in lower]
    if vague_hits:
        warnings.append("Vague attribution phrase(s): " + ", ".join(vague_hits) + ".")

    has_source_term = any(term in lower for term in SOURCE_TERMS)
    if not has_source_term:
        warnings.append("No configured source-related phrase was found (for example, 'according to', 'report', 'study', or 'data').")

    if clickbait_hits:
        warnings.append("Clickbait-style phrase(s): " + ", ".join(clickbait_hits) + ".")

    return {
        "warnings": warnings,
        "clickbait_hits": clickbait_hits,
        "exclamation_count": exclamation_count,
        "excessive_uppercase": excessive_uppercase,
        "extreme_hits": extreme_hits,
        "manipulative_hits": manipulative_hits,
        "vague_hits": vague_hits,
        "has_source_term": has_source_term,
        "has_numeric_data": bool(re.search(r"\d", text)),
    }

def calculate_credibility_score(signals):
    """Calculate a bounded heuristic assistance score using the project rubric."""
    score = 100
    if signals["clickbait_hits"]:
        score -= 15
    if signals["exclamation_count"] > 3:
        score -= 10
    if signals["excessive_uppercase"]:
        score -= 10
    score -= 5 * (len(signals["extreme_hits"]) + len(signals["manipulative_hits"]))
    if signals["vague_hits"]:
        score -= 10
    if signals["has_source_term"]:
        score += 5
    if signals["has_numeric_data"]:
        score += 5
    score = max(0, min(100, score))

    if score >= 75:
        category = "Low linguistic risk"
    elif score >= 45:
        category = "Moderate linguistic risk"
    else:
        category = "High linguistic risk"
    return score, category

def analyze_news(text):
    """Run preprocessing, sentiment, warning-signal scoring, and summarization."""
    text = (text or "").strip()
    if not text:
        raise ValueError("Please provide some text to analyze.")

    # Preprocessing output is provided for reproducibility and future extensions.
    processed = preprocess_text(text)
    sentiment, polarity = get_sentiment(text)
    signals = analyze_warning_signals(text)
    score, category = calculate_credibility_score(signals)
    summary = summarize_text(text)

    clickbait_status = "Yes" if signals["clickbait_hits"] else "No configured phrase detected"
    if signals["exclamation_count"] > 3 or signals["excessive_uppercase"]:
        clickbait_status = "Possible attention-seeking formatting detected"

    return {
        "sentiment": sentiment,
        "sentiment_score": polarity,
        "clickbait_status": clickbait_status,
        "warning_signals": signals["warnings"],
        "credibility_score": score,
        "risk_category": category,
        "summary": summary,
        "preprocessed_text": processed,
    }
