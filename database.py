import pyodbc
import time
import random
import string
import datetime
import urllib.request
import speech_recognition as sr
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# DB Credentials
dsn = 'rpitestsqlserverdatasource'
user = ''
password = ''
database = ''
server = ''

# Un-comment the next two lines below if running code on Raspberry Pi
# connString = 'DSN={0};UID={1};PWD={2};DATABASE={3};'.format(dsn,user,password,database)
# conn = pyodbc.connect(connString)

# Un-comment the line below if running code on Mac/PC
conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+user+';PWD='+ password)

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

# End sequence
def deathSequence(random_identifier,cursor, time_allowance):
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
        time_allowance = (time_allowance - 120)/60
    
    elif final_average_compound >= 0.01:
        time_allowance = (time_allowance + 120)/60
    
    if curse_count >= curse_threshold:
        time_allowance = (time_allowance - 180)/60
        
    cursor.execute("INSERT INTO list (time_allowance, curse_words, curse_threshold, creationTime) VALUES (?, ?, ?, GETDATE())", (time_allowance, curse_list, curse_threshold))
    conn.commit()

# Get the latest from the list table
list_query = "select top 1 * from list order by creationTime desc"
cursor.execute(list_query)
curse_fetch = cursor.fetchone()
curse_list = curse_fetch[0].lower()
time_allowance = curse_fetch[1]
curse_threshold = curse_fetch[2]

print(time_allowance)
print(curse_threshold)
print(curse_list)

# Comparing speech to curse words
curse_count = 0

readings = []
SLS = 1

#time_allowance_sec = time_allowance * 60
time_allowance_sec = 200
session_end = datetime.datetime.now() + datetime.timedelta(seconds = time_allowance_sec)
current_time = datetime.datetime.now()

startTime = round(time.time())

# Initialize recognizer class (for recognizing the speech)
r = sr.Recognizer()
m = sr.Microphone()

# Sentiment
while current_time < session_end:
    sentences = []
    with sr.Microphone() as source:
        print("Talk")
        audio_text = r.listen(source, phrase_time_limit = 10)
        print("Time over, thanks")
           
    # recoginize_() method will throw a request error if the API is unreachable, hence using exception handling    
        try:
            # using google speech recognition
            value = r.recognize_google(audio_text).lower()
            sentences.append(value)
            print("Text:" + value)
        except:
            print("Sorry, I did not get that")
            continue
    
    time1 = round(time.time() * 1000)
    
    #Analyze sentiment
    analyzer = SentimentIntensityAnalyzer()
    vs = analyzer.polarity_scores(sentences)
    print("{:-<65} {}".format(' '.join(sentences), str(vs)))
    
    time.time_ns() 
    time2 = round(time.time() * 1000)
    print((time2 - time1) / 1000.0)
    
    # Insert some data into table
    cursor.execute("INSERT INTO test2 (identifier, speech, pos, compound, neu, neg, creationTime) VALUES (?, ?, ?, ?, ?, ?, GETDATE());", (random_identifier, value, vs['pos'], vs['compound'], vs['neu'], vs['neg']))
    conn.commit()

    color = None
    #cursing
    capture_list = value.split()
    for i in capture_list:
        for j in curse_list.split(", "):
            if j == i:
                curse_count += 1
                color = "blink_red"
                print(color)

        if "**" in i:
            curse_count += 1
            color = "blink_red"
            print(color)

    print(curse_count)
    
    if curse_count >= curse_threshold:
        color = "rapid_red"
        print(color)
        send_ifttt(color)
        deathSequence(random_identifier,cursor,time_allowance)
        break
    elif curse_count == curse_threshold - 1:
        color = "rapid_red"
        print(color)
        send_ifttt(color)
        time.sleep(5)
        color = "red"
        print(color)
        send_ifttt(color)
        color = None
    
    if color != None:
        send_ifttt(color)

    time.sleep(1)
    
    endTime = round(time.time())
    
    if endTime - startTime < 60:
        continue
    
    compound_query = "select avg(compound) from test2 where creationTime >= dateadd(minute, -1, getdate())"
    cursor.execute(compound_query)
    compound_fetch = cursor.fetchone()
    average_compound = compound_fetch[0]
    print(average_compound)

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

    if SLS == 1:
        color = 'green'
    if SLS == 2:  # Low aggression
        color = 'yellow'
        print(color)
    elif SLS == 3:  # Medium aggression
        color = 'orange'
        print(color)
    elif SLS == 4:  # Medium high aggression
        color = "red_orange"
        print(color)
    elif SLS == 5:  # Max aggression
        color = 'red'
        print(color)
    else: 
        color = 'red'
        print(color)
    ##send to IFTTT
    send_ifttt(color)
    startTime = round(time.time())

if current_time >= session_end:
    deathSequence(random_identifier, cursor, time_allowance)

# Close connection to DB
cursor.close()
conn.close()
print("Done.")
