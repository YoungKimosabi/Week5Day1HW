from flask import render_template, request, flash, redirect, url_for
import requests
from .forms import PokedexForm, LoginForm, RegisterForm
from app import app
from .models import User
from flask_login import current_user, logout_user, login_user, login_required

@app.route('/')
@login_required
def index():

    return render_template('index.html.j2')

@app.route('/pokedex', methods=['GET','POST'])
@login_required
def pokedex():
    
    form = PokedexForm()
    if request.method=='POST' and form.validate_on_submit():
        poke_name = form.pokename.data
        url = f'https://pokeapi.co/api/v2/pokemon/{poke_name}'
        response = requests.get(url)
        
        if not response.ok:
            flash('We had an error loading your pokemon, it either doesnt exist or you cant spell', 'warning')
            return render_template('pokedex.html.j2', form=form)
        
        
        res = response.json()
        poke_dict={
                
                "name":res['forms'][0]['name'] ,
                "ability": res['abilities'][0]['ability']['name'],
                "base_xp": res['base_experience'],
                "picture": res['sprites']['front_shiny'],
                "attack_base":res['stats'][2]['base_stat'] ,
                "defense_base": res['stats'][3]['base_stat'],
                "hp_base" : res['stats'][0]['base_stat']
                
                }
        
            
        return render_template('pokedex.html.j2', form=form, pokes=poke_dict)
    return render_template('pokedex.html.j2', form=form)

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if request.method=='POST' and form.validate_on_submit():
        # Do Login stuff
        email = form.email.data.lower()
        password = form.password.data

        #Look up user by email address that is trying to log in
        u=User.query.filter_by(email=email).first()
        if u and u.check_hashed_password(password):
            login_user(u)
            flash('Welcome to Fakebook!','success')
            return redirect(url_for('index'))
        flash('Incorrect Email Password Combo', 'danger')
        return render_template('login.html.j2', form=form)
    return render_template("login.html.j2", form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method =='POST' and form.validate_on_submit():
        try:
            new_user_data={
                "first_name":form.first_name.data.title(),
                "last_name": form.last_name.data.title(),
                "email":form.email.data.lower(),
                "password":form.password.data
            }
            # Create an empty User
            new_user_object = User()
            #build user with the form data
            new_user_object.from_dict(new_user_data)
            #save user to the database
            new_user_object.save()

        except:
            flash("There was an unexpected Error creating you account Please Try again Later","danger")
            return render_template('register.html.j2', form=form)
        flash('You have successfully registered!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html.j2', form=form)


@app.route('/logout')
@login_required
def logout():
    if current_user:
        logout_user()
        flash('You have logged out','warning')
        return redirect(url_for('login'))