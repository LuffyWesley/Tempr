import pyodbc
import ifttt
import sentiment
import speech

server = ''
database = ''
username = ''
password = ''
conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = conn.cursor()

# Drop previous table of same name if one exists
cursor.execute("DROP TABLE IF EXISTS test2;")
print("Finished dropping table (if existed).")

# Create table
cursor.execute("CREATE TABLE test2 (speech NVARCHAR(MAX), pos FLOAT(53), compound FLOAT(53), neu FLOAT(53), neg FLOAT(53), color VARCHAR(50), creationTime smalldatetime)")
print("Finished creating table.")

# Insert some data into table
cursor.execute("INSERT INTO test2 (speech, pos, compound, neu, neg, , color, creationTime) VALUES (?, ?, ?, ?, ?, ?, GETDATE());", (speech.capture, sentiment.vs['pos'], sentiment.vs['compound'], sentiment.vs['neu'], sentiment.vs['neg'], ifttt.color))
print("Inserted",cursor.rowcount,"row(s) of data.")

# Cleanup
conn.commit()
cursor.close()
conn.close()
print("Done.")