from bson import ObjectId
from flask import request, url_for, render_template, redirect, session, jsonify
from flask_login import login_required
from pymongo import ReturnDocument

from app import app, users_collection


@login_required
@app.route('/Questions_Post', methods=[ 'POST'])
def questions():
    # je vérifie s'il y a bien une session active
     User_id = session.get('User_id')
     if User_id is None:
         # si aucune sessions n'est active, je redirige vers la page de login
         return redirect(url_for('login'))
     question = request.form['questions']
     question =str(question)

     if not question:
         return jsonify({
             "message": "No questions entered",
             "status": 400,
         })
     question_post = users_collection.find_one_and_update(
         {"_id": ObjectId(User_id)},
         {"$inc": {"questions": question }},
         upsert = True,
         return_document = ReturnDocument.AFTER
     )
     return jsonify({
         "status": 200,
     })

