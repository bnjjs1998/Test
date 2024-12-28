from bson import ObjectId
from flask import url_for, redirect, session, jsonify
from pymongo import ReturnDocument
from app import users_collection, app


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
