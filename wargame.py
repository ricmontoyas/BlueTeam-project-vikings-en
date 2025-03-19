import random
import os
import tkinter as tk
from tkinter import messagebox
from pokemonClasses import Pokemon, PokemonAttack, Player
from pygame import mixer

###############################################
# Final version: Buttons for replay/exit appear
# only at the end of the battle, in show_battle_result.
###############################################

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MUSIC_PATHS = {
    "intro": os.path.join(BASE_DIR, "Intro_music_edited_1.ogg"),
    "battle": os.path.join(BASE_DIR, "Battle_track_mixdown.ogg"),
    "victory": os.path.join(BASE_DIR, "success_mixdown.ogg"),
    "defeat": os.path.join(BASE_DIR, "defeat_mixdown.ogg")
}

# Updated attacks with emojis
ATTACK_DATA = {
    "💥Tackle":      {"damage": 15, "accuracy": 0.9},
    "🐾Scratch":     {"damage": 15, "accuracy": 0.9},
    "🌱Vine Whip":   {"damage": 25, "accuracy": 0.8},
    "🔥Ember":       {"damage": 25, "accuracy": 0.8},
    "💧Water Gun":   {"damage": 25, "accuracy": 0.8}
}

POKEMON_ATTACKS = {
    "🍃Bulbasaur": ["💥Tackle", "🐾Scratch", "🌱Vine Whip"],
    "🔥Charmander": ["💥Tackle", "🐾Scratch", "🔥Ember"],
    "💧Squirtle":  ["💥Tackle", "🐾Scratch", "💧Water Gun"]
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

        # Load images AFTER root is created
        self.pokemon_images = {
            "🍃Bulbasaur": self.load_image("Bulbasaur.gif"),
            "🔥Charmander": self.load_image("Charmander.gif"),
            "💧Squirtle":  self.load_image("Squirtle.gif")
        }
        self.attack_images = {
            "💥Tackle":    None,
            "🐾Scratch":   None,
            "🌱Vine Whip": None,
            "🔥Ember":     None,
            "💧Water Gun": None
        }

        play_music("intro", loop=True)

        self.player_name = ""
        self.player_pokemon = None
        self.friend_name = ""
        self.friend_pokemon = None

        self.player_hp = 0
        self.friend_hp = 0
        self.battle_log = ""

        self.welcome_screen()

    def load_image(self, filename):
        """Attempt to load an image from _images folder."""
        path = os.path.join(BASE_DIR, "_images", filename)
        if os.path.exists(path):
            return tk.PhotoImage(file=path, master=self.root)
        return None

    def welcome_screen(self):
        """First screen: shows introduction text + Next button."""
        self.clear_screen()

        intro_text = (
            "🎮 WELCOME TO YOUR FIRST POKÉMON BATTLE!\n\n"
            "👋 Hello, future Pokémon Master!\n\n"
            "🌳 It's time to meet Professor Oak and choose your first Pokémon!\n"
            "👴 Professor Oak: Hello there! Welcome to the world of Pokémon!\n"
            "🤝 My name is Oak, and this here is my grandson, Gary!\n"
            "🚀 We've known each other for a long time, but today, you will begin your journey as a Pokémon Trainer!\n"
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
        """Second screen: asks for player's name, then 'Continue'."""
        self.clear_screen()

        tk.Label(
            self.root,
            text="Please enter your name:",
            font=("Arial", 12)
        ).pack(pady=10)

        self.name_entry = tk.Entry(self.root, font=("Arial", 12))
        self.name_entry.pack(pady=5)
        self.name_entry.focus_set()

        tk.Button(
            self.root,
            text="Continue",
            font=("Arial", 12),
            command=self.intro_continue
        ).pack(pady=10)

    def intro_continue(self):
        """Stores player's name and moves on to choose a Pokémon."""
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showwarning("Warning", "Please enter a valid name!")
            return

        self.player_name = name
        stop_music()
        play_music("battle", loop=True)
        self.choose_pokemon()

    def choose_pokemon(self):
        """Screen to select Bulbasaur, Charmander, or Squirtle."""
        self.clear_screen()

        tk.Label(
            self.root,
            text=f"Hello {self.player_name}, choose your Pokémon!",
            font=("Arial", 12)
        ).pack(pady=10)

        self.pokemon_var = tk.StringVar()
        self.pokemon_var.set("🍃Bulbasaur")

        for pokemon in ["🍃Bulbasaur", "🔥Charmander", "💧Squirtle"]:
            frm = tk.Frame(self.root)
            frm.pack(anchor=tk.W, pady=5)

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
        """Assigns the chosen Pokémon, chooses a random friend and their Pokémon, sets HP, then shows them."""
        self.player_pokemon = self.pokemon_var.get()

        # random friend
        possible_friends = [
            "David", "Jorge", "Tayna", "Eduardo", "Luis", "Marc",
            "Maria", "Nancy", "Patricia", "Stefano", "Zeynep"
        ]
        self.friend_name = random.choice(possible_friends)

        # friend's random Pokémon
        self.friend_pokemon = random.choice([
            p for p in ["🍃Bulbasaur", "🔥Charmander", "💧Squirtle"]
            if p != self.player_pokemon
        ])

        self.player_hp = 60
        self.friend_hp = 60

        self.battle_log = (
            f"You chose {self.player_pokemon}! "
            f"{self.friend_name} chose {self.friend_pokemon}!\n"
            "Let the battle begin!\n"
        )

        self.clear_screen()

        images_frame = tk.Frame(self.root)
        images_frame.pack(pady=10)

        # Show player's Pokémon
        player_img = self.pokemon_images[self.player_pokemon]
        if player_img:
            tk.Label(images_frame, image=player_img).grid(row=0, column=0, padx=20)
        tk.Label(
            images_frame,
            text=f"Your Pokémon: {self.player_pokemon}",
            font=("Arial", 12, "bold")
        ).grid(row=1, column=0)

        # Show friend's Pokémon
        friend_img = self.pokemon_images[self.friend_pokemon]
        if friend_img:
            tk.Label(images_frame, image=friend_img).grid(row=0, column=1, padx=20)
        tk.Label(
            images_frame,
            text=f"{self.friend_name}'s Pokémon: {self.friend_pokemon}",
            font=("Arial", 12, "bold")
        ).grid(row=1, column=1)

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
        """Main battle interface: HP, attacks, battle log, but NO replay/exit buttons yet."""
        self.clear_screen()

        top_frame = tk.Frame(self.root)
        top_frame.pack(pady=10)

        # Left: player's Pokémon
        player_img = self.pokemon_images[self.player_pokemon]
        if player_img:
            tk.Label(top_frame, image=player_img).grid(row=0, column=0, padx=10)
        tk.Label(
            top_frame,
            text=f"Your Pokémon: {self.player_pokemon}\nHP: {self.player_hp}",
            font=("Arial", 12),
            justify="center"
        ).grid(row=0, column=1)

        # Right: friend's Pokémon
        friend_img = self.pokemon_images[self.friend_pokemon]
        if friend_img:
            tk.Label(top_frame, image=friend_img).grid(row=0, column=2, padx=10)
        tk.Label(
            top_frame,
            text=f"{self.friend_name}'s Pokémon: {self.friend_pokemon}\nHP: {self.friend_hp}",
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

        # Show the log from the last move, if any
        if self.battle_log.strip():
            tk.Label(
                self.root,
                text=self.battle_log,
                font=("Arial", 12),
                justify="left",
                wraplength=650,
                fg="blue"
            ).pack(pady=5)

    def perform_attack(self):
        """Perform player's attack, then friend's counterattack, then refresh UI."""
        attack_used = self.attack_var.get()
        accuracy = ATTACK_DATA[attack_used]["accuracy"]
        damage = ATTACK_DATA[attack_used]["damage"]

        # Determine the message based on damage
        if damage <= 15:
            extra_msg = "\nSoft Attack!"
        elif damage <= 20:
            extra_msg = "\nAverage Attack!!"
        else:
            extra_msg = "\nSUPER POWER!!!"

        # Player attacks
        if random.random() <= accuracy:
            self.friend_hp -= damage
            text_hit = (
                f"Your {self.player_pokemon} used {attack_used}! "
                f"It hits {self.friend_name}'s {self.friend_pokemon} for {damage} damage!{extra_msg}"
            )
        else:
            text_hit = f"Your {self.player_pokemon} used {attack_used} but missed!"

        # Check if friend fainted
        if self.friend_hp <= 0:
            stop_music()
            play_music("victory")
            self.friend_hp = 0
            final_text = text_hit
            self.show_battle_result(final_text, "You won!")
            return

        # Friend's turn
        friend_attack = random.choice(POKEMON_ATTACKS[self.friend_pokemon])
        f_accuracy = ATTACK_DATA[friend_attack]["accuracy"]
        f_damage = ATTACK_DATA[friend_attack]["damage"]

        # Friend's extra message based on damage
        if f_damage <= 15:
            friend_extra = "\nSoft Attack!"
        elif f_damage <= 20:
            friend_extra = "\nAverage Attack!!"
        else:
            friend_extra = "\nSUPER POWER!!!"

        if random.random() <= f_accuracy:
            self.player_hp -= f_damage
            text_friend = (
                f"{self.friend_name}'s {self.friend_pokemon} used {friend_attack}! "
                f"It hits your {self.player_pokemon} for {f_damage} damage!{friend_extra}"
            )
        else:
            text_friend = (
                f"{self.friend_name}'s {self.friend_pokemon} used {friend_attack} but missed!"
            )

        # Check if player's fainted
        if self.player_hp <= 0:
            stop_music()
            play_music("defeat")
            self.player_hp = 0
            final_text = f"{text_hit}\n{text_friend}"
            self.show_battle_result(final_text, f"{self.friend_name} won!")
            return

        # If still both are alive, update the log
        self.battle_log = f"{text_hit}\n{text_friend}\n"
        self.battle_screen()

    def show_battle_result(self, last_moves, final_result):
        """Show the final result with options to replay or exit."""
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
        """Rematch with the same Pokémon vs. new random friend + Pokémon."""
        stop_music()
        play_music("battle", loop=True)

        # Pick new friend + new random Pokémon
        possible_friends = [
            "David", "Jorge", "Tayna", "Eduardo", "Luis", "Marc",
            "Maria", "Nancy", "Patricia", "Stefano", "Zeynep"
        ]
        self.friend_name = random.choice(possible_friends)
        self.friend_pokemon = random.choice([
            p for p in ["🍃Bulbasaur", "🔥Charmander", "💧Squirtle"]
            if p != self.player_pokemon
        ])

        self.player_hp = 60
        self.friend_hp = 60
        # Start battle again
        self.battle_screen()

    def rematch_different(self):
        """Pick a brand new Pokémon."""
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