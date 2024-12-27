from flask import jsonify

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
    try:
        #je déclare la collection
        collections_mongo = mongo.db["User"]

        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            return jsonify(
                {"message": "Les mots de passe sont corrects"}
            ), 200

        if not all([email, username, password, confirm_password]):
            return jsonify(
                {
                    "Status": "error",
                    "Message": "il manque certaines infos dans le formulaire ",
                    "Serveur": 400
                }
            ), 400

        user_register = {"email": email, "username": username, "password": password}
        documents_register = collections_mongo.insert_one(user_register)
        
        
        #Verifier si l'utilisateur existe déjà 
        
       

        return jsonify(
            {
                "State": "success",
                "message": f"{username} est correctement enregistré",
                "status": 200
            }
        ), 200
        
    except BadRequest as e:
        return jsonify(
            {
                "Status": "error",
                "Message": str(e)
            }
        ), 400


