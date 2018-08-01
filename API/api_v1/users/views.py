from flask import Flask, jsonify, request, Blueprint
import psycopg2
import jwt
import datetime
import re
import hashlib

from models import *
from __init__ import *

users = Blueprint('users', __name__)



def tokens(k):
    @wraps(k)
    def decorators(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'message' : 'Token is missing'})
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'message' : 'Token is invalid'})
        return k(*args, **kwargs)
    return decorators

		
def pwhash(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_pwhash(password, hash):
    if pwhash(password)==hash:
        return True

    return False


'''this class has functions which allows users to register and login after registration, a registered user has a token generated for them at login'''
class Users():
	@users.route('/api/v2/auth/signup',methods=['POST'])
	def  register():
		name= request.get_json()['name'].strip()
		email_address= request.get_json()['email_address'].strip()
		username=request.get_json()['username'].strip()
		password=request.get_json()['password'].strip()
		repeat_password=request.get_json()['repeat_password'].strip()
		phash=pwhash(password)

		if not name:
			return jsonify({"message":"you must provide a name"})
		if not username:
			return jsonify({"message":"you must provide a username"})
		if len(username) < 5 or len(username) > 22:
			return jsonify({"message":"username must be between 5 and 22 characters"})

		if not password:
			return jsonify({"message":"you must provide a password"})
			
		if password != repeat_password:
			return jsonify({"message":"password do not match"})

		if len(password) < 9 or len(password) > 20:
			return jsonify({"message":"password must be between 9 and 20 characters"})

		if not re.match('\d.*[A-Z]|[A-Z].*\d', password):
			return jsonify({"message":"password must contain a capital letter and a number"})

		if not email_adress:
			return jsonify({"message":"you must provide an email"})

		if not re.match("[^@]+@[^@]+\.[^@]+", email_address):
			return jsonify({"message":"email address not valid"})
		try:
			with connection.cursor() as cursor:
				sql="INSERT INTO users(name,email_address,password,username,repeat_password) VALUES\
				('"+name+"','"+email_address+"','"+str(phash)+"','"+username+"','"+str(phash)+"');"
				cursor.execute("SELECT * FROM  users WHERE username='"+username+"';");
				if cursor.fetchone() is not None:
					return jsonify({"message":"username taken"}), 409
				else:
					cursor.execute(sql)
		except:
			return jsonify({"message":"unable to register!"}), 500
		connection.commit()
		return jsonify({"name":name, "email_adress":email_address, "username":username})
		

	@users.route('/api/v2/auth/login',methods=['POST'])
	def login():
		username=request.get_json()['username'].strip()
		password= request.get_json()['password'].strip()
		
		if not username:
			return jsonify({"message":"please enter a username"})
		if not password:
			return jsonify({"message":"please enter a password"})
		with connection.cursor() as cursor:
			sql_log="SELECT * FROM  users WHERE username = '"+username+"'"
			cursor.execute(sql_log)
			result=cursor.fetchone()
			if result is None :
				return jsonify({"message":"your username is wrong"})
			else:
			
				if check_pwhash(password, result[4]):
					token=jwt.encode({'username':username,'user_id':result[0],'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)},app.config['SECRET_KEY'])
					return jsonify({"message":"succesfuly logged in",'token':token.decode ('UTF-8')})
				else:
					return jsonify({'message':'invalid password'})
		connection.commit()
		return jsonify({"message":"check your login details"})


@users.route('/api/v2/logout',methods=['POST','GET'])
def logout():
	
	with connection.cursor() as cursor:
		sql_log="SELECT * FROM  users WHERE Username LIKE '"+username+"' and Password LIKE '"+password+"'"
		cursor.execute(sql_log)
		result = cursor.fetchone()
		return jsonify({"message":"you have been logged out"})
