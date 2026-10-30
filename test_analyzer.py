import unittest
from analyzer import get_sentiment, analyze_warning_signals, calculate_credibility_score

class AnalyzerTests(unittest.TestCase):
    def test_sentiment_returns_expected_shape(self):
        label, polarity = get_sentiment("The product is wonderful and excellent.")
        self.assertIn(label, ["Positive", "Negative", "Neutral"])
        self.assertGreaterEqual(polarity, -1.0)
        self.assertLessEqual(polarity, 1.0)

    def test_clickbait_phrase_detected(self):
        signals = analyze_warning_signals("You won't believe this shocking story!")
        self.assertTrue(signals["clickbait_hits"])

    def test_score_is_bounded(self):
        signals = analyze_warning_signals("SHOCKING!!! NEVER EVER!!!")
        score, category = calculate_credibility_score(signals)
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 100)
        self.assertIn(category, ["Low linguistic risk", "Moderate linguistic risk", "High linguistic risk"])

if __name__ == "__main__":
    unittest.main()
