from flask import Flask, jsonify, request, Blueprint
import psycopg2
import jwt
import datetime
from __init__ import *

users = Blueprint('users', __name__)

connection = psycopg2.connect(host='localhost',user='postgres',password='milamish8',dbname='diary')

def tokens(k):
    @wraps(k)
    def decorators(*tok, **toks):
        token = request.args.get('token')

        if not token:
            return jsonify({'message' : 'Token is missing'})

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])


        except:
            return jsonify({'message' : 'Token is invalid'})

        return k(*tok, **toks)
    return decorators


class Register():
	@app.route('/api/v2/register',methods=['POST','GET'])
	def  register():
		name= request.get_json()['name']
		email_adress= request.get_json()['email_adress']
		username=request.get_json()['username']
		password=request.get_json()['password']
		repeat_password=request.get_json()['repeat_password']
		'''password= passWord.generate_hash(['password'])
		repeat_password= passWord.generate_hash(['repeat_password'])'''
		
		if password!=repeat_password:
			return jsonify({"message":"password do not match"})
		try:
			connection = psycopg2.connect(host='localhost',user='postgres',password='milamish8',dbname='diary')
			with connection.cursor() as cursor:
				sql="INSERT INTO users(name,email_adress,password,username,repeat_password) VALUES('"+name+"','"+email_adress+"','"+password+"','"+username+"','"+repeat_password+"');"
				try:
					cursor.execute("SELECT * FROM  users WHERE username='"+username+"';");
					if cursor.fetchone() is not None:
						return jsonify({"message":"username taken"})
					else:
						cursor.execute(sql)


				except:
					return jsonify({"message":"oops!"})
			connection.commit()
		finally:
			connection.close()
		return jsonify({"message":"registered"})

class Login():
	@users.route('/api/v2/login',methods=['POST','GET'])
	def login():
		username=request.get_json()['username']
		password= request.get_json()['password']
		connection = psycopg2.connect(host ='localhost',user='postgres',password='milamish8',dbname='diary')
		with connection.cursor() as cursor:
			sql_log="SELECT * FROM  users WHERE Username LIKE '"+username+"' and Password LIKE '"+password+"'"
			cursor.execute(sql_log)
			result=cursor.fetchone()
			if result is None :
				return jsonify({"message":"your password or username is wrong"})
			else:
				token=jwt.encode({'username':username,'user_id':result[0],'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)},app.config['SECRET_KEY'])
				return jsonify({"message":"succesfuly logged in",'token':token.decode ('UTF-8')})
				connection.commit()
				return jsonify({"message":"check your login details"})
				connection.close()


@users.route('/api/v2/logout',methods=['POST','GET'])
def logout():
    return jsonify({"message":"you have been logged out"})
