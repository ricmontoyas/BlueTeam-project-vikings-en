import tkinter as tk
from tkinter import messagebox
import random
from vikingsClasses import Viking, Saxon, War
from pokemonClasses import Player, Pokemon, PokemonAttack

# Pokémon choices
POKEMON_CHOICES = {
    "Bulbasaur": ["Tackle", "Scratch", "Vine Whip"],
    "Charmander": ["Tackle", "Scratch", "Ember"],
    "Squirtle": ["Tackle", "Scratch", "Water Gun"]
}

ATTACK_DAMAGE = {
    attack: random.randint(10, 30) for moves in POKEMON_CHOICES.values() for attack in moves
}

# GUI Setup
class PokemonBattleGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Pokémon Battle")
        self.root.geometry("400x500")
        
        self.player_name = ""
        self.player_pokemon = ""
        self.gary_pokemon = ""
        self.player = None
        self.gary = None
        self.war = None
        
        # Init Data
        ## Type Player
        self.player1 = ""
        self.player2 = ""
        ## List of general able Pokemons 
        self.pokemons = []
        ## List of general able Pokemons Attacks
        self.pokemons_attacks = []

        # Start
        self.start_screen()
        
    def init_data(self, player1_name, player2_name = "Gary"):
        # Init players
        self.player1 = Player(player1_name)
        self.player2 = Player(player2_name)

        # Init Pokemons
        self.pokemons.append(Pokemon("Bulbasaur", "Bulbasaur are small, amphibian and plant Pokémon that move on all four legs", 100))
        self.pokemons.append(Pokemon("Charmander", "Charmander is a bipedal, reptilian Pokémon", 100))
        self.pokemons.append(Pokemon("Squirtle", "Squirtle is a light-blue turtle creature with a hard brown shell and a long, curly tail.", 100))

        # Init Pokemon Attacks
        self.pokemons_attacks.append(PokemonAttack("Tackle", "A physical attack in which the user charges and slams into the foe with its whole body.", 10,1 ,2))
        self.pokemons_attacks.append(PokemonAttack("Scratch", "Scratches the target with sharp claws. Hard, pointed, and sharp claws rake the foe to inflict damage.", 10,1 ,3))
        self.pokemons_attacks.append(PokemonAttack("Vine Whip", "The Pokémon uses its cruel whips to strike the opponent. Whips the foe with slender vines. 0.8 acuracy", 20,0.8 ,4))
        self.pokemons_attacks.append(PokemonAttack("Ember", "An attack that may inflict a burn. 0.7 acuracy", 23,0.7 ,4))
        self.pokemons_attacks.append(PokemonAttack("Water Gun", "The foe is blasted with a forceful shot of water. 0.6 acuracy", 25,0.6 ,4))


    def start_screen(self):
        self.clear_window()
        tk.Label(self.root, text="Welcome to Pokémon Battle!", font=("Arial", 16)).pack(pady=10)
        tk.Label(self.root, text="Enter your name:").pack()
        self.name_entry = tk.Entry(self.root)
        self.name_entry.pack()

        # Init Data
        self.init_data(self.name_entry)

        tk.Button(self.root, text="Next", command=self.choose_pokemon).pack(pady=10)
    
    def choose_pokemon(self):
        self.player_name = self.name_entry.get()
        if not self.player_name:
            messagebox.showwarning("Warning", "Please enter your name!")
            return
        
        self.clear_window()
        tk.Label(self.root, text=f"Hello {self.player_name}! Choose your Pokémon:", font=("Arial", 14)).pack(pady=10)
        for pokemon in POKEMON_CHOICES.keys():
            tk.Button(self.root, text=pokemon, command=lambda p=pokemon: self.start_battle(p)).pack(pady=5)
    
    def start_battle(self, pokemon):
        self.player_pokemon = pokemon
        self.gary_pokemon = random.choice([p for p in POKEMON_CHOICES.keys() if p != pokemon])
        
        self.player = Viking(self.player_name, 100, 50, None)
        self.gary = Saxon(100, 50, None)
        self.war = War()
        self.war.addViking(self.player)
        self.war.addSaxon(self.gary)
        
        self.battle_screen()
    
    def battle_screen(self):
        self.clear_window()
        tk.Label(self.root, text=f"{self.player_name}'s {self.player_pokemon} VS Gary's {self.gary_pokemon}", font=("Arial", 14)).pack(pady=10)
        self.player_hp = tk.Label(self.root, text=f"Your HP: {self.player.health}")
        self.player_hp.pack()
        self.gary_hp = tk.Label(self.root, text=f"Gary's HP: {self.gary.health}")
        self.gary_hp.pack()
        
        tk.Label(self.root, text="Choose an attack:").pack()
        for attack in POKEMON_CHOICES[self.player_pokemon]:
            tk.Button(self.root, text=f"{attack} ({ATTACK_DAMAGE[attack]} dmg)", command=lambda a=attack: self.attack(a)).pack(pady=2)
    
    def attack(self, attack):
        damage = ATTACK_DAMAGE[attack]
        self.gary.receiveDamage(damage)
        
        if self.gary.health <= 0:
            messagebox.showinfo("Victory!", "🎉 You won the battle! 🎉")
            self.end_game()
            return
        
        self.player.receiveDamage(ATTACK_DAMAGE[random.choice(POKEMON_CHOICES[self.gary_pokemon])])
        
        if self.player.health <= 0:
            messagebox.showinfo("Defeat...", "😈 Gary defeated you! 😈")
            self.end_game()
            return
        
        self.update_health()
    
    def update_health(self):
        self.player_hp.config(text=f"Your HP: {self.player.health}")
        self.gary_hp.config(text=f"Gary's HP: {self.gary.health}")
    
    def end_game(self):
        self.clear_window()
        tk.Label(self.root, text="Game Over", font=("Arial", 16)).pack(pady=10)
        tk.Button(self.root, text="Play Again", command=self.start_screen).pack(pady=5)
        tk.Button(self.root, text="Exit", command=self.root.quit).pack(pady=5)
    
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    game = PokemonBattleGame(root)
    root.mainloop()
    