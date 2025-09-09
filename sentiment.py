from transformers import pipeline

# Initialize once
sentiment_pipeline = pipeline("sentiment-analysis")

def analyze_sentiment(text):
    """
    Returns a list of dicts: [{'label': 'POSITIVE', 'score': 0.987}]
    """
    if not text or text.strip() == "":
        return [{'label': 'NEUTRAL', 'score': 0.0}]
    
    try:
        result = sentiment_pipeline(text)
        return result
    except Exception as e:
        print(f"Sentiment error: {e}")
        return [{'label': 'ERROR', 'score': 0.0}]
