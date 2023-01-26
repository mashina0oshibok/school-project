import sqlite3
from config import Database_path

# Connect to SQLite3 database (SQLite3DataBase.db)
db_connection = sqlite3.connect(Database_path)
cursor = db_connection.cursor()

# Drop databases
with db_connection:
    cursor.execute("DROP TABLE authors")
    cursor.execute("DROP TABLE books")
    cursor.execute("DROP TABLE users")
    cursor.execute("DROP TABLE requests")

# Disconnect from server
db_connection.close()
