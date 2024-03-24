import sqlite3

# connection with the DB
connection = sqlite3.connect("data.db")
cursor = connection.cursor()

# query data
cursor.execute("SELECT * FROM events WHERE date='2088.10.15'")
rows = (cursor.fetchall())
print(rows)

# query columns
cursor.execute("SELECT band, date  FROM events WHERE date='2088.10.15'")
rows = (cursor.fetchall())
print(rows)

# insert rows
new_rows = [('Cats', 'Cat City', '2088.10.17'),
            ('Hens', 'Hen City', '2088.10.17')]
cursor.executemany("INSERT INTO events VALUES(?,?,?)", new_rows)
connection.commit()

cursor.execute("SELECT * FROM events")
rows = (cursor.fetchall())
print(rows)
