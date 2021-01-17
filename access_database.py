import sqlite3

con = sqlite3.connect('database.db')
cur = con.cursor()

print('===================================================')
print('Users')
print('===================================================')
sql = """
    SELECT * FROM users;
"""
cur.execute(sql)
for row in cur.fetchall():
    print('id=', row[0])
    print('username=', row[1])
    print('password=', row[2])
    print('=========================')