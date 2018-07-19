import flask
from flask import Flask
from flask import *
from functools import wraps
import jwt
import datetime

app=Flask(__name__)
app.secret_key="mish"

users = {}
individual=[]
hobies=[]
achievements=[]
entries={"hobies":hobies,"achievements":achievements,"users":users}


def tokens(k):
    @wraps(k)
    def decorated(*args, **kwargs):
        token = request.args.get('token')

        if not token:
            return jsonify({'message' : 'you need to be logged in first'}), 403

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])


        except:
            return jsonify({'message' : 'invalid access'}), 403

        return k(*args, **kwargs)
    return decorated

@app.route('/api/v1/home',methods=['POST','GET'])
def home():
    return jsonify({"message":"welcome to my diary"})

    
@app.route('/api/v1/login', methods=['POST','GET'])
def login():
    username=request.get_json()["username"]
    password=request.get_json()["password"]
    if username in users:
        if password==users[username]["password"]:
            session["logged_in"]=True
            token=jwt.encode({'username':username,'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)},app.config['SECRET_KEY'])
            return jsonify({"message":"succesfuly logged in",'token':token.decode ('UTF-8')})
                    
        else:
            return jsonify({"message": "your password is wrong"})
    else:
        return jsonify({"message": "check your username"})
   

@app.route('/api/v1/register', methods=['POST','GET'])
def register():
    name= request.get_json()['name']
    email= request.get_json()['email']
    password= request.get_json()['password']
    username=request.get_json()['username']
    users.update({username:{"name": name,"email": email,"password": password}})
    return jsonify({"name": name},{"username":username})

@app.route('/api/v1/hobby', methods=['POST','GET'])
@tokens
def hobby():
    hobby=request.get_json()["hobby"]
    hobies.append(hobby)
    return jsonify(hobby)

@app.route('/api/v1/view_hobbies',methods=['GET','POST'])
@tokens
def view_hobbies():
    return jsonify(hobies)

@app.route('/api/v1/achievement', methods=['POST','GET'])
@tokens
def achievement():
    achievement=request.get_json()["achievement"]
    achievements.append(achievement)
    return jsonify(achievement)

@app.route('/api/v1/view_achievement',methods=['POST','GET'])
@tokens
def view_achievement():
    return jsonify(achievements)

@app.route('/api/v1/all_entries',methods=['POST','GET'])
@tokens
def all_entries():
    return jsonify(entries)

@app.route('/api/v1/all_users', methods=['POST','GET'])
@tokens
def all_users():
    return jsonify(users) 

@app.route('/api/v1/delete_achievement/<int:ID>',methods=['DELETE'])
@tokens
def delete_achievement(ID):
    del achievements[ID-1]
    return jsonify({ 'message': 'deleted'})

@app.route("/api/v1/update_achievement/<int:ID>", methods=['PUT'])
@tokens
def update_entry(ID):
    update=request.get_json()['update']
    achievements[ID-1]=update
    return jsonify({"message":"updated"})

@app.route("/api/v1/update_hobby/<int:ID>", methods=['PUT'])
@tokens
def update_hobby(ID):
    update_hobby=request.get_json()['update_hobby']
    hobies[ID-1]=update_hobby
    return jsonify({"message":"hobby updated"})

@app.route('/api/v1/delete_hobby/<int:ID>',methods=['DELETE'])
@tokens
def delete_hobby(ID):
    del hobies[ID-1]
    return jsonify({ 'message': ' hobby deleted'})

    

if __name__ =="__main__":
    app.run(debug=True)
