import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

from database import init_db, save_analysis, get_analyses, delete_analysis, get_analysis_by_id
from analyzer import analyze_news
from pdf_report import create_pdf_report

st.set_page_config(
    page_title="News Sentiment & Credibility Assistant",
    page_icon="📰",
    layout="wide",
)

DISCLAIMER = (
    "This tool analyzes linguistic and content-based warning signals. "
    "It does not independently verify whether a news item is true or false."
)

init_db()

# Keep navigation simple for a beginner-friendly Streamlit project.
st.sidebar.title("📰 News Analysis")
page = st.sidebar.radio(
    "Navigate",
    ["Home", "Analyze News", "Dashboard", "Analysis History", "About the Project"],
)
st.sidebar.caption("Local MCA mini project")
st.sidebar.warning(DISCLAIMER)

def show_result(result, title, article):
    """Display one analysis result in a consistent layout."""
    st.subheader("Analysis results")
    c1, c2, c3 = st.columns(3)
    c1.metric("Sentiment", result["sentiment"])
    c2.metric("Polarity", f'{result["sentiment_score"]:.3f}')
    c3.metric("Credibility-assistance score", f'{result["credibility_score"]}/100')

    risk = result["risk_category"]
    if risk == "Low linguistic risk":
        st.success(f"Risk category: {risk}")
    elif risk == "Moderate linguistic risk":
        st.warning(f"Risk category: {risk}")
    else:
        st.error(f"Risk category: {risk}")

    st.progress(result["credibility_score"] / 100)
    st.write("**Clickbait detected:**", result["clickbait_status"])
    st.write("**Clickbait / warning details:**")
    if result["warning_signals"]:
        for warning in result["warning_signals"]:
            st.warning(warning)
    else:
        st.info("No configured warning patterns were detected. This does not prove accuracy.")

    st.write("**Short summary**")
    st.write(result["summary"])
    st.caption(DISCLAIMER)

    pdf_bytes = create_pdf_report(title, article, result)
    st.download_button(
        "Download this analysis as PDF",
        data=pdf_bytes,
        file_name="news_analysis_report.pdf",
        mime="application/pdf",
    )

if page == "Home":
    st.title("AI-Based News Sentiment and Credibility Assistance Dashboard")
    st.write(
        "A local Python web application that studies the language used in news "
        "headlines, articles, and social-media posts. It combines basic sentiment "
        "analysis, pattern-based warning signals, text summarization, and historical charts."
    )
    st.info(DISCLAIMER)
    st.subheader("Main features")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("- Positive, Negative, or Neutral sentiment\n"
                    "- Text polarity score\n"
                    "- Clickbait phrase detection\n"
                    "- Linguistic warning signals")
    with col2:
        st.markdown("- Heuristic score from 0 to 100\n"
                    "- Automatic short summary when a model is available\n"
                    "- SQLite analysis history\n"
                    "- Interactive Plotly dashboard and PDF export")
    st.subheader("How to use")
    st.markdown(
        "1. Open **Analyze News**.\n"
        "2. Enter a headline and paste the text.\n"
        "3. Select **Analyze text**.\n"
        "4. Review the result and optionally download the PDF.\n"
        "5. Visit **Dashboard** or **Analysis History** to review saved analyses."
    )

elif page == "Analyze News":
    st.title("Analyze News")
    st.write("Paste a headline and the article or post you want to examine.")
    with st.form("news_analysis_form"):
        title = st.text_input("News headline", max_chars=300)
        article = st.text_area("News/article/social-media text", height=260)
        submitted = st.form_submit_button("Analyze text", type="primary")

    if submitted:
        if not article.strip() and not title.strip():
            st.error("Please enter a headline or article text.")
        else:
            combined_text = "\n".join(part for part in [title.strip(), article.strip()] if part)
            with st.spinner("Analyzing text. Summarization may take longer on the first run..."):
                result = analyze_news(combined_text)
            record_id = save_analysis(
                news_title=title.strip() or "Untitled analysis",
                news_text=combined_text,
                sentiment=result["sentiment"],
                sentiment_score=result["sentiment_score"],
                clickbait_status=result["clickbait_status"],
                warning_signals=result["warning_signals"],
                credibility_score=result["credibility_score"],
                risk_category=result["risk_category"],
                summary=result["summary"],
            )
            st.success(f"Analysis saved to local history (record #{record_id}).")
            show_result(result, title.strip() or "Untitled analysis", combined_text)

elif page == "Dashboard":
    st.title("Dashboard")
    rows = get_analyses()
    if not rows:
        st.info("No analyses are saved yet. Analyze a news item first.")
    else:
        df = pd.DataFrame(rows)
        df["analyzed_date"] = pd.to_datetime(df["analyzed_date"], errors="coerce")
        total = len(df)
        avg_score = float(df["credibility_score"].mean()) if total else 0
        most_common = df["sentiment"].mode().iloc[0] if not df["sentiment"].mode().empty else "N/A"
        a, b, c = st.columns(3)
        a.metric("Total analyzed items", total)
        b.metric("Average assistance score", f"{avg_score:.1f}/100")
        c.metric("Most common sentiment", most_common)

        sentiment_counts = df["sentiment"].value_counts().reindex(
            ["Positive", "Negative", "Neutral"], fill_value=0
        ).reset_index()
        sentiment_counts.columns = ["Sentiment", "Count"]
        risk_order = ["Low linguistic risk", "Moderate linguistic risk", "High linguistic risk"]
        risk_counts = df["risk_category"].value_counts().reindex(risk_order, fill_value=0).reset_index()
        risk_counts.columns = ["Risk category", "Count"]

        left, right = st.columns(2)
        with left:
            st.subheader("Sentiment distribution")
            fig = px.pie(sentiment_counts, names="Sentiment", values="Count", hole=0.35)
            st.plotly_chart(fig, use_container_width=True)
        with right:
            st.subheader("Linguistic-risk categories")
            fig = px.bar(risk_counts, x="Risk category", y="Count", text="Count")
            st.plotly_chart(fig, use_container_width=True)

        trend = df.dropna(subset=["analyzed_date"]).sort_values("analyzed_date")
        if not trend.empty:
            st.subheader("Credibility-assistance score trend")
            fig = px.line(
                trend, x="analyzed_date", y="credibility_score",
                markers=True, hover_data=["news_title", "sentiment"]
            )
            fig.update_yaxes(range=[0, 100])
            st.plotly_chart(fig, use_container_width=True)

        st.subheader("Recent analyses")
        st.dataframe(
            df.sort_values("analyzed_date", ascending=False)[
                ["analysis_id", "news_title", "sentiment", "sentiment_score",
                 "credibility_score", "risk_category", "analyzed_date"]
            ].head(10),
            use_container_width=True,
            hide_index=True,
        )
        st.caption(DISCLAIMER)

elif page == "Analysis History":
    st.title("Analysis History")
    rows = get_analyses()
    if not rows:
        st.info("No saved records are available.")
    else:
        df = pd.DataFrame(rows)
        f1, f2, f3 = st.columns([1, 1, 2])
        sentiments = ["All"] + sorted(df["sentiment"].dropna().unique().tolist())
        risks = ["All"] + sorted(df["risk_category"].dropna().unique().tolist())
        selected_sentiment = f1.selectbox("Filter by sentiment", sentiments)
        selected_risk = f2.selectbox("Filter by risk category", risks)
        search = f3.text_input("Search headline or text")
        filtered = df.copy()
        if selected_sentiment != "All":
            filtered = filtered[filtered["sentiment"] == selected_sentiment]
        if selected_risk != "All":
            filtered = filtered[filtered["risk_category"] == selected_risk]
        if search.strip():
            mask = (
                filtered["news_title"].fillna("").str.contains(search, case=False, regex=False)
                | filtered["news_text"].fillna("").str.contains(search, case=False, regex=False)
            )
            filtered = filtered[mask]

        st.dataframe(
            filtered[["analysis_id", "news_title", "sentiment", "sentiment_score",
                      "clickbait_status", "credibility_score", "risk_category", "analyzed_date"]],
            use_container_width=True,
            hide_index=True,
        )
        st.subheader("View or delete a record")
        ids = filtered["analysis_id"].astype(int).tolist()
        if ids:
            selected_id = st.selectbox("Select record ID", ids)
            record = get_analysis_by_id(int(selected_id))
            if record:
                with st.expander("View selected record details"):
                    st.write("**Headline:**", record["news_title"])
                    st.write("**Text:**", record["news_text"])
                    st.write("**Warnings:**", record["warning_signals"] or "None recorded")
                    st.write("**Summary:**", record["summary"])
                confirm = st.checkbox("I confirm that I want to delete this record.")
                if st.button("Delete selected record", disabled=not confirm):
                    delete_analysis(int(selected_id))
                    st.success("Record deleted.")
                    st.rerun()
        st.caption(DISCLAIMER)

elif page == "About the Project":
    st.title("About the Project")
    st.markdown(
        "**Project title:** AI-Based News Sentiment and Credibility Assistance Dashboard\n\n"
        "**Purpose:** To provide an educational demonstration of sentiment analysis, "
        "text preprocessing, rule-based language signals, summarization, database storage, "
        "and dashboard visualization.\n\n"
        "**Core libraries:** Streamlit, TextBlob, NLTK, Transformers, Pandas, Plotly, SQLite, ReportLab.\n\n"
        "**Important limitation:** The score is a manually designed heuristic. It is not a "
        "validated misinformation classifier, a fact-checking service, or a measure of truth."
    )
    st.info(DISCLAIMER)
