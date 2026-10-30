# AI-BASED NEWS SENTIMENT AND CREDIBILITY ASSISTANCE DASHBOARD
## MCA Mini Project Report

## Abstract
The AI-Based News Sentiment and Credibility Assistance Dashboard is a Python web application designed to examine linguistic characteristics in news headlines, articles, and social-media posts. The system uses TextBlob for polarity-based sentiment analysis, NLTK for text preprocessing, rule-based patterns for clickbait and sensational wording, Hugging Face Transformers for optional summarization, SQLite for storing analysis history, and Plotly for dashboard charts. A heuristic score from 0 to 100 summarizes the warning signals detected by the configured rules. The application does not independently verify facts and does not label content as true or false. It is intended as an educational decision-support prototype that encourages users to review language patterns critically.

## 1. Introduction
Online information is published in many formats and can use neutral, emotional, or attention-seeking language. Readers may benefit from tools that highlight linguistic patterns such as excessive punctuation, absolute claims, vague attribution, and clickbait phrases. Natural Language Processing (NLP) provides methods for cleaning text, estimating sentiment, and producing summaries. This project combines introductory NLP methods with a simple web interface and database so users can explore these techniques in one place.

## 2. Problem Statement
Manually reviewing the tone and presentation of many news items can take time. A beginner-friendly tool is needed to demonstrate sentiment classification, pattern detection, summarization, and analysis history without making unsupported factual claims about the content.

## 3. Objectives
1. Build a local web interface using Streamlit.
2. Classify sentiment as Positive, Negative, or Neutral using TextBlob polarity thresholds.
3. Preprocess text with NLTK.
4. Detect selected clickbait, extreme, manipulative, and vague-attribution phrases.
5. Calculate a transparent heuristic linguistic-risk assistance score.
6. Generate a short summary where a free summarization model is available.
7. Store and retrieve analysis records using SQLite.
8. Visualize sentiment and risk categories with Plotly.
9. Export an individual analysis as a PDF report.
10. Display a clear disclaimer that the application does not verify truth.

## 4. Literature Survey
### 4.1 Natural Language Processing
NLP studies computational methods for processing human language. Common tasks include tokenization, text normalization, sentiment analysis, and summarization. Results depend on language, context, model design, and input quality.

### 4.2 Sentiment Analysis
Lexicon-based sentiment tools estimate polarity from words and phrases. TextBlob provides a polarity value between -1 and +1. Such tools can struggle with sarcasm, domain-specific terms, negation, and context. In this project, polarity above 0.1 is Positive, below -0.1 is Negative, and values in between are Neutral.

### 4.3 Text Preprocessing
Preprocessing can include lowercasing, URL and punctuation removal, tokenization, stop-word removal, and lemmatization. It helps demonstrate common NLP preparation steps. The original text is retained for sentiment and warning detection so formatting signals such as uppercase letters and exclamation marks are not lost.

### 4.4 Text Summarization
Transformer-based summarization models generate a shorter version of a longer passage. Their output may omit details or misrepresent nuance, so a summary should be treated as an aid rather than a replacement for the original article.

### 4.5 Rule-Based Warning Signals
Rule-based methods search for preselected words and patterns. They are transparent and easy to explain, but can produce false positives and false negatives. A warning phrase is not proof that a claim is inaccurate.

## 5. Methodology
1. User enters a headline and article text.
2. The application combines the supplied text and validates that it is not empty.
3. The preprocessing module lowercases text, removes URLs, numbers and punctuation, tokenizes, removes English stop words, and attempts lemmatization.
4. TextBlob calculates sentiment polarity.
5. Rule-based checks look for clickbait phrases, excessive exclamation marks, uppercase text, extreme words, emotionally manipulative words, vague attribution, source-related phrases, and numerical content.
6. The scoring function starts at 100, applies the specified deductions and additions, and clips the result to the 0–100 range.
7. A risk category is assigned from the score thresholds.
8. The summarizer attempts to use a Hugging Face model; if unavailable, it uses a simple fallback.
9. Results are saved to SQLite.
10. The user can inspect the dashboard, filter history, delete a record, or download a PDF.

## 6. System Requirements
### Hardware
- Dual-core processor or better
- 4 GB RAM minimum; 8 GB or more recommended for transformer summarization
- Sufficient disk space for Python packages and the downloaded model
- Internet access recommended for initial model/resource downloads

### Software
- Windows, macOS, or Linux
- Python 3.10 or newer recommended
- Visual Studio Code or another Python editor
- Streamlit, TextBlob, NLTK, Transformers, PyTorch, Pandas, Plotly, and ReportLab
- SQLite, included with standard Python builds

## 7. System Design
### Input
Headline and article/post text.

### Processing
Text preprocessing, sentiment analysis, pattern detection, scoring, and summarization.

### Storage
SQLite stores the title, full submitted text, sentiment, polarity, clickbait status, warning signals, score, category, summary, and timestamp.

### Output
Sentiment label, polarity, warning messages, score, risk category, summary, charts, history table, and optional PDF.

### Architecture
User → Streamlit interface → Analyzer → Preprocessing / TextBlob / warning rules / summarizer → SQLite → Dashboard and PDF output.

## 8. Modules
### 8.1 Home Module
Introduces the project, lists its capabilities, and displays the ethical disclaimer.

### 8.2 News Analysis Module
Accepts a headline and text, invokes the analysis functions, and displays the results.

### 8.3 Preprocessing Module
Cleans text, tokenizes it, removes stop words, and attempts lemmatization using NLTK.

### 8.4 Sentiment Module
Uses TextBlob polarity and applies the required thresholds: greater than 0.1 is Positive, less than -0.1 is Negative, otherwise Neutral.

### 8.5 Clickbait and Warning Module
Searches for configured phrases and formatting patterns. Detected signals are reported as linguistic indicators, not factual conclusions.

### 8.6 Scoring Module
Applies a transparent heuristic rule set to create a score from 0 to 100 and assigns a risk category. Because the rules are manually selected and not empirically validated, the score must not be described as a probability of truth.

### 8.7 Summarization Module
Uses a free Hugging Face Transformers summarization pipeline for longer text. Very short text is returned directly; failures use a basic extractive fallback.

### 8.8 Database Module
Creates the table and provides insert, select, lookup, and delete functions with parameterized SQL statements.

### 8.9 Dashboard Module
Uses Pandas to prepare the records and Plotly to display sentiment distribution, risk-category counts, score trends, and recent analyses.

### 8.10 PDF Module
Creates a downloadable report containing the analysis and disclaimer.

## 9. Database Design
Table name: `news_analysis`

| Field | Type | Description |
|---|---|---|
| analysis_id | INTEGER PRIMARY KEY AUTOINCREMENT | Unique record identifier |
| news_title | TEXT | Headline supplied by the user |
| news_text | TEXT | Submitted article or post |
| sentiment | TEXT | Positive, Negative, or Neutral |
| sentiment_score | REAL | TextBlob polarity from -1 to +1 |
| clickbait_status | TEXT | Result of configured pattern checks |
| warning_signals | TEXT | JSON-encoded list of warnings |
| credibility_score | INTEGER | Heuristic score from 0 to 100 |
| risk_category | TEXT | Low, Moderate, or High linguistic risk |
| summary | TEXT | Generated or fallback summary |
| analyzed_date | TEXT | Local analysis timestamp |

## 10. Testing
The following are manual test cases. Actual results should be recorded after running the application.

| Test | Input/action | Expected behavior |
|---|---|---|
| T1 | Submit empty headline and empty text | Validation error |
| T2 | Submit neutral short text | Analysis completes; summary uses short-text fallback |
| T3 | Submit text containing “you won't believe” | Clickbait pattern is reported |
| T4 | Submit more than three exclamation marks | Excess punctuation warning appears |
| T5 | Submit mostly uppercase text | Uppercase warning may appear if threshold is met |
| T6 | Submit text containing “according to a report” and digits | Source/numeric bonuses are applied by the rubric |
| T7 | Analyze a long article with model access | Transformer summary is attempted |
| T8 | Run without model access | Fallback summary is returned and application remains usable |
| T9 | Analyze multiple items | Records appear in SQLite history |
| T10 | Filter history by sentiment/category | Table updates to matching records |
| T11 | Delete a selected record | Record is removed from history |
| T12 | Open dashboard with saved records | Metrics and charts appear |
| T13 | Download PDF | A PDF report is generated |

## 11. Results
The application is designed to produce sentiment labels, polarity values, configured warning signals, a heuristic score, a linguistic-risk category, and a short summary. Saved records are used to calculate dashboard counts and score trends. Insert screenshots of the running Home page, Analyze News results, Dashboard charts, Analysis History, and downloaded PDF here after testing the project locally. Do not claim that the system detects factual misinformation unless a separate validated evaluation has been performed.

## 12. Limitations
- TextBlob is a basic sentiment tool and may not understand sarcasm or context.
- Rule-based phrase detection can miss new patterns and flag harmless writing.
- The score is a manually designed heuristic, not a scientifically validated credibility measure.
- A number, date, or source phrase does not establish factual accuracy.
- Summarization models can omit or distort details.
- Transformer downloads can require a stable internet connection, time, memory, and disk space.
- The project is primarily designed for English text.
- SQLite is appropriate for a local student project but is not intended for high-volume concurrent deployment.
- User-submitted text is stored locally; sensitive material should not be pasted into the application.

## 13. Future Enhancements
- Add source-link fields and user-assisted reference checking.
- Evaluate alternative sentiment models on a labeled dataset.
- Add support for multiple languages.
- Improve phrase detection with configurable rules.
- Add model evaluation, error analysis, and documented precision/recall where an appropriate labeled task exists.
- Add export to CSV and richer report templates.
- Add authentication and access controls if deployed for multiple users.
- Improve accessibility and responsive design.

## 14. Conclusion
The project demonstrates how Python NLP libraries, rule-based language analysis, summarization, database storage, and interactive visualization can be combined in a local web application. It helps users inspect the tone and presentation of text while clearly distinguishing linguistic warning signals from factual verification. The modular structure makes the project suitable for an MCA mini-project and provides a base for future experiments in NLP and responsible information analysis.

## References
1. TextBlob documentation: https://textblob.readthedocs.io/
2. NLTK documentation: https://www.nltk.org/
3. Streamlit documentation: https://docs.streamlit.io/
4. Hugging Face Transformers documentation: https://huggingface.co/docs/transformers/
5. Pandas documentation: https://pandas.pydata.org/docs/
6. Plotly Python documentation: https://plotly.com/python/
7. Python SQLite documentation: https://docs.python.org/3/library/sqlite3.html
8. ReportLab documentation: https://docs.reportlab.com/
