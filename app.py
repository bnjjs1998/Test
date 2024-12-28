from flask import Flask
from pymongo import MongoClient
from flask_session import Session

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Remplacez par une clé sécurisée

# Configuration pour utiliser MongoDB pour les sessions
app.config['SESSION_TYPE'] = 'mongodb'
app.config['SESSION_MONGODB'] = MongoClient("mongodb://localhost:27017/")
app.config['SESSION_MONGODB_DB'] = 'mydb'
app.config['SESSION_MONGODB_COLLECTION'] = 'sessions'

# Connexion à MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client.mydb
users_collection = db["User"]

# Initialisation de la session
Session(app)

from routes_login import *  # Assurez-vous que routes est importé après l'initialisation de l'app
