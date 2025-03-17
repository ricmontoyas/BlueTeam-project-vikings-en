import tkinter as tk
from tkinter import messagebox
import random
from vikingsClasses import Viking, Saxon, War

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
        
        self.start_screen()
        
    def start_screen(self):
        self.clear_window()
        tk.Label(self.root, text="Welcome to Pokémon Battle!", font=("Arial", 16)).pack(pady=10)
        tk.Label(self.root, text="Enter your name:").pack()
        self.name_entry = tk.Entry(self.root)
        self.name_entry.pack()
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
    