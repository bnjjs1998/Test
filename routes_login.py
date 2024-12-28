# app/routes_login.py
from bson import ObjectId
from flask import render_template, request, redirect, url_for, session, jsonify
from flask_login import login_required
from pymongo import ReturnDocument
from app import app, users_collection


@app.route("/")
def home():
    if "username" in session:
        return render_template('login.html')
    return "Vous n'êtes pas connecté. <a href='/login'>Connexion</a> ou <a href='/register'>Inscription</a>"


@login_required
@app.route("/dashboard", methods=['GET', 'POST'])
def dashboard():
    return render_template('index.html')


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Rechercher l'utilisateur dans la base de données
        user = users_collection.find_one({"username": username, "password": password})

        if user:
            # Stocker dans la session les informations nécessaires
            session["username"] = username
            session["user_id"] = str(user["_id"])  # Stocker l'ID de l'utilisateur
            session["email"] = user.get("email")  # Stocker l'email de l'utilisateur si disponible

            return redirect(url_for("dashboard"))
        return "Nom d'utilisateur ou mot de passe incorrect."
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    # je récupère les infos du formulaire
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        # Je vérifie les infos
        if users_collection.find_one({"username": username}):
            return "Nom d'utilisateur déjà pris."

        if users_collection.find_one({"email": email}):
            return "l'email est deja pris"
        # la requete qui me permet
        users_collection.insert_one({"username": username, "password": password})
        return redirect(url_for("login"))
    return render_template("register.html")


@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("home"))


@login_required
@app.route("/profile", methods=["GET"])
def profile():
    user_id = session["user_id"]
    if user_id is None:
        return redirect(url_for("login"))
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    if user:

        user["_id"] = str(user["_id"])
        return jsonify(user), 200
    else:
        return jsonify({"message": "User not found"}), 404


#un Counter de test par session
@app.route("/counter", methods=["POST"])
def counter():

    user_id = session["user_id"]
    if "user_id" not in session:
        return redirect(url_for("login"))

    updated_counter = users_collection.find_one_and_update(
        {"_id": ObjectId(user_id)},
        {"$inc": {"counter": 1}},
        upsert=True,  # Crée un document si aucun ne correspond
        return_document=ReturnDocument.AFTER  # Retourne le document après la mise à jour
    )
    # j'affiche un json avec le resultat de ma requete
    if updated_counter:
        return jsonify({
            "counter": updated_counter["counter"],
            "status": "success"
        })


