from flask import *
import psycopg2

def table():
	connection= psycopg2.connect(host ='localhost',user='postgres',password='milamish8',dbname='diary')
	cursor.execute(" CREATE TABLE users (user_ID int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY, \
		name  NOT NULL VARCHAR(100),\
	 	username NOT NULL VARCHAR(100),\
	 	email_adress NOT NULL VARCHAR(50),\
	 	password NOT NULL VARCHAR(50),\
	 	repeat_password NOT NULL VARCHAR(50);")