from flask import Flask, render_template, request
import requests

app = Flask(__name__)
@app.route('/')
def index():

    return "<h1>My App</h1>"


@app.route('/Pokedex',  methods=['GET','POST'])
def pokedex():
    if request.method == 'POST':
        poke_name = request.form.get('poke_name')
        
        

        url = f'https://pokeapi.co/api/v2/pokemon/{poke_name}'
        response = requests.get(url)
        if not response.ok:
            error_string = 'We had an error'
            return render_template('pokedex.html.j2', error=error_string)
        new_poke=[]
        poke_dict={}
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
        new_poke.append(poke_dict)
        
        return render_template('pokedex.html.j2', pokes=new_poke)
    return render_template('pokedex.html.j2')