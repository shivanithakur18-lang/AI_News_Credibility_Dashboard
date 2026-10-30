import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

def _ensure_nltk_resources():
    """Download small NLTK resources on first use when internet is available."""
    resources = [
        ("tokenizers/punkt", "punkt"),
        ("corpora/stopwords", "stopwords"),
        ("corpora/wordnet", "wordnet"),
        ("corpora/omw-1.4", "omw-1.4"),
    ]
    for path, package in resources:
        try:
            nltk.data.find(path)
        except LookupError:
            try:
                nltk.download(package, quiet=True)
            except Exception:
                pass

def preprocess_text(text):
    """Lowercase, remove URLs/numbers/punctuation, tokenize, remove stop words, and lemmatize."""
    _ensure_nltk_resources()
    cleaned = (text or "").lower()
    cleaned = re.sub(r"https?://\S+|www\.\S+", " ", cleaned)
    cleaned = re.sub(r"\d+", " ", cleaned)
    cleaned = re.sub(r"[^\w\s]", " ", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()

    try:
        tokens = word_tokenize(cleaned)
    except LookupError:
        tokens = cleaned.split()

    try:
        stop_words = set(stopwords.words("english"))
    except LookupError:
        stop_words = set()

    lemmatizer = WordNetLemmatizer()
    result = []
    for token in tokens:
        if token.isalpha() and token not in stop_words:
            try:
                token = lemmatizer.lemmatize(token)
            except LookupError:
                pass
            result.append(token)
    return " ".join(result)
