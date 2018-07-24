from flask import *
from functools import wraps
import datetime
import jwt
# db_diary
from models import *
import psycopg2
from passlib.hash import pbkdf2_sha256 as sha256


app=Flask(__name__)
app.config ['SECRET_KEY']='mish'
'''
class passWord():
    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)
    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)'''

def tokens(k):
    @wraps(k)
    def tokenize(*tok, **toks):
        token = request.args.get('token')

        if not token:
            return jsonify({'message' : 'Token is missing'})

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])


        except:
            return jsonify({'message' : 'Token is invalid'})

        return k(*tok, **toks)
    return tokenize

@app.route('/api/v2/home',methods=['POST','GET'])
def home():
    return jsonify({"message":"welcome to my diary"})

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

@app.route('/api/v2/login',methods=['POST','GET'])
def login():
	username=request.get_json()['username']
	password= request.get_json()['password']
	
	try:
		connection = psycopg2.connect(host ='localhost',user='postgres',password='milamish8',dbname='diary')
		with connection.cursor() as cursor:
			sql_log="SELECT * FROM  users WHERE Username LIKE '"+username+"' and Password LIKE '"+password+"'"
			try:
				cursor.execute(sql_log)
				result=cursor.fetchone()
				if result is None :
					return jsonify({"message":"your password or username is wrong"})
				else:
					token=jwt.encode({'username':username,'user_id':result[0],'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)},app.config['SECRET_KEY'])
					return jsonify({"message":"succesfuly logged in",'token':token.decode ('UTF-8')})
			except:
				return jsonify({"message":"check your login details"})
		connection.commit()
	finally:
		connection.close()

@app.route('/api/v2/add_entry',methods=['POST','GET'])
@tokens
def add_entry():
	hobby= request.get_json()['hobby']
	milestone=request.get_json()['milestone']
	achievement=request.get_json()['achievement']
	todo=request.get_json()['todo']
	data = jwt.decode(request.args.get('token'), app.config['SECRET_KEY'])
	user_id=data['user_id']
	connection = psycopg2.connect(host ='localhost',user='postgres',password='milamish8',dbname='diary')
	try:
		
		with connection.cursor() as cursor:
			#sql_entry= "INSERT INTO entries(hobby,milestone,achievement,todo,user_id) VALUES('"+hobby+"', '"+milestone+"', '"+achievement+"', '"+todo+"', '"+str(user_id)+"');"
			sql_entry= "INSERT INTO entries(hobby,milestone,achievement,todo,user_id) VALUES(%s,%s,%s,%s,%s);"
			try:
				cursor.execute(sql_entry,(hobby,milestone,achievement,todo,user_id))
			except:
				return jsonify({"message":"oops!"})
		connection.commit()
	finally:
		connection.close()
	return jsonify({"hobby":hobby,"milestone":milestone,"achievement":achievement,"todo":todo,"user_id":user_id})
	

@app.route('/api/v2/view_a_single_entry/<int:entry_id>',methods=['POST','GET'])
@tokens
def view_a_single_entry(entry_id):
	connection=psycopg2.connect(host='localhost',user='postgres',password='milamish8',dbname='diary')
	
	try:
		
		with connection.cursor() as cursor:
			sql_view="SELECT * FROM entries WHERE entries.entry_id ="+str(entry_id)+";"
			try:
				cursor.execute(sql_view)
				result=cursor.fetchone()
				return jsonify(result)
				for row in result:
					row=cursor.fetchall()
					return jsonify(str(row[0]) + "\n\n" + "\t\t" + row[1] +"\n\n" + row[2] + "\n\n" + row[3])
			except:
				return jsonify({"message": "unable to fetch entry"})
				
		connection.commit()
	finally:
		connection.close()

@app.route('/api/v2/entries_from_individual_user/<int:user_id>',methods=['GET'])
@tokens
def entries_for_single_user(user_id):
	connection=psycopg2.connect(host='localhost',user='postgres',password='milamish8',dbname='diary')
	try:
		with connection.cursor() as cursor:
			sql_one="SELECT * FROM entries WHERE entries.user_id='"+str(user_id)+"';"
			try:
				cursor.execute(sql_one)
				result=cursor.fetchall()
				return jsonify(result)
				for row in result:
					row=cusor,fetchall()
			except:
				return jsonify({"message":"not found"})
		connection.commit()
	finally:
		connection.close()

@app.route('/api/v2/view_all_entries',methods=['POST','GET'])
#@tokens
def view_all_entries():
		connection=psycopg2.connect(host='localhost',user='postgres',password='milamish8',dbname='diary')
		try:
			with connection.cursor() as cursor:
				sql_view_entries="SELECT * FROM entries";
				try:
					cursor.execute(sql_view_entries)
					result= cursor.fetchall()
					return jsonify(result)
					for row in result:
						row=cursor.fetchall()
				except:
					return jsonify({"message":"unable to fetch data"})
			connection.commit()
		finally:
			connection.close()  


@app.route('/api/v2/modify_an_entry/<int:entry_id>',methods=['PUT','POST'])
#@tokens
def modify_an_entry(entry_id):
	connection=psycopg2.connect(host='localhost',user='postgres',password='milamish8',dbname='diary')
	hobby=request.get_json()['hobby']
	milestone=request.get_json()['milestone']
	achievement=request.get_json()['achievement']
	todo=request.get_json()['todo']
	try:
		with connection.cursor() as cursor:
			sql_update="update entries SET hobby='"+hobby+"',milestone='"+milestone+"',achievement = '"+achievement+"',todo = '"+todo+"' where entry_id='"+str(entry_id)+"';"
			try:
				cursor.execute(sql_update)
				connection.commit()
				return jsonify({"message":"succesfully modified"})
			except:
				return jsonify({"message":"unable to update"})
	finally:
		connection.close()

@app.route('/api/v2/delete_entry/<int:entry_id>',methods=['DELETE'])
#@tokens
def delete_entry(entry_id):
	connection=psycopg2.connect(host='localhost',user='postgres',password='milamish8',dbname='diary')
	try:
		with connection.cursor() as cursor:
			sql_del="DELETE FROM entries WHERE entries.entry_id= "+str(entry_id)+" and entries.entry_id='"+str((entry_id))+"';"
			try:
				cursor.execute("SELECT * FROM entries WHERE entries.entry_id = "+str(entry_id)+" and entries.entry_id='"+str((entry_id))+"'")
				result=cursor.fetchone()
				if result is None:
					return jsonify({"message":"entry does not exist"})
				else:
					cursor.execute(sql_del)
			except:
				return jsonify({"message": "unable to delete entry"})
		connection.commit()
	finally:
		connection.close()
	return jsonify({"message": "entry succesfully deleted"})

  

@app.route('/api/v2/logout',methods=['POST','GET'])
def logout():
    return jsonify({"message":"you have been logged out"})


if __name__=="__main__":
	table()
	app.run(debug=True)