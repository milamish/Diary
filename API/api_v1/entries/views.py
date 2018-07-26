from flask import Flask, request, Blueprint, jsonify
from functools import wraps
import datetime
import jwt
import psycopg2
from __init__ import *

entries = Blueprint('entries', __name__)
'''args allows one to pass variable number of arguments while kwargs allows one to pass key arguments'''
def tokens(k):
    @wraps(k)
    def decorators(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'message' : 'Token is required for access'})
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'message' : 'Token is invalid'})
        return k(*args, **kwargs)
    return decorators
'''this class has functions which allows a user to make enties i.e, add, delete , modify and view'''
class Entries():
	@entries.route('/api/v2/add_entry',methods=['POST','GET'])
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
				sql_entry="INSERT INTO entries(hobby,milestone,achievement,todo,user_id) VALUES(%s,%s,%s,%s,%s);"
				try:
					cursor.execute(sql_entry,(hobby,milestone,achievement,todo,user_id))
				except:
					return jsonify({"message":"unable to add entry"}), 500
			connection.commit()
		finally:
			connection.close()
		return jsonify({"hobby":hobby,"milestone":milestone,"achievement":achievement,"todo":todo,"user_id":user_id}), 200
	

	@entries.route('/api/v2/view_a_single_entry/<int:entry_id>',methods=['POST','GET'])
	@tokens
	def view_a_single_entry(entry_id):
		data = jwt.decode(request.args.get('token'), app.config['SECRET_KEY'])
		user_id=data['user_id']
		connection=psycopg2.connect(host='localhost',user='postgres',password='milamish8',dbname='diary')
		
		try:
			
			with connection.cursor() as cursor:
				sql_view="SELECT * FROM entries WHERE entries.entry_id ="+str(entry_id)+";"
				try:
					cursor.execute(sql_view)
					result=cursor.fetchone()
					if result is None:
						return jsonify({"message":"entry_id does not exist"}), 404
					else:
						return jsonify(result)
				except:
					return jsonify({"message": "unable to fetch entry"}), 500
					
			connection.commit()
		finally:
			connection.close()

	@entries.route('/api/v2/entries_from_individual_user',methods=['GET'])
	@tokens
	def entries_for_single_user():
		data = jwt.decode(request.args.get('token'), app.config['SECRET_KEY'])
		user_id=data['user_id']
		connection=psycopg2.connect(host='localhost',user='postgres',password='milamish8',dbname='diary')
		try:
			with connection.cursor() as cursor:
				sql_one="SELECT * FROM entries WHERE user_id ='"+str(user_id)+"';"
				try:
					cursor.execute(sql_one)
					result=cursor.fetchall()
					return jsonify(result)
				except:
					return jsonify({"message":"entry not found"}), 500
			connection.commit()
		finally:
			connection.close()

	@entries.route('/api/v2/view_all_entries',methods=['POST','GET'])
	@tokens
	def view_all_entries():
			connection=psycopg2.connect(host='localhost',user='postgres',password='milamish8',dbname='diary')
			try:
				with connection.cursor() as cursor:
					sql_view_entries="SELECT * FROM entries";
					try:
						cursor.execute(sql_view_entries)
						result= cursor.fetchall()
						return jsonify(result)
					except:
						return jsonify({"message":"unable to fetch data"}), 500
				connection.commit()
			finally:
				connection.close()  


	@entries.route('/api/v2/modify_an_entry/<int:entry_id>',methods=['PUT','POST'])
	@tokens
	def modify_an_entry(entry_id):
		data = jwt.decode(request.args.get('token'), app.config['SECRET_KEY'])
		user_id=data['user_id']
		hobby=request.get_json()['hobby']
		milestone=request.get_json()['milestone']
		achievement=request.get_json()['achievement']
		todo=request.get_json()['todo']
		get_date=str(datetime.datetime.today())
		connection=psycopg2.connect(host='localhost',user='postgres',password='milamish8',dbname='diary')

		try:
			with connection.cursor() as cursor:
				cursor.execute("SELECT * FROM entries WHERE entries.entry_id='"+str(entry_id)+"' and entries.user_id='"+str(user_id)+"'")
				result=cursor.fetchone()
				if result is not None:
					sql_update="update entries SET hobby='"+hobby+"',milestone='"+milestone+"',achievement = '"+achievement+"',todo = '"+todo+"' where entry_id='"+str(entry_id)+"';"
					try:
						cursor.execute(sql_update)
						connection.commit()
						return jsonify({"message":"succesfully modified"})
					except:
						return jsonify({"message":"unable to update"}), 500
		finally:
			connection.close()
		return jsonify({"message":"entry does not exist"})

	@entries.route('/api/v2/delete_entry/<int:entry_id>',methods=['DELETE'])
	@tokens
	def delete_entry(entry_id):
		data = jwt.decode(request.args.get('token'), app.config['SECRET_KEY'])
		user_id=data['user_id']
		connection=psycopg2.connect(host='localhost',user='postgres',password='milamish8',dbname='diary')
		try:
			with connection.cursor() as cursor:
				sql_del="DELETE FROM entries WHERE entries.entry_id= "+str(entry_id)+" and entries.entry_id='"+str((entry_id))+"';"
				try:
					cursor.execute("SELECT * FROM entries WHERE entries.entry_id = "+str(entry_id)+" and entries.entry_id='"+str((entry_id))+"'")
					result=cursor.fetchone()
					if result is None:
						return jsonify({"message":"entry does not exist"}), 404
					else:
						cursor.execute(sql_del)
						return jsonify({"message": "entry succesfully deleted"})
				except:
					return jsonify({"message": "unable to delete entry"}), 500
			connection.commit()
		finally:
			connection.close()
		