import sqlite3

conn = sqlite3.connect('user.db')
cursor = conn.cursor() 
cmd = "CREATE TABLE user (id INTEGER PRIMARY KEY AUTOINCREMENT , name TEXT, password TEXT)"
cursor.execute(cmd)
cmd = "CREATE TABLE store (id INTEGER PRIMARY KEY AUTOINCREMENT , name TEXT)"
cursor.execute(cmd)
cmd = "CREATE TABLE item (id INTEGER PRIMARY KEY AUTOINCREMENT , name TEXT, price FLOAT , store_id INTEGER, FOREIGN KEY(store_id) REFERENCES store(id) )"
cursor.execute(cmd)


# cmd = "SELECT * FROM user"
# result = cursor.execute(cmd)
# print('result',result.fetchall())
# for row in result:
#     print(row)
# row = result.fetchone()
# if row:
#     print(row)
conn.commit()
conn.close()