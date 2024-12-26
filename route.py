from flask_login import login_required
from pyexpat.errors import messages
from werkzeug.exceptions import BadRequest
from app import app
from app import *
from flask import request, session, jsonify
from flask import render_template
from flask import jsonify
from flask_pymongo import PyMongo
from pymongo.synchronous.collection import Collection
from register_route import *
from login_route import login_manager
from model import *
from configMongo import *


@app.route('/')
def index():
    return render_template('login.html')

from login_route import *
# Route pour le tableau de bord (accessible uniquement après connexion)
@app.route('/dashboard')
@login_required
def dashboard():
    dashboard_message = f"Bienvenue {current_user.username} !"
    return render_template('index.html', dashboard_message=dashboard_message)

#Voici les routes test qui ne dépendent pas du login en accès public
@app.route('/get_collection', methods=['GET'])
def collection():
    try:
        collection_choose = 'mydb'
        collections_mongo = mongo.db[collection_choose]
        documents = list(collections_mongo.find({}))
        return f"Voici la liste de mes collections {collection_choose}:{documents}:", 200
    except BadRequest as e:
        return f"erreur, la collection choisi n'est pas connecté", 500

