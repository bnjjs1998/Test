#Le fichier se nomme configMongo.py
from app import *
from flask_pymongo import PyMongo

app.config["MONGO_URI"] = "mongodb://localhost:27017/mydb"
mongo = PyMongo(app)



