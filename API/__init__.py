from flask import Flask, request, jsonify, Blueprint

from users.views import users
from entries.views import entries
from views import main

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mish'

app.register_blueprint(users)
app.register_blueprint(entries)
app.register_blueprint(main)