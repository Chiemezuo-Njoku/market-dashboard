from textblob import TextBlob

def analyze_sentiment(text: str):
    analysis = TextBlob(text).sentiment.polarity

    if analysis > 0:
        return "positive"
    elif analysis < 0:
        return "negative"
    else:
        return "neutral"