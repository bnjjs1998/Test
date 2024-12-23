from app import *
from warnings import catch_warnings

# Ici tous les outils liès à FLask
from flask import request, session, jsonify
from flask import render_template

from flask import jsonify
# j'importe le module Flask_pymongo
from flask_pymongo import PyMongo
from pymongo.synchronous.collection import Collection

# Les outils pour gérer les connexions
from login import login_manager

#ici c'est ma db de test
from model import *
# J'importe les variables de connexions à la DB
from configMongo import *

@app.route('/')
def index():
    return render_template('login.html')

@login_manager.user_loader
def load_user(user_id):
    for user in users:
        if user.id == int(user_id):
            return user
    return None

# Route pour la page de connexion
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        for user in users:
            if user.username == username and user.password == password:
                login_user(user)
                return redirect(url_for('dashboard'))
        return "Nom d'utilisateur ou mot de passe incorrect", 401

    return render_template('login.html')

# Route pour le tableau de bord (accessible uniquement après connexion)
@app.route('/dashboard')
@login_required
def dashboard():
    dashboard_message = f"Bienvenue {current_user.username} !"
    return render_template('index.html', dashboard_message=dashboard_message)


# Route pour se déconnecter
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


#Voici les routes test qui ne dépendent pas du login en accès public

@app.route('/collection', methods=['GET', 'POST'])
def collection():
    try:
        collection_choose = 'mydb'
        collections_mongo = mongo.db[collection_choose]
        documents = list(collections_mongo.find({}))
        return f"Voici la liste de mes collections {collection_choose}:{documents}:", 200
    except catch_warnings as e:
        return f"erreur, la collection choisi n'est pas connecté", 500
