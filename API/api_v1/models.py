import psycopg2

connection= psycopg2.connect(host ='localhost',user='postgres',password='milamish8',dbname='diary')

def table():
	connection= psycopg2.connect(host ='localhost',user='postgres',password='milamish8',dbname='diary')
	with connection.cursor() as cursor:
		cursor.execute("CREATE TABLE IF NOT EXISTS users (user_id serial PRIMARY KEY,\
			name VARCHAR(100) NOT NULL,\
			username VARCHAR(100) NOT NULL,\
			email_adress VARCHAR(50) NOT NULL,\
			password VARCHAR(100) NOT NULL,\
			repeat_password VARCHAR(100) NOT NULL,\
			reg_date timestamp DEFAULT CURRENT_TIMESTAMP);")
		cursor.execute("CREATE TABLE IF NOT EXISTS entries(entry_id serial PRIMARY KEY, \
			title VARCHAR(100) NOT NULL, \
			entry_comment VARCHAR(100) NOT NULL,\
			entry_date timestamp DEFAULT CURRENT_TIMESTAMP,\
			user_id INT);")

		connection.commit()