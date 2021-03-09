import pyodbc
# import ifttt
import sentiment
import speech
import time
import random
import string
import datetime
import urllib.request
from datetime import datetime, timedelta

server = ''
database = ''
username = ''
password = ''
# Un-comment the line below if running in Raspberry Pi
# dsn = 'rpitestsqlserverdatasource'

# Un-comment the line below if running code on Mac/PC
conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)

# Un-comment the next two lines below if running code on Raspberry Pi
# connString = 'DSN={0};UID={1};PWD={2};DATABASE={3};'.format(dsn,username,password,database)
# conn = pyodbc.connect(connString)

cursor = conn.cursor()

# Seconds since epoch at GMT
seconds = time.time()

# Random unique identifier
length_of_string = 3
random_string = "".join(random.choice(string.ascii_letters) for i in range(length_of_string))
random_identifier = random_string + str(seconds)

# Power on (slow fade from off to green, duration 5 seconds)
url = 'https://maker.ifttt.com/trigger/{}/with/key/NzX9u8NuVPaFWZyqQRhlv'.format(power_on)
urllib.request.urlopen(url)

# IFTTT webhook
def send_ifttt(color):
    url = 'https://maker.ifttt.com/trigger/{}/with/key/NzX9u8NuVPaFWZyqQRhlv'.format(color)
    urllib.request.urlopen(url)

# Un-comment to drop previous table of same name if one exists
# cursor.execute("DROP TABLE IF EXISTS list;")
# cursor.execute("DROP TABLE IF EXISTS test;")
# cursor.execute("DROP TABLE IF EXISTS test2;")
# print("Finished dropping table (if existed).")

# Un-comment to create table
# cursor.execute("CREATE TABLE list (curse_words NVARCHAR(MAX), time_allowance INT, curse_threshold INT, creationTime smalldatetime)")
# cursor.execute("CREATE TABLE test (speech NVARCHAR(MAX), pos FLOAT(53), compound FLOAT(53), neu FLOAT(53), neg FLOAT(53), color VARCHAR(50), creationTime smalldatetime)")
# cursor.execute("CREATE TABLE test2 (identifier NVARCHAR(MAX), speech NVARCHAR(MAX), pos FLOAT(53), compound FLOAT(53), neu FLOAT(53), neg FLOAT(53), color VARCHAR(50), creationTime smalldatetime)")
# print("Finished creating table.")

# Insert some data into table
# cursor.execute("INSERT INTO test (speech, pos, compound, neu, neg, color, creationTime) VALUES (?, ?, ?, ?, ?, ?, GETDATE());", (speech.capture, sentiment.vs['pos'], sentiment.vs['compound'], sentiment.vs['neu'], sentiment.vs['neg'], ifttt.color))
# cursor.execute("INSERT INTO test2 (identifier, speech, pos, compound, neu, neg, color, creationTime) VALUES (?, ?, ?, ?, ?, ?, ?, GETDATE());", (random_identifier, speech.capture, sentiment.vs['pos'], sentiment.vs['compound'], sentiment.vs['neu'], sentiment.vs['neg'], ifttt.color))
# Un-comment to manually test DB
# cursor.execute("INSERT INTO list (curse_words, time_allowance, curse_threshold, creationTime) VALUES (?, ?, ?, GETDATE());", (random_identifier, 120, 15))
# print("Inserted",cursor.rowcount,"row(s) of data.")

# Get the latest from the list table
list_query = "select top 1 * from list order by creationTime desc"
cursor.execute(list_query)
curse_fetch = cursor.fetchone()
curse_list = curse_fetch[0]
time_allowance = curse_fetch[1]
curse_threshold = curse_fetch[2]

# Comparing speech to curse words
# capture_list = speech.capture.split()
curse_count = 0

# Cursing
# for i in capture_list:
#     for j in curse_list:
#         if j == i:
#             curse_count += 1
#             color="blink_red"
#         else:
#             curse_count += 0
# if curse_count == curse_threshold:
#     time_allowance -= 180 # remove 3 mins
#     color = "rapid_red"
# elif curse_count == curse_threshold-1:
#     color="rapid_red"
#     color="red"

readings = []
SLS = 1

time_allowance_sec = time_allowance * 60
session_end = datetime.now() + timedelta(seconds = time_allowance_sec)
current_time = datetime.now()

# Sentiment
while current_time < session_end:
    capture_list = speech.capture.split()
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
        sleep(5)
        color = "red"
        send_ifttt(color)
        sleep(5)

    compound_query = "select avg(compound) from test where creationTime >= dateadd(minute, -3, getdate())"
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
    current_time = datetime.now()

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

    # Insert some data into table
    cursor.execute("INSERT INTO test2 (identifier, speech, pos, compound, neu, neg, color, creationTime) VALUES (?, ?, ?, ?, ?, ?, ?, GETDATE());", (random_identifier, speech.capture, sentiment.vs['pos'], sentiment.vs['compound'], sentiment.vs['neu'], sentiment.vs['neg'], color))

if current_time >= session_end:
    color="purple"
    send_ifttt(color)
    sleep(10)
    color="turn_off" #turn off lights
    send_ifttt(color)
    color="switch_off" #turn off smart plug
    send_ifttt(color)

    final_compound_query = "select avg(compound) from test2 where identifier = '{}';".format(random_identifier)
    cursor.execute(final_compound_query)
    final_compound_fetch = cursor.fetchone()
    final_average_compound = final_compound_fetch[0]

    if final_average_compound <= -0.01:
        cursor.execute("INSERT INTO list (time_allowance, creationTime) VALUES (?, GETDATE())", ((time_allowance - 120)/60))
    elif final_average_compund >= 0.01:
        cursor.execute("INSERT INTO list (time_allowance, creationTime) VALUES (?, GETDATE())", ((time_allowance + 120)/60))
    if curse_count >= curse_threshold:
        cursor.execute("INSERT INTO list (time_allowance, creationTime) VALUES (?, GETDATE())", ((time_allowance - 180)/60))


# Cleanup
conn.commit()
cursor.close()
conn.close()
print("Done.")