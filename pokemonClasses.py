

class PokemonAttack:
    def __init__(self, name, description, damage, hit_probability):
        self.name = name
        self.description = description
        self.damage = damage
        self.hit_probability = hit_probability
    
    def getName(self):
        return self.name
    
    def getDescription(self):
        return self.description
    
    def getProbability(self):
        return self.hit_probability
    
    def getDamage(self):
        return self.damage

class Pokemon:
    def __init__(self, name, description, health):
        self.name = name
        self.description = description
        self.health = health
        self.pokemon_attacks = []
    
    def addAtack(self, attack):
        self.pokemon_attacks.append(attack)

    def reciveDamage(self, damage):
        self.health -= damage
        if self.health > 0:
            return f"{self.name} has received {damage} points of damage"
        else:
            return f"{self.name} has died in combat"
        
    def getName(self):
        return self.name
    
    def getDescription(self):
        return self.description
    
    def getHealth(self):
        return self.health

    def getAttacks(self):
        return self.pokemon_attacks
    

class Player:
    def __init__(self, name, credits = 10):
        self.name = name
        self.pokemons = []
        self.credits = credits

    def addPokemon(self, pokemon):
        self.pokemons.append(pokemon)

    def getName(self):
        return self.name
    
    def getPokemons(self):
        return self.pokemons
    
    def getCredits(self):
        return self.credits
    



