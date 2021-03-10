import pyodbc
# import sentiment
# import speech
import time
import random
import string
import datetime
import urllib.request
import speech_recognition as sr
import urllib.request
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
# import speech

dsn = 'rpitestsqlserverdatasource'
user = 'tempr.admin@tempr'
password = 'VQ7_68667BQZ8qDA4R'
database = 'tempr'

connString = 'DSN={0};UID={1};PWD={2};DATABASE={3};'.format(dsn,user,password,database)
conn = pyodbc.connect(connString)

cursor = conn.cursor()

# Seconds since epoch at GMT
seconds = time.time()

# Turn plug on
url = 'https://maker.ifttt.com/trigger/{}/with/key/NzX9u8NuVPaFWZyqQRhlv'.format('plug_on')
urllib.request.urlopen(url)
 
# Power on (slow fade from off to green, duration 5 seconds)
url = 'https://maker.ifttt.com/trigger/{}/with/key/NzX9u8NuVPaFWZyqQRhlv'.format('power_on')
urllib.request.urlopen(url)

# Random unique identifier
length_of_string = 3
random_string = "".join(random.choice(string.ascii_letters) for i in range(length_of_string))
random_identifier = random_string + str(seconds)

# IFTTT webhook
def send_ifttt(color):
    url = 'https://maker.ifttt.com/trigger/{}/with/key/NzX9u8NuVPaFWZyqQRhlv'.format(color)
    urllib.request.urlopen(url)

# Get the latest from the list table
list_query = "select top 1 * from list order by creationTime desc"
cursor.execute(list_query)
curse_fetch = cursor.fetchone()
curse_list = curse_fetch[0].lower()
time_allowance = curse_fetch[1]
curse_threshold = curse_fetch[2]

# Comparing speech to curse words
curse_count = 0

readings = []
SLS = 1

time_allowance_sec = time_allowance * 60
session_end = datetime.datetime.now() + datetime.timedelta(seconds = time_allowance_sec)
current_time = datetime.datetime.now()

# Sentiment
while current_time < session_end:
    # Initialize recognizer class (for recognizing the speech)
    r = sr.Recognizer()
    m = sr.Microphone()
    sentences = []
    with sr.Microphone() as source:
        print("Talk")
        audio_text = r.listen(source)
        print("Time over, thanks")
    
    # recoginize_() method will throw a request error if the API is unreachable, hence using exception handling    
        try:
            # using google speech recognition
            value = r.recognize_google(audio_text).lower()
            sentences.append(value)
            print("Text:" + value)
        except:
            print("Sorry, I did not get that")
    
    analyzer = SentimentIntensityAnalyzer()
    for words in sentences:
        vs = analyzer.polarity_scores(words)
        print("{:-<65} {}".format(words, str(vs)))
    
    # Insert some data into table
    cursor.execute("INSERT INTO test2 (identifier, speech, pos, compound, neu, neg, creationTime) VALUES (?, ?, ?, ?, ?, ?, GETDATE());", (random_identifier, value, vs['pos'], vs['compound'], vs['neu'], vs['neg']))
    
    #cursing
    capture_list = value.split()
    for i in capture_list:
        for j in curse_list:
            if j == i:
                curse_count += 1
                color = "blink_red"
                send_ifttt(color)
            else:
                curse_count += 0
    if curse_count == curse_threshold:
        time_allowance -= 180  # remove 3 mins
        color = "rapid_red"
        send_ifttt(color)

    elif curse_count == curse_threshold - 1:
        color = "rapid_red"
        send_ifttt(color)
        time.sleep(5)
        color = "red"
        send_ifttt(color)

    compound_query = "select avg(compound) from test2 where creationTime >= dateadd(minute, -180, getdate())"
    cursor.execute(compound_query)
    compound_fetch = cursor.fetchone()
    average_compound = compound_fetch[0]

    if average_compound >= 0.05: # positive
        readings.append("pos")
        if SLS > 1: ## 1 step down for positive behavior
            SLS = SLS - 1
        else:
            SLS = 1

    elif average_compound <= -0.05: # negative
        if average_compound <= -0.5: #aggressive negative
            readings.append("aggressive")

            if readings[-3:] == ["aggressive", "aggressive", "aggressive"]:
                SLS = 5
            elif readings[-2:] == ["aggressive", "aggressive"]:
                SLS = 4
            elif readings[-2:] == ["pos", "aggressive"] and SLS > 2:
                SLS = 4
            else:
                SLS = 3
        elif average_compound <= -0.05: ##medium_negative
            readings.append("med_neg")
            if readings[-3:] == ["med_neg", "med_neg", "med_neg"]:
                SLS = 3
            elif SLS == 1:
                SLS = 2

    if len(readings) == 4:
        readings.pop(0)
    current_time = datetime.datetime.now()

    if SLS == 2:  # Low aggression
        color = 'yellow'
    elif SLS == 3:  # Medium aggression
        color = 'orange'
    elif SLS == 4:  # Medium high aggression
        color = "red_orange"
    elif SLS == 5:  # Max aggression
        color = 'red'
    else:  # Neutral
        color = 'green'
    ##send to IFTTT
    send_ifttt(color)

    
if current_time >= session_end:
    color="purple"
    time.sleep(10)
    send_ifttt(color)
    color="turn_off" #turn off lights
    send_ifttt(color)
    color="switch_off" #turn off smart plug
    send_ifttt(color)

    final_compound_query = "select avg(compound) from test2 where identifier = '{}';".format(random_identifier)
    cursor.execute(final_compound_query)
    final_compound_fetch = cursor.fetchone()
    final_average_compound = final_compound_fetch[0]

    if final_average_compound <= -0.01:
        cursor.execute("INSERT INTO list (time_allowance, curse_words, curse_threshold, creationTime) VALUES (?, ?, ?, GETDATE())", ((time_allowance - 120)/60), curse_list, curse_threshold)
    elif final_average_compound >= 0.01:
        cursor.execute("INSERT INTO list (time_allowance, curse_words, curse_threshold, creationTime) VALUES (?, ?, ?, GETDATE())", ((time_allowance + 120)/60), curse_list, curse_threshold)
    if curse_count >= curse_threshold:
        cursor.execute("INSERT INTO list (time_allowance, curse_words, curse_threshold, creationTime) VALUES (?, ?, ?, GETDATE())", ((time_allowance - 180)/60), curse_list, curse_threshold)


# Cleanup
conn.commit()
cursor.close()
conn.close()
print("Done.")
