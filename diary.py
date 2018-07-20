from flask import *

app=Flask(__name__)
app.secret_key="mish"

users = {}
entries=[]

@app.route('/api/v1/home',methods=['POST','GET'])
def home():
    return jsonify({"message":"welcome to my diary"})

@app.route('/api/v1/register', methods=['POST','GET'])
def register():
    name= request.get_json()['name']
    email= request.get_json()['email']
    password= request.get_json()['password']
    username=request.get_json()['username']
    users.update({username:{"name": name,"email": email,"password": password}})
    return jsonify({"name": name},{"username":username})

    
@app.route('/api/v1/login', methods=['POST','GET'])
def login():
    username=request.get_json()["username"]
    password=request.get_json()["password"]
    if username in users:
        if password==users[username]["password"]:
            session["logged_in"]=True
            return jsonify({"message":"succesfuly logged in"})
        else:
            return jsonify({"message": "your password is wrong"})
    else:
        return jsonify({"message": "check your username"})

@app.route('/api/v1/entry',methods=['POST','GET'])
def entry():
    entry=request.get_json()["entry"]
    entries.append(entry)
    return jsonify(entries)

@app.route('/api/v1/fetch_entries',methods=['POST','GET'])
def fetch_entries():
    return jsonify(entries)


@app.route('/api/v1/update_entry/<int:ID>', methods=['PUT'])
def update_entry(ID):
    update_entry=request.get_json()['update_entry']
    entries[ID-1]=update_entry
    return jsonify({"message":"entry updated"})

@app.route('/api/v1/delete_entry/<int:ID>',methods=['DELETE'])
def delete_entry(ID):
    del entries[ID-1]
    return jsonify({ 'message': ' entry deleted'})

@app.route('/api/v1/individual_entry/<int:ID>',methods=['GET'])
def individual_entry(ID):
    return jsonify(entries[ID-1])

    

if __name__ =="__main__":
    app.run(debug=True)
