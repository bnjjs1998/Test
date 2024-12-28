from flask import request, url_for, render_template, redirect
from app import app, users_collection

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
