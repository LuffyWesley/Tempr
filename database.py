import pyodbc
import ifttt
import sentiment
import speech
import time
import random
import string

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

# Un-comment to drop previous table of same name if one exists
# cursor.execute("DROP TABLE IF EXISTS test2;")
# print("Finished dropping table (if existed).")

# Un-comment to create table
# cursor.execute("CREATE TABLE test2 (identifier NVARCHAR(MAX), speech NVARCHAR(MAX), pos FLOAT(53), compound FLOAT(53), neu FLOAT(53), neg FLOAT(53), color VARCHAR(50), creationTime smalldatetime)")
# print("Finished creating table.")

# Insert some data into table
cursor.execute("INSERT INTO test2 (identifier, speech, pos, compound, neu, neg, color, creationTime) VALUES (?, ?, ?, ?, ?, ?, ?, GETDATE());", (random_identifier, speech.capture, sentiment.vs['pos'], sentiment.vs['compound'], sentiment.vs['neu'], sentiment.vs['neg'], ifttt.color))
# Un-comment to manually test DB
# cursor.execute("INSERT INTO test2 (identifier, speech, pos, compound, neu, neg, color, creationTime) VALUES (?, ?, ?, ?, ?, ?, ?, GETDATE());", (random_identifier , 'I am beautiful', 1.0, 0.05, 0.0, 0.0, "green"))
print("Inserted",cursor.rowcount,"row(s) of data.")

# Cleanup
conn.commit()
cursor.close()
conn.close()
print("Done.")