from flask import Flask, request, Blueprint, jsonify
from functools import wraps
import datetime
import jwt
import pdb
import psycopg2
from __init__ import *

from models import *

entries = Blueprint('entries', __name__)
'''args allows one to pass variable number of arguments while kwargs allows one to pass key arguments'''
def tokens(k):
    @wraps(k)
    def decorators(*args, **kwargs):
        token = request.headers.get('x-access-token')
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
	@entries.route('/api/v2/entries',methods=['POST'])
	@tokens
	def add_entry():
		title= request.get_json()['title'].strip()
		entry_comment=request.get_json()['entry_comment'].strip()
		data = jwt.decode(request.headers.get('x-access-token'), app.config['SECRET_KEY'])
		user_id=data['user_id']

		if not title:
			return jsonify({"message":"enter title"})
		if not entry_comment:
			return jsonify({"message":"enter entry comment"})
				
		try:
			with connection.cursor() as cursor:
				sql_entry="INSERT INTO entries(title,entry_comment,user_id) VALUES(%s,%s,%s);"
				try:
					cursor.execute(sql_entry,(title,entry_comment,user_id))
				except:
					return jsonify({"message":"unable to add entry"}), 500
			connection.commit()
		finally:
			return jsonify({"title":title,"entry_comment":entry_comment,"user_id":user_id}), 200
	

	@entries.route('/api/v2/entries/<int:entry_id>',methods=['POST','GET'])
	@tokens
	def view_a_single_entry(entry_id):
		data = jwt.decode(request.headers.get('x-access-token'), app.config['SECRET_KEY'])
		user_id=data['user_id']
		
		try:
			
			with connection.cursor() as cursor:
				sql_view="SELECT * FROM entries WHERE entries.entry_id ="+str(entry_id)+";"
				try:
					cursor.execute(sql_view)
					result=cursor.fetchone()
					if result is None:
						return jsonify({"message":"entry_id does not exist"}), 404
					else:
						return jsonify({"result":result})
				except:
					return jsonify({"message": "unable to fetch entry"}), 500
					
			connection.commit()
		finally:
			pass

	@entries.route('/api/v2/entries',methods=['GET'])
	@tokens
	def view_all_entries():
		data = jwt.decode(request.headers.get('x-access-token'), app.config['SECRET_KEY'])
		user_id=data['user_id']
		
		try:
			with connection.cursor() as cursor:
				sql_one="SELECT * FROM entries WHERE user_id = '"+str(user_id)+"';"
				try:
					cursor.execute(sql_one)
					result=cursor.fetchall()
					if len(result)==0:
						return jsonify({"message":"no entries found"})
					else:
						return jsonify ({"results":result})
				except:
					return jsonify({"message":"entry not found"}), 500
			connection.commit()
		finally:
			pass


	
	@entries.route('/api/v2/entries/<int:entry_id>',methods=['PUT','POST'])
	@tokens
	def modify_an_entry(entry_id):
		data = jwt.decode(request.headers.get('x-access-token'), app.config['SECRET_KEY'])
		user_id=data['user_id']
		title=request.get_json()['title'].strip()
		entry_comment=request.get_json()['entry_comment'].strip()
		get_date=str(datetime.datetime.today())
		
		try:
			with connection.cursor() as cursor:
				cursor.execute("SELECT * FROM entries WHERE entries.entry_id='"+str(entry_id)+"' and entries.user_id='"+str(user_id)+"'")
				result=cursor.fetchone()
				if result is not None:
					sql_update="update entries SET title='"+title+"',entry_comment='"+entry_comment+"' where entry_id='"+str(entry_id)+"';"
					try:
						cursor.execute(sql_update)
						connection.commit()
						return jsonify({"message":"succesfully modified"})
					except:
						return jsonify({"message":"unable to update"}), 500
		except:
			return jsonify({"message":"entry does not exist"})

	@entries.route('/api/v2/entries/<int:entry_id>',methods=['DELETE'])
	@tokens
	def delete_entry(entry_id):
		data = jwt.decode(request.headers.get('x-access-token'), app.config['SECRET_KEY'])
		user_id=data['user_id']
		
		try:
			with connection.cursor() as cursor:
				sql_del="DELETE FROM entries WHERE entries.entry_id= '"+str(entry_id)+"' and entries.user_id='"+str((user_id))+"';"
				try:
					cursor.execute("SELECT * FROM entries WHERE entries.entry_id = '"+str(entry_id)+"' and entries.user_id='"+str((user_id))+"'")
					result=cursor.fetchone()
					if result is None:
						return jsonify({"message":"entry does not exist"}), 404
					else:
						cursor.execute(sql_del)
						
				except:
					return jsonify({"message": "unable to delete entry"}), 500
			connection.commit()
		finally:
			return jsonify({"message": "entry succesfully deleted"})
		