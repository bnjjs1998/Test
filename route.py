from warnings import catch_warnings

from flask import request, session
from flask import render_template
from pymongo.synchronous.collection import Collection

from app  import app
from app import *
from login import login_manager
from model import *
# J'importe les variables de connexions à la DB
from configMongo import *
# j'importe le module Flask_pymongo
from flask_pymongo import PyMongo

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


@app.route('/collection', methods=['GET', 'POST'])
def collection():
    try:
        Collection_choose ='mydb'
        collection = mongo.db[Collection_choose]

        print('')
    except Exception as e:
        print(f"Errreur de connexion à Mongo",e)
