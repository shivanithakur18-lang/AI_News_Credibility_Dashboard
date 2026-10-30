# AI_News_Credibility_Dashboard
AI-powered News Credibility &amp; Sentiment Analysis Dashboard built with Python, Streamlit, SQLite, TextBlob, NLTK, Hugging Face, and Plotly.
# AI-Based News Sentiment and Credibility Assistance Dashboard

## 📌 Project Overview

The **AI-Based News Sentiment and Credibility Assistance Dashboard** is a Python-based web application that analyzes news headlines, articles, and social media posts.

The project uses Natural Language Processing (NLP), sentiment analysis, text summarization, and linguistic warning-signal detection to help users understand the language and tone of online content.

It provides sentiment classification, clickbait detection, warning signals, a heuristic credibility-assistance score, and analysis history through an interactive dashboard.

**Important Disclaimer:** This tool analyzes linguistic and content-based warning signals. It does not independently verify whether a news item is true or false.

## 🎯 Objectives

- Analyze the sentiment of news articles and headlines.
- Classify content as Positive, Negative, or Neutral.
- Detect common clickbait phrases.
- Identify sensational and potentially misleading language patterns.
- Generate a credibility-assistance score from 0 to 100.
- Generate short summaries of news content.
- Store previous analysis records.
- Display analysis results through interactive charts.
- Generate downloadable PDF reports.

## ✨ Key Features

1. **Sentiment Analysis:** Identifies positive, negative, and neutral sentiment.
2. **Text Polarity:** Calculates the polarity score of the entered text.
3. **Clickbait Detection:** Identifies commonly used clickbait phrases.
4. **Warning Signal Detection:** Highlights sensational language and other linguistic warning patterns.
5. **Credibility Assistance Score:** Provides a heuristic score based on detected warning signals.
6. **News Summarization:** Generates a short summary using a pretrained AI model when available.
7. **Analysis History:** Stores previous analyses using SQLite.
8. **Interactive Dashboard:** Displays sentiment distribution and credibility trends.
9. **PDF Report Generation:** Allows users to download analysis reports.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Streamlit | Web application and user interface |
| TextBlob | Sentiment analysis |
| NLTK | Text preprocessing |
| Hugging Face Transformers | Text summarization |
| SQLite | Database management |
| Pandas | Data handling |
| Plotly | Interactive charts |
| ReportLab | PDF report generation |

## ⚙️ Project Structure

```text
AI_News_Credibility_Dashboard/
│
├── app.py
├── analyzer.py
├── preprocessing.py
├── summarizer.py
├── database.py
├── pdf_report.py
├── requirements.txt
├── README.md
├── PROJECT_REPORT.md
├── test_analyzer.py
└── .gitignore
```

## 💻 Installation and Setup

### Step 1: Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_LINK
```

Replace `YOUR_GITHUB_REPOSITORY_LINK` with your actual GitHub repository URL.

### Step 2: Open the Project Folder

```bash
cd AI_News_Credibility_Dashboard
```

### Step 3: Create a Virtual Environment

```bash
python -m venv .venv
```

### Step 4: Activate the Environment

**For Windows:**

```bash
.venv\Scripts\activate
```

### Step 5: Install Required Libraries

```bash
pip install -r requirements.txt
```

### Step 6: Run the Application

```bash
python -m streamlit run app.py
```

The application will open in your web browser.

If it does not open automatically, visit:

```text
http://localhost:8501
```

## 📊 Application Modules

| Module | Description |
|---|---|
| Home | Displays project introduction and features |
| Analyze News | Performs sentiment and warning-signal analysis |
| Dashboard | Displays charts and analysis statistics |
| Analysis History | Shows previously saved analyses |
| About the Project | Provides project information and details |

## 🗄️ Database

The project uses **SQLite** to store analysis records.

The database maintains information such as:

- News text
- Sentiment classification
- Polarity score
- Credibility-assistance score
- Warning signals
- Analysis date and time

The database is initialized automatically when the application runs.

## 🔍 Working Methodology

1. The user enters a news headline, article, or social media post.
2. The application preprocesses the text.
3. Sentiment analysis identifies the overall tone.
4. Clickbait and warning-signal detection checks for suspicious linguistic patterns.
5. A heuristic credibility-assistance score is calculated.
6. A short summary is generated when the summarization model is available.
7. The results are stored in SQLite.
8. The dashboard displays the analysis and allows PDF report generation.

## ⚠️ Limitations

- The application does not independently verify news authenticity.
- Sentiment analysis may not correctly understand sarcasm or complex language.
- Warning signals are based on predefined linguistic patterns.
- The credibility-assistance score is heuristic and should not be treated as a factual probability.
- AI summarization may require an internet connection to download the pretrained model initially.

## 🚀 Future Enhancements

- Integration with trusted fact-checking websites and APIs.
- Support for multiple languages.
- Advanced machine learning-based classification.
- Real-time news analysis.
- Improved clickbait and misinformation detection.
- News source comparison and verification assistance.

## 🎓 Academic Project

**Project Title:** AI-Based News Sentiment and Credibility Assistance Dashboard

**Project Type:** MCA Mini Project

**Domain:** Artificial Intelligence and Natural Language Processing

**Programming Language:** Python

## 👩‍💻 Author

**Shivani Thakur**

Master of Computer Applications (MCA)

Chandigarh University

---

⭐ If you find this project useful, consider giving the repository a star.

**Disclaimer:** This project is developed for educational purposes. Its results are intended to assist users in examining linguistic warning signals, not to establish the truth or falsity of news content.
