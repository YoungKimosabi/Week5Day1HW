from app import db, login
from flask_login import UserMixin  
from datetime import datetime as dt
from werkzeug.security import generate_password_hash, check_password_hash

class PokemonUser(db.Model):
    poke_id = db.Column(db.Integer, db.ForeignKey('pokemon.poke_id'), primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)

class Pokemon(db.Model):
    poke_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    base_experience = db.Column(db.Integer)
    hp = db.Column(db.Integer)
    attack = db.Column(db.Integer)
    defense = db.Column(db.Integer)
    ability = db.Column(db.String)

    def dict(self, data):
        self.poke_id = data['poke_id']
        self.name = data['name']
        self.base_experience=data['base_experience']
        self.hp =data['hp']
        self.attack = data['attack']
        self.defense = data['defense']
        self.ability = data['ability']

    def save(self):
        db.session.add(self) #adds the pokemon to the db session
        db.session.commit()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name =  db.Column(db.String)
    email =  db.Column(db.String, unique=True, index=True)
    password =  db.Column(db.String)
    created_on = db.Column(db.DateTime, default=dt.utcnow)
    icon = db.Column(db.Integer)
    roster = db.relationship(Pokemon,
                secondary='pokemon_user',
                backref = 'users',
                lazy='dynamic'
                )


    # should return a unique identifing string
    def __repr__(self):
        return f'<User: {self.email} | {self.id}>'

    # Human readbale ver of rpr
    def __str__(self):
        return f'<User: {self.email} | {self.first_name} {self.last_name}>'

    #salts and hashes our password to make it hard to steal
    def hash_password(self, original_password):
        return generate_password_hash(original_password)

    # compares the user password to the password provided in the login form
    def check_hashed_password(self, login_password):
        return check_password_hash(self.password, login_password)

    def from_dict(self, data):
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email=data['email']
        self.password = self.hash_password(data['password'])
        self.icon = data['icon']

    # save the user to the database
    def save(self):
        db.session.add(self) #adds the user to the db session
        db.session.commit() #save everythig in the session to the db

    def get_icon_url(self):
        return f'https://avatars.dicebear.com/api/avataaars/{self.icon}.svg'

    def catchem(self, pokemon):
        if not self.pokemon_in_roster(pokemon) and self.roster.count()<5:
            self.roster.append(pokemon)
            db.session.commit()

    def release(self, pokemon):
        if self.pokemon_in_roster(pokemon):
            self.roster.remove(pokemon)
            db.session.commit()
    
@login.user_loader
def load_user(id):
    return User.query.get(int(id))
    # SELECT * FROM user WHERE id = ???