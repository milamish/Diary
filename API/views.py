from flask import Flask, jsonify, request, Blueprint

main = Blueprint('main', __name__)

@main.route('/api/v2/home',methods=['POST','GET'])
def home():
	return jsonify({"message":"welcome to my diary"})