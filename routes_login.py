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
# La partie register
from register_route import *
#un Counter de test par session
from counter_route import *

