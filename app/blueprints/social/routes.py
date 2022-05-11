from .import bp as social
from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user
from app.models import Post

# @social.route('/add_pokemon/<int:id>')
# @login_required
# def add_pokemon(id):


# @social.route('/remove_pokemon/<int:id>')
# @login_required
# def remove_pokemon(id):

