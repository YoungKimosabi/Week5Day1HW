from flask import render_template, request
import requests
from .forms import PokedexForm
from app import app

@app.route('/')
def index():

    return "<h1>My App</h1>"

@app.route('/pokedex', methods=['GET','POST'])
def pokedex():
    
    form = PokedexForm()
    if request.method=='POST' and form.validate_on_submit():
        poke_name = form.pokename.data
        url = f'https://pokeapi.co/api/v2/pokemon/{poke_name}'
        response = requests.get(url)
        
        if not response.ok:
            error_string = 'We had an error'
            return render_template('pokedex.html.j2', form=form, error=error_string)
        
        
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

    