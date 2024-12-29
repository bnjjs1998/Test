from flask import request, url_for, render_template, redirect, session, jsonify
from flask_login import login_required

from app import app, users_collection


@login_required
@app.route('/Questions_Post', methods=[ 'POST'])
def questions():
    # je vérifie s'il y a bien une session active
     User_id = session.get('User_id')
     if User_id is None:
         # si aucune sessions n'est active, je redirige vers la page de login
         return redirect(url_for('login'))

     questions = request.form['questions']
     if not questions:
         return jsonify({
             "message": "No questions entered",
             "status": 400,
         })
     return jsonify({

     })
