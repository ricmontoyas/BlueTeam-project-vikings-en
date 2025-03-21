

class PokemonAttack:
    def __init__(self, name, description, damage, hit_probability, credit_cost):
        self.name = name
        self.description = description
        self.damage = damage
        self.hit_probability = hit_probability
        self.credit_cost = credit_cost

    
class Pokemon:
    def __init__(self, name, description, health, image):
        self.name = name
        self.description = description
        self.health = health
        self.pokemon_attacks = []
        self.image = image
    
    def addAtack(self, attack):
        self.pokemon_attacks.append(attack)

    def reciveDamage(self, damage):
        self.health -= damage
        if self.health > 0:
            return f"{self.name} has received {damage} points of damage"
        else:
            return f"{self.name} has died in combat"
    

class Player:
    def __init__(self, name, credits = 10):
        self.name = name
        self.pokemons = []
        self.credits = credits
        self.hp_label = ""

    def addPokemon(self, pokemon):
        self.pokemons.append(pokemon)

    



