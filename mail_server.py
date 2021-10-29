import sqlite3


db = sqlite3.connect('server_db.sqlite')
cur = db.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users (
id INT,
name TEXT
)
""")
db.commit()