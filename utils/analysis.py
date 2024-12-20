
import spacy
from textblob import TextBlob  # Retain for sentiment analysis

# Load the spaCy medium model
nlp = spacy.load("en_core_web_md")

def analyze_response(text):
    # Sentiment analysis (using TextBlob)
    blob = TextBlob(text)
    sentiment = "positive" if blob.sentiment.polarity > 0.1 else "negative" if blob.sentiment.polarity < -0.1 else "neutral"

    # Extract key phrases using spaCy
    doc = nlp(text)
    key_phrases = [chunk.text for chunk in doc.noun_chunks if len(chunk.text.split()) > 1]

    # Assess response quality
    quality = "high" if len(text) > 100 and sentiment == "positive" else "medium" if len(text) > 50 else "low"

    return sentiment, key_phrases[:5], quality  # Limit to top 5 key phrases


def generate_score(sentiment, emotion_data, transcription):
    # Example scoring formula
    length_score = min(len(transcription) / 200, 1)
    emotion_score = 1 if emotion_data.get('happy', 0) > 50 else 0.5
    sentiment_score = 1 if sentiment == "positive" else 0.5
    return round((length_score + emotion_score + sentiment_score) / 3 * 100, 2)

def track_progress():
    import json
    try:
        with open("progress.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
