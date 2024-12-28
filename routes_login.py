# app/routes_login.py
from flask import render_template, request, redirect, url_for, session, jsonify
from flask_login import login_required
from flask_pymongo import MongoClient
from bson import ObjectId

from pyexpat.errors import messages

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
        # la requête qui me permet
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


    # Vérifiez si l'utilisateur est connecté via la session
    if "user_id" not in session:
        return redirect(url_for("login"))

    # Récupérez les informations de l'utilisateur depuis la session
    user_id = session["user_id"]
    username = session["username"]
    email = session["email"]
    password = session["password"]


    try:
        # Convertissez l'ID de l'utilisateur en ObjectId pour interroger MongoDB
        if not ObjectId.is_valid(user_id):
            return jsonify({"message": "Invalid user ID format."}), 400

        # Récupérer les informations de l'utilisateur depuis la base de données si nécessaire
        user = users_collection.find_one({"_id": ObjectId(user_id)})

        if not user:
            return jsonify({"message": "User not found."}), 404


    # Retourner les informations sous forme de JSON
    return jsonify({
        "username": username,
        "email": email,
        "password": password,
        "message": "Profile loaded successfully."
    })
