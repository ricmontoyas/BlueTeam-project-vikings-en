import random
import os
import tkinter as tk
from tkinter import messagebox
from pokemonClasses import Pokemon, PokemonAttack, Player

# Se requiere Pillow para cargar archivos .jpg
# Instálalo con: pip install pillow
from PIL import Image, ImageTk

from pygame import mixer

###############################################

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MUSIC_PATHS = {
    "intro": os.path.join(BASE_DIR, "Intro_music_edited_1.ogg"),
    "battle": os.path.join(BASE_DIR, "Battle_track_mixdown.ogg"),
    "victory": os.path.join(BASE_DIR, "success_mixdown.ogg"),
    "defeat": os.path.join(BASE_DIR, "defeat_mixdown.ogg")
}

# Attacks with emojis
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

        # Attempt to load professorOak.jpg from _images
        self.prof_oak_img = self.load_jpeg("professorOak.jpg")

        # Load images for Pokémon 
        self.pokemon_images = {
            "🍃Bulbasaur": self.load_tk_image("Bulbasaur.gif"),
            "🔥Charmander": self.load_tk_image("Charmander.gif"),
            "💧Squirtle":  self.load_tk_image("Squirtle.gif")
        }
        # Attack images if needed
        self.attack_images = {
            "💥Tackle":    None,
            "🐾Scratch":   None,
            "🌱Vine Whip": None,
            "🔥Ember":     None,
            "💧Water Gun": None
        }

        # Randomly pick one friend name right here:
        possible_friends = [
            "David", "Jorge", "Tayna", "Eduardo", "Luis", "Marc",
            "Maria", "Nancy", "Patricia", "Stefano", "Zeynep"
        ]
        self.friend_name = random.choice(possible_friends)

        play_music("intro", loop=True)

        self.player_name = ""
        self.player_pokemon = None
        self.friend_pokemon = None

        self.player_hp = 0
        self.friend_hp = 0
        self.battle_log = ""

        self.welcome_screen()

    def load_jpeg(self, filename):
        """
        Loads a JPG image using Pillow and returns a PhotoImage to use in Tkinter.
        If it fails or doesn't exist, returns None.
        """
        path = os.path.join(BASE_DIR, "_images", filename)
        if os.path.exists(path):
            try:
                pil_img = Image.open(path)
                return ImageTk.PhotoImage(pil_img)
            except:
                return None
        return None

    def load_tk_image(self, filename):
        """
        Loads a .gif or .png with Tk's native PhotoImage (if it fails, returns None).
        """
        path = os.path.join(BASE_DIR, "_images", filename)
        if os.path.exists(path):
            try:
                return tk.PhotoImage(file=path, master=self.root)
            except:
                return None
        return None

    def welcome_screen(self):
        """First screen: shows introduction text + the Oak image + Next button."""
        self.clear_screen()

        # Frame to hold the Oak image, if found
        if self.prof_oak_img:
            img_label = tk.Label(self.root, image=self.prof_oak_img)
            img_label.pack(pady=5)

        # We incorporate the random friend name in the introduction text
        # instead of "my grandson, Gary!"
        intro_text = (
            "🎮 WELCOME TO YOUR FIRST POKÉMON BATTLE!\n\n"
            "👋 Hello, the moment every Pokémon master has been waiting for has arrived!\n"
            "🌳 It's time to meet Professor Oak and choose your first Pokémon!\n\n"
            "👴 Professor Oak: Hello there! Welcome to the world of Pokémon!\n"
            f"🤝 My name is Oak, and this here is my friend, {self.friend_name}!\n"
            "🚀 We've known each other for a long time, but today, you will begin your journey as a Pokémon Trainer!\n"
        )

        tk.Label(
            self.root,
            text=intro_text,
            font=("Arial", 14),
            justify="left",
            wraplength=650
        ).pack(pady=20)

        tk.Button(
            self.root,
            text="Next",
            font=("Arial", 14),
            command=self.create_name_screen
        ).pack(pady=10)

    def create_name_screen(self):
        """Second screen: asks for player's name, then 'Continue'."""
        self.clear_screen()

        tk.Label(
            self.root,
            text="Please enter your name:",
            font=("Arial", 14)
        ).pack(pady=20)

        self.name_entry = tk.Entry(self.root, font=("Arial", 14))
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
            font=("Arial", 14)
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
                font=("Arial", 14)
            ).pack(side=tk.LEFT, padx=10)

        tk.Button(
            self.root,
            text="Confirm",
            command=self.start_battle
        ).pack(pady=10)

    def start_battle(self):
        """Assigns the chosen Pokémon and chooses a random Pokémon for the friend, sets HP, then shows them."""
        self.player_pokemon = self.pokemon_var.get()

        # Friend's random Pokémon
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
            font=("Arial", 14, "bold")
        ).grid(row=1, column=0)

        # Show friend's Pokémon
        friend_img = self.pokemon_images[self.friend_pokemon]
        if friend_img:
            tk.Label(images_frame, image=friend_img).grid(row=0, column=1, padx=20)
        tk.Label(
            images_frame,
            text=f"{self.friend_name}'s Pokémon: {self.friend_pokemon}",
            font=("Arial", 14, "bold")
        ).grid(row=1, column=1)

        tk.Label(
            self.root,
            text=self.battle_log,
            font=("Arial", 14),
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
            font=("Arial", 14),
            justify="center"
        ).grid(row=0, column=1)

        # Right: friend's Pokémon
        friend_img = self.pokemon_images[self.friend_pokemon]
        if friend_img:
            tk.Label(top_frame, image=friend_img).grid(row=0, column=2, padx=10)
        tk.Label(
            top_frame,
            text=f"{self.friend_name}'s Pokémon: {self.friend_pokemon}\nHP: {self.friend_hp}",
            font=("Arial", 14),
            justify="center"
        ).grid(row=0, column=3)

        tk.Label(
            self.root,
            text="Choose an attack:",
            font=("Arial", 14)
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
                font=("Arial", 14),
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
        """Rematch with the same Pokémon vs. same random friend name, but new random Pokémon."""
        stop_music()
        play_music("battle", loop=True)

        # If you want a new friend each time, un-comment the code below:
        # possible_friends = [
        #     "David", "Jorge", "Tayna", "Eduardo", "Luis", "Marc",
        #     "Maria", "Nancy", "Patricia", "Stefano", "Zeynep"
        # ]
        # self.friend_name = random.choice(possible_friends)

        self.friend_pokemon = random.choice([
            p for p in ["🍃Bulbasaur", "🔥Charmander", "💧Squirtle"]
            if p != self.player_pokemon
        ])
        self.player_hp = 60
        self.friend_hp = 60
        self.battle_screen()

    def rematch_different(self):
        """Pick a brand new Pokémon (same friend name)."""
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