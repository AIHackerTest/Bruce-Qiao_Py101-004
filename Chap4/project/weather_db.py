"""use sqlite3 build weather.db"""

import sqlite3

conn = sqlite3.connect('weather.db')

c = conn.cursor()

c.execute('''CREATE TABLE inquiry_list (city text, weather text, temp text, update_time text)''')

c.execute("INSERT INTO inquiry_list VALUES ('曲江', '晴', '24', ‘2017-09-04 14:45’)")
conn.commit()

t = ('曲江',)
c.execute('SELECT * FROM inquiry_list WHERE symbol=?', t)
print(c.fetchone())

conn.close()
