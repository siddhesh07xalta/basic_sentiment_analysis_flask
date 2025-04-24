from flask import Flask, request, jsonify
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

app = Flask(__name__)
analyzer = SentimentIntensityAnalyzer()

def get_sentiment(text):
    score = analyzer.polarity_scores(text)
    compound = score['compound']
    if compound >= 0.05:
        return "positive"
    elif compound <= -0.05:
        return "negative"
    else:
        return "neutral"

@app.route('/sentiment', methods=['POST'])
def sentiment():
    data = request.json
    if 'text' not in data:
        return jsonify({'error': 'No text provided'}), 400
    
    sentiment_result = get_sentiment(data['text'])
    return jsonify({
        'sentiment': sentiment_result
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
