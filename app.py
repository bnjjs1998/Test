from flask import Flask, request, render_template, redirect, url_for, session
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Remplacez par une clé sécurisée

# Connexion à MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client.mydb
users_collection = db["User"]


@app.route("/")
def home():
    if "username" in session:
        return f"Bienvenue, {session['username']}! <a href='/logout'>Déconnexion</a>"
    return "Vous n'êtes pas connecté. <a href='/login'>Connexion</a> ou <a href='/register'>Inscription</a>"


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = users_collection.find_one({"username": username, "password": password})
        if user:
            session["username"] = username
            return redirect(url_for("home"))
        return "Nom d'utilisateur ou mot de passe incorrect."
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if users_collection.find_one({"username": username}):
            return "Nom d'utilisateur déjà pris."

        users_collection.insert_one({"username": username, "password": password})
        return redirect(url_for("login"))
    return render_template("register.html")


@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
