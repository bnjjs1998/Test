from flask import jsonify, render_template

from app import app
from app import *
from configMongo import mongo
from route import *
#charger la page register

@app.route('/register_index')
def register_index():
    return render_template('register.html')


#la route qui permet de s'inscrire
@app.route('/insert_register', methods=['POST'])
def insert_register():
    collections_mongo = mongo.db["User"]

    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password_register')
    confirm_password = request.form.get('confirm_password')

    # Vérifier si les mots de passe correspondent
    if password != confirm_password:
        return jsonify({"message": "Les mots de passe ne correspondent pas"}), 400

    # Vérifier si tous les champs sont remplis
    if not all([email, username, password, confirm_password]):
        return jsonify(
            {
                "Status": 400,
                "Message": "Il manque certaines informations dans le formulaire"
            }
        ), 400

    # Vérifier si l'email ou le nom d'utilisateur existe déjà
    existing_user = collections_mongo.find_one({"$or": [{"email": email}, {"username": username}]})
    if existing_user:
        return jsonify(
            {
                "Status": 400,
                "Message": "Le mail ou le nom d'utilisateur existent déjà"
            }
        ), 400

    # Si l'email et le nom d'utilisateur sont uniques, insérer l'utilisateur
    user_register = {"email": email, "username": username, "password": password}
    collections_mongo.insert_one(user_register)

    return jsonify({"message": "Utilisateur enregistré avec succès"}), 201


