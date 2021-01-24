#import library
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import speech

## Text sentiment analysis
analyzer = SentimentIntensityAnalyzer()
for sentence in speech.sentences:
    vs = analyzer.polarity_scores(sentence)
    print("{:-<65} {}".format(sentence, str(vs)))