import random
import os
import tkinter as tk
from tkinter import messagebox
from pokemonClasses import Pokemon, PokemonAttack, Player
from pygame import mixer

###############################################
# Code updated to set focus on the name entry.
###############################################

# Get the current directory path of wargame.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Music files stored in the same folder as wargame.py
MUSIC_PATHS = {
    "intro": os.path.join(BASE_DIR, "Intro_music_edited_1.ogg"),
    "battle": os.path.join(BASE_DIR, "Battle_track_mixdown.ogg"),
    "victory": os.path.join(BASE_DIR, "success_mixdown.ogg"),
    "defeat": os.path.join(BASE_DIR, "defeat_mixdown.ogg")
}

# Attack dictionary - updated so it takes at least two hits to win
ATTACK_DATA = {
    "Tackle":      {"damage": 15, "accuracy": 0.9},
    "Scratch":     {"damage": 15, "accuracy": 0.9},
    "Vine Whip":   {"damage": 25, "accuracy": 0.8},
    "Ember":       {"damage": 25, "accuracy": 0.8},
    "Water Gun":   {"damage": 25, "accuracy": 0.8}
}

# Each Pokémon's available attacks
POKEMON_ATTACKS = {
    "🍃Bulbasaur": ["Tackle", "Scratch", "Vine Whip"],
    "🔥Charmander": ["Tackle", "Scratch", "Ember"],
    "💧Squirtle":  ["Tackle", "Scratch", "Water Gun"]
}

# Initialize pygame mixer
mixer.init()

def play_music(track, loop=False):
    mixer.music.load(MUSIC_PATHS[track])
    mixer.music.play(-1 if loop else 0)

def stop_music():
    mixer.music.stop()

class PokemonGame:
    def __init__(self, master):
        self.root = master
        self.root.title("Pokémon Battle")
        self.root.geometry("700x500")

        # Load images AFTER we have a Tk root
        self.pokemon_images = {
            "🍃Bulbasaur": self.load_image("Bulbasaur.gif"),
            "🔥Charmander": self.load_image("Charmander.gif"),
            "💧Squirtle":  self.load_image("Squirtle.gif")
        }
        # If you have attack images, load them here:
        self.attack_images = {
            "Tackle":    None,
            "Scratch":   None,
            "Vine Whip": None,
            "Ember":     None,
            "Water Gun": None
        }

        # Start intro music
        play_music("intro", loop=True)

        # Game state variables
        self.player_name = ""
        self.player_pokemon = None
        self.gary_pokemon = None

        # Both start with 60 HP to prevent a single-hit win
        self.player_hp = 0
        self.gary_hp = 0

        # Partial log of the battle
        self.battle_log = ""

        # Step 1: Show only introduction text + Next button
        self.welcome_screen()

    def load_image(self, filename):
        """Load images from _images folder, linked to the existing Tk root."""
        path = os.path.join(BASE_DIR, "_images", filename)
        if os.path.exists(path):
            return tk.PhotoImage(file=path, master=self.root)
        return None

    def welcome_screen(self):
        """First screen with ONLY the introduction text and a Next button."""
        self.clear_screen()

        intro_text = (
            "WELCOME TO YOUR FIRST POKÉMON BATTLE!\n\n"
            "Hello, future Pokémon Master!\n\n"
            "It's time to meet Professor Oak and choose your first Pokémon!\n"
            "Professor Oak: Hello there! Welcome to the world of Pokémon!\n"
            "My name is Oak, and this here is my grandson, Gary!\n"
            "We've known each other for a long time, but today, you will begin your journey as a Pokémon Trainer!\n"
        )

        tk.Label(
            self.root,
            text=intro_text,
            font=("Arial", 12),
            justify="left",
            wraplength=650
        ).pack(pady=20)

        tk.Button(
            self.root,
            text="Next",
            font=("Arial", 12),
            command=self.create_name_screen
        ).pack(pady=10)

    def create_name_screen(self):
        """Second screen: ask for player's name + a Continue button."""
        self.clear_screen()

        tk.Label(
            self.root,
            text="Please enter your name:",
            font=("Arial", 12)
        ).pack(pady=10)

        self.name_entry = tk.Entry(self.root, font=("Arial", 12))
        self.name_entry.pack(pady=5)

        # <-- Focus immediately on this entry box
        self.name_entry.focus_set()

        tk.Button(
            self.root,
            text="Continue",
            font=("Arial", 12),
            command=self.intro_continue
        ).pack(pady=10)

    def intro_continue(self):
        """ Gets the player's name and proceeds to Pokémon selection. """
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showwarning("Warning", "Please enter a valid name!")
            return

        self.player_name = name
        stop_music()       # stop intro music
        play_music("battle", loop=True)

        self.choose_pokemon()

    def choose_pokemon(self):
        """ Screen for choosing a Pokémon. """
        self.clear_screen()

        tk.Label(
            self.root,
            text=f"Hello {self.player_name}, choose your Pokémon!",
            font=("Arial", 12)
        ).pack(pady=10)

        self.pokemon_var = tk.StringVar()
        self.pokemon_var.set("🍃Bulbasaur")

        # Display each Pokémon along with its image
        for pokemon in ["🍃Bulbasaur", "🔥Charmander", "💧Squirtle"]:
            frm = tk.Frame(self.root)
            frm.pack(anchor=tk.W, pady=5)

            # Show Pokémon image if available
            img = self.pokemon_images[pokemon]
            if img:
                tk.Label(frm, image=img).pack(side=tk.LEFT)

            tk.Radiobutton(
                frm,
                text=pokemon,
                variable=self.pokemon_var,
                value=pokemon,
                font=("Arial", 11)
            ).pack(side=tk.LEFT, padx=10)

        tk.Button(
            self.root,
            text="Confirm",
            command=self.start_battle
        ).pack(pady=10)

    def start_battle(self):
        """ Assigns the chosen Pokémon, Gary's Pokémon, HP, and shows a screen with both images. """
        self.player_pokemon = self.pokemon_var.get()
        self.gary_pokemon = random.choice([
            p for p in ["🍃Bulbasaur", "🔥Charmander", "💧Squirtle"]
            if p != self.player_pokemon
        ])

        self.player_hp = 60
        self.gary_hp = 60
        self.battle_log = (
            f"You chose {self.player_pokemon}! Gary chose {self.gary_pokemon}!\n"
            f"Let the battle begin!\n"
        )

        self.clear_screen()

        # Show both images side by side
        images_frame = tk.Frame(self.root)
        images_frame.pack(pady=10)

        player_img = self.pokemon_images[self.player_pokemon]
        if player_img:
            tk.Label(images_frame, image=player_img).grid(row=0, column=0, padx=20)
        tk.Label(images_frame, text=self.player_pokemon, font=("Arial", 12, "bold")).grid(row=1, column=0)

        gary_img = self.pokemon_images[self.gary_pokemon]
        if gary_img:
            tk.Label(images_frame, image=gary_img).grid(row=0, column=1, padx=20)
        tk.Label(images_frame, text=self.gary_pokemon, font=("Arial", 12, "bold")).grid(row=1, column=1)

        tk.Label(
            self.root,
            text=self.battle_log,
            font=("Arial", 12),
            wraplength=650,
            justify="left"
        ).pack(pady=10)

        tk.Button(
            self.root,
            text="Continue",
            command=self.battle_screen
        ).pack(pady=10)

    def battle_screen(self):
        """ Screen that shows the battle interface: HP bars and attack selection. """
        self.clear_screen()

        top_frame = tk.Frame(self.root)
        top_frame.pack(pady=10)

        # Player's Pokémon image and HP
        player_img = self.pokemon_images[self.player_pokemon]
        if player_img:
            tk.Label(top_frame, image=player_img).grid(row=0, column=0, padx=10)
        tk.Label(
            top_frame,
            text=f"{self.player_pokemon}\nHP: {self.player_hp}",
            font=("Arial", 12),
            justify="center"
        ).grid(row=0, column=1)

        # Gary's Pokémon image and HP
        gary_img = self.pokemon_images[self.gary_pokemon]
        if gary_img:
            tk.Label(top_frame, image=gary_img).grid(row=0, column=2, padx=10)
        tk.Label(
            top_frame,
            text=f"{self.gary_pokemon}\nHP: {self.gary_hp}",
            font=("Arial", 12),
            justify="center"
        ).grid(row=0, column=3)

        tk.Label(
            self.root,
            text="Choose an attack:",
            font=("Arial", 12)
        ).pack(pady=5)

        self.attack_var = tk.StringVar()
        attacks = POKEMON_ATTACKS[self.player_pokemon]
        self.attack_var.set(attacks[0])

        for atk in attacks:
            frm = tk.Frame(self.root)
            frm.pack(anchor=tk.W)
            atk_img = self.attack_images[atk]
            if atk_img:
                tk.Label(frm, image=atk_img).pack(side=tk.LEFT)

            tk.Radiobutton(
                frm,
                text=atk,
                variable=self.attack_var,
                value=atk
            ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            self.root,
            text="Attack!",
            command=self.perform_attack
        ).pack(pady=10)

    def perform_attack(self):
        """ The player attacks, then Gary attacks, updating HP and checking for victory. """
        attack_used = self.attack_var.get()
        accuracy = ATTACK_DATA[attack_used]["accuracy"]
        damage = ATTACK_DATA[attack_used]["damage"]

        if random.random() <= accuracy:
            if damage <= 15:
                extra_msg = "\nNice try!"
            elif damage <= 20:
                extra_msg = "\nAverage Attack!"
            else:
                extra_msg = "\nGreat Attack!"

            self.gary_hp -= damage
            text_hit = (
                f"{self.player_pokemon} used {attack_used}! "
                f"It hits Gary's {self.gary_pokemon} for {damage} damage!" + extra_msg
            )
        else:
            text_hit = f"{self.player_pokemon} used {attack_used} but missed!"

        # Check if Gary is defeated
        if self.gary_hp <= 0:
            stop_music()
            play_music("victory")
            self.gary_hp = 0
            self.show_battle_result(text_hit, "You won!")
            return

        # GARY attacks back
        gary_attack = random.choice(POKEMON_ATTACKS[self.gary_pokemon])
        gary_acc = ATTACK_DATA[gary_attack]["accuracy"]
        gary_dmg = ATTACK_DATA[gary_attack]["damage"]
        if random.random() <= gary_acc:
            if gary_dmg <= 15:
                extra_msg_gary = "\nNice try!"
            elif gary_dmg <= 20:
                extra_msg_gary = "\nAverage Attack!"
            else:
                extra_msg_gary = "\nGreat Attack!"

            self.player_hp -= gary_dmg
            text_gary = (
                f"Gary's {self.gary_pokemon} used {gary_attack}! "
                f"It hits your {self.player_pokemon} for {gary_dmg} damage!" + extra_msg_gary
            )
        else:
            text_gary = (
                f"Gary's {self.gary_pokemon} used {gary_attack} but missed!"
            )

        # Check if player is defeated
        if self.player_hp <= 0:
            stop_music()
            play_music("defeat")
            self.player_hp = 0
            self.show_battle_result(f"{text_hit}\n{text_gary}", "Gary won!")
            return

        # If battle continues, update screen
        self.battle_log = f"{text_hit}\n{text_gary}\n"
        self.battle_screen()

    def show_battle_result(self, last_moves, final_result):
        """ Displays the final result and options to replay. """
        self.clear_screen()

        tk.Label(
            self.root,
            text=last_moves,
            font=("Arial", 12),
            justify="left",
            wraplength=650
        ).pack(pady=10)

        tk.Label(
            self.root,
            text=final_result,
            font=("Arial", 14, "bold")
        ).pack(pady=10)

        tk.Button(
            self.root,
            text="Play again with the same Pokémon",
            command=self.rematch_same
        ).pack(pady=5)

        tk.Button(
            self.root,
            text="Choose another Pokémon",
            command=self.rematch_different
        ).pack(pady=5)

        tk.Button(
            self.root,
            text="Exit",
            command=self.root.quit
        ).pack(pady=5)

    def rematch_same(self):
        stop_music()
        play_music("battle", loop=True)
        self.gary_pokemon = random.choice([
            p for p in ["🍃Bulbasaur", "🔥Charmander", "💧Squirtle"]
            if p != self.player_pokemon
        ])
        self.player_hp = 60
        self.gary_hp = 60
        self.battle_screen()

    def rematch_different(self):
        stop_music()
        play_music("battle", loop=True)
        self.choose_pokemon()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

def main():
    root = tk.Tk()
    game = PokemonGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()