import sqlite3

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()
cursor.execute("DELETE FROM django_migrations")
conn.commit()
conn.close()
