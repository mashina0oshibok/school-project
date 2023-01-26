import sqlite3
from config import *

# Connect to SQLite3 database (SQLite3DataBase.db)
db_connection = sqlite3.connect(Database_path)
cursor = db_connection.cursor()

# Creating tables
with db_connection:
    cursor.execute(Create_Authors_Table)
    cursor.execute(Create_Books_Table)
    cursor.execute(Create_Users_Table)
    cursor.execute(Create_Requests_Table)

# Disconnect from servers
db_connection.close()
