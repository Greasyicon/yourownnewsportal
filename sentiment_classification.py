# sentiment_classification.py

from transformers import pipeline

def get_sentiment(text, model_path="results"):
    sentiment_analysis = pipeline("sentiment-analysis", model=model_path)
    return sentiment_analysis(text)

def classify_text(text):
    sentiment = get_sentiment(text)
    if sentiment["label"] == "POSITIVE":
        return "Positive"
    else:
        return "Negative"
