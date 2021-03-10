#import library
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import speech

## Text sentiment analysis
analyzer = SentimentIntensityAnalyzer()

def measure_sentiment(sentences):
    for words in sentences:
        vs = analyzer.polarity_scores(words)
        print("{:-<65} {}".format(words, str(vs)))
