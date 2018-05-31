import sqlite3
import os
import Configure

conn = None

def sqlite3_init():
	global conn
	try:
		conn = sqlite3.connect(Configure.DB_NAME)
	except Exception as e:
		print ('sqlite3 init fail.')
		print (e)

def sqlite3_execute(sql, args = None):
	global conn
	data = None
	try:
		cur = conn.cursor()
		if args:
			cur.execute(sql, args)
		else:
			cur.execute(sql)
		data = cur.fetchall()
	except Exception as e:
	    print (e, "[SQL]:" + sql.strip())
	    conn.rollback()

	conn.commit()
	if data:
		return data
	return None

def sqlite3_close():
	global conn
	conn.close()

def unitest():
	sqlite3_init()

	sqlite3_execute("CREATE TABLE stocks (date text, trans text, symbol text, qty real, price real)")

	sqlite3_execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")
	sqlite3_execute("INSERT INTO stocks VALUES ('2006-03-28', 'BUY', 'IBM', 1000, 45.00)")
	sqlite3_execute("INSERT INTO stocks VALUES ('2006-04-05', 'BUY', 'MSFT', 1000, 72.00)")
	sqlite3_execute("INSERT INTO stocks VALUES ('2006-04-06', 'SELL', 'IBM', 500, 53.00)")

	assert 4 == sqlite3_execute("SELECT count(*) FROM stocks")[0][0]

	sqlite3_execute("DROP TABLE stocks")

	sqlite3_close()

if __name__ == '__main__':
	unitest()

