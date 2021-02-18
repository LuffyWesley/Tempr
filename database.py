import pyodbc
import ifttt
import sentiment
import speech

dsn = 'rpitestsqlserverdatasource'
server = ''
database = ''
username = ''
password = ''

# Comment or un-comment the line below if running code on Mac/PC
conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)

# Comment or un-comment the next two lines below if running code on Raspberry Pi
connString = 'DSN={0};UID={1};PWD={2};DATABASE={3};'.format(dsn,username,password,database)
conn = pyodbc.connect(connString)

cursor = conn.cursor()

# Drop previous table of same name if one exists
# cursor.execute("DROP TABLE IF EXISTS test2;")
# print("Finished dropping table (if existed).")

# Create table
# cursor.execute("CREATE TABLE test2 (speech NVARCHAR(MAX), pos FLOAT(53), compound FLOAT(53), neu FLOAT(53), neg FLOAT(53), color VARCHAR(50), creationTime smalldatetime)")
# print("Finished creating table.")

# Insert some data into table
cursor.execute("INSERT INTO test2 (speech, pos, compound, neu, neg, color, creationTime) VALUES (?, ?, ?, ?, ?, ?, GETDATE());", (speech.capture, sentiment.vs['pos'], sentiment.vs['compound'], sentiment.vs['neu'], sentiment.vs['neg'], ifttt.color))
print("Inserted",cursor.rowcount,"row(s) of data.")

# Cleanup
conn.commit()
cursor.close()
conn.close()
print("Done.")