<<<<<<< HEAD
from transformers import pipeline

sentiment_model = pipeline("sentiment-analysis")

def analyze_sentiment(text):
    result = sentiment_model(text)[0]
    return result['label'], result['score']
=======
from transformers import pipeline

sentiment_model = pipeline("sentiment-analysis")

def analyze_sentiment(text):
    result = sentiment_model(text)[0]
    return result['label'], result['score']
>>>>>>> 647a1a0ecdbb67439beb8685a67f4906de223262
