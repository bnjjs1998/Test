#Le fichier se nomme config-mongo_DB.py

from app import *
from flask_pymongo import PyMongo

app.config["MONGO_URI"] = "mongodb://localhost:27017/mydb"
mongo = PyMongo(app)
collection_choose = 'login_user'
