import pyodbc

server = ''
database = ''
username = ''
password = ''
conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = conn.cursor()

  # Drop previous table of same name if one exists
cursor.execute("DROP TABLE IF EXISTS test;")
print("Finished dropping table (if existed).")

  # Create table
cursor.execute("CREATE TABLE test (id int IDENTITY(1,1) PRIMARY KEY, name VARCHAR(50), quantity INTEGER);")
print("Finished creating table.")

  # Insert some data into table
cursor.execute("INSERT INTO test (name, quantity) VALUES (?, ?);", ("banana", 150))
print("Inserted",cursor.rowcount,"row(s) of data.")
cursor.execute("INSERT INTO test (name, quantity) VALUES (?, ?);", ("orange", 154))
print("Inserted",cursor.rowcount,"row(s) of data.")
cursor.execute("INSERT INTO test (name, quantity) VALUES (?, ?);", ("apple", 100))
print("Inserted",cursor.rowcount,"row(s) of data.")

  # Cleanup
conn.commit()
cursor.close()
conn.close()
print("Done.")