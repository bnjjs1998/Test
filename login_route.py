from bson import ObjectId
from flask import url_for, render_template

from app import *
from app import app
from configMongo import mongo
from route import *

# Clé secrète pour Flask (nécessaire pour gérer les sessions)
app.secret_key = "BPCE_SILoginvote"

# Configuration du gestionnaire de connexion
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    user_data = mongo.db.User.find_one({"_id": ObjectId(user_id)})
    if user_data:
        # Créez un objet utilisateur à partir des données de MongoDB
        return user_data
    return None


# Route pour la page de connexion
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user_login = mongo.db.User.find_one({"username": username})
        return "Nom d'utilisateur ou mot de passe incorrect", 401

    return render_template('login.html')

# Route pour se déconnecter
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
