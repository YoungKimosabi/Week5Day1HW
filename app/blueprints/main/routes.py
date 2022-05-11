from flask import render_template, request, flash
from .forms import PokedexForm
import requests
from .import bp as main
from flask_login import login_required, current_user
from ...models import Pokemon


@main.route('/', methods = ['GET'])
@login_required
def index():

    return render_template('index.html.j2')

@main.route('/pokedex', methods=['GET','POST'])
@login_required
def pokedex():
    
    form = PokedexForm()
    if request.method=='POST' and form.validate_on_submit():
        poke_name = form.pokename.data
        check_poke = Pokemon.query.filter_by(name = poke_name).first()
        if not check_poke:

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
            
            Pokemon.dict(poke_dict)

            Pokemon.save()

        
          
        return render_template('pokedex.html.j2', form=form, pokes=poke_dict)
    return render_template('pokedex.html.j2', form=form)