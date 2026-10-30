# AI-Based News Sentiment and Credibility Assistance Dashboard

A beginner-friendly MCA mini project built with Python, Streamlit, SQLite, TextBlob, NLTK, Hugging Face Transformers, Pandas, Plotly, and ReportLab.

## Important disclaimer

> This tool analyzes linguistic and content-based warning signals. It does not independently verify whether a news item is true or false.

The score is a transparent heuristic based on selected text patterns. It is not a fact-checking system or a validated misinformation detector.

## Features

- Positive, Negative, or Neutral sentiment using TextBlob
- Polarity score from -1 to +1
- Clickbait and sensational-language pattern detection
- Heuristic credibility-assistance score from 0 to 100
- Optional Hugging Face summarization with a graceful fallback
- SQLite analysis history with filtering and deletion
- Plotly charts and recent analysis metrics
- Downloadable PDF report

## Requirements

- Python 3.10 or newer recommended
- Internet connection for first-time NLTK resource and Hugging Face model downloads
- A few GB of free disk space may be needed for the summarization model and PyTorch

## Setup

### Windows

1. Extract the project ZIP.
2. Open the project folder in VS Code.
3. Open Terminal > New Terminal.
4. Create a virtual environment:

   ```bash
   py -m venv .venv
   ```

5. Activate it:

   ```bash
   .venv\\Scripts\\activate
   ```

6. Install packages:

   ```bash
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

7. Start the application:

   ```bash
   streamlit run app.py
   ```

8. Streamlit normally opens the browser automatically. If not, open the local URL printed in the terminal, usually `http://localhost:8501`.

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

## First run

- The app creates `news_analysis.db` automatically.
- NLTK may download tokenizer, stop-word, and WordNet resources when needed.
- The summarization model is downloaded on its first use. The first analysis of a long article may be slower.
- If model download/loading fails, the app uses a short extractive fallback and continues working.

## Folder contents

- `app.py`: Streamlit user interface and page navigation
- `analyzer.py`: sentiment, warning signals, and scoring
- `preprocessing.py`: text cleaning, tokenization, stop-word removal, and lemmatization
- `summarizer.py`: Hugging Face summarization and fallback
- `database.py`: SQLite database functions
- `pdf_report.py`: PDF export
- `requirements.txt`: required Python packages
- `news_analysis.db`: created automatically at runtime

## Scoring rules

Starts at 100:
- Any configured clickbait phrase: -15
- More than three exclamation marks: -10
- Excessive uppercase letters: -10
- Each distinct extreme/manipulative word: -5
- Vague attribution phrase: -10
- Source-related phrase: +5
- Number/date present: +5
- Final score is clipped to 0–100

Categories:
- 75–100: Low linguistic risk
- 45–74: Moderate linguistic risk
- 0–44: High linguistic risk

This rubric is educational and should not be interpreted as a factual credibility measurement. A source phrase or number can be present in inaccurate content, and reliable writing may use emotional language.

## Troubleshooting

- If `streamlit` is not recognized, activate `.venv` and run `python -m streamlit run app.py`.
- If package installation fails, confirm Python is 3.10+ and retry in a new virtual environment.
- If the transformer model cannot download, check internet access. The app still works using fallback summarization.
- To reset local history, stop the app and delete `news_analysis.db`. This permanently deletes saved analyses.
- Keep the database private if pasted text contains sensitive information.

## Academic extension ideas

- Compare TextBlob sentiment with a transformer sentiment model
- Add source URLs and user-entered citations
- Add language selection and model evaluation
- Test the heuristic on a labeled dataset and report precision/recall for a clearly defined task
- Add user authentication only if required for deployment
