import sqlite3


sql = '''SELECT date('now', '-5 days')
FROM temperature_data;
'''

db = "temperature_data.db"
conn=sqlite3.connect(db)
cur=conn.cursor()
cur.execute(sql)
rows=cur.fetchall()
conn.commit()
conn.close()
for row in rows:
    print(row)