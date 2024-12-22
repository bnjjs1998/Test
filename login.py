from app import *
from app import app

# Clé secrète pour Flask (nécessaire pour gérer les sessions)
app.secret_key = "your_secret_key"

# Configuration du gestionnaire de connexion
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Page par défaut pour les utilisateurs non connectés

