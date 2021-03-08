import urllib.request
import sentiment

compound = sentiment.vs['compound']

# if compound <= -0.05: # negative sentiment
#     color = 'red'
# elif compound >= 0.05: # positive sentiment
#     color = 'green'
# else: # neutral sentiment
#     color = 'yellow'

# IFTTT webhook
url = 'https://maker.ifttt.com/trigger/{}/with/key/NzX9u8NuVPaFWZyqQRhlv'.format(color)
urllib.request.urlopen(url)   