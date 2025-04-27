from flask import Flask, request, jsonify
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re

app = Flask(__name__)
analyzer = SentimentIntensityAnalyzer()

def clean_text(text):
    cleaned = re.sub(r'\s+', ' ', text)
    return cleaned.strip()

def get_sentiment(text):
    cleaned_text = clean_text(text)
    score = analyzer.polarity_scores(cleaned_text)
    compound = score['compound']
    if compound >= 0.05:
        return "positive"
    elif compound <= -0.05:
        return "negative"
    else:
        return "neutral"

@app.route('/sentiment', methods=['POST'])
def sentiment():
    data = request.get_json(silent=True)
    if not data or 'text' not in data:
        return jsonify({'error': 'No text provided'}), 400
    
    sentiment_result = get_sentiment(data['text'])
    return jsonify({
        'sentiment': sentiment_result
    })

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok'}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
