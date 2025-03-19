import random
import os
import tkinter as tk
from tkinter import messagebox
from pokemonClasses import Pokemon, PokemonAttack, Player

# Se requiere Pillow para cargar .jpg
from PIL import Image, ImageTk

from pygame import mixer

###############################################
# EXAMPLE: HP animation with after()
###############################################

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MUSIC_PATHS = {
    "intro": os.path.join(BASE_DIR, "Intro_music_edited_1.ogg"),
    "battle": os.path.join(BASE_DIR, "Battle_track_mixdown.ogg"),
    "victory": os.path.join(BASE_DIR, "success_mixdown.ogg"),
    "defeat": os.path.join(BASE_DIR, "defeat_mixdown.ogg")
}

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

        # Load Oak image
        self.prof_oak_img = self.load_jpeg("professorOak.jpg")

        # Load Pokémon images
        self.pokemon_images = {
            "🍃Bulbasaur": self.load_tk_image("Bulbasaur.gif"),
            "🔥Charmander": self.load_tk_image("Charmander.gif"),
            "💧Squirtle":  self.load_tk_image("Squirtle.gif")
        }
        self.attack_images = {
            "💥Tackle":    None,
            "🐾Scratch":   None,
            "🌱Vine Whip": None,
            "🔥Ember":     None,
            "💧Water Gun": None
        }

        # Random friend
        possible_friends = [
            "David", "Jorge", "Tayna", "Eduardo", "Luis", "Marc",
            "Maria", "Nancy", "Patricia", "Stefano", "Zeynep"
        ]
        self.friend_name = random.choice(possible_friends)

        # Initial game state
        self.player_name = ""
        self.player_pokemon = None
        self.friend_pokemon = None

        self.player_hp = 0
        self.friend_hp = 0

        # We will reference these labels for HP animation
        self.player_hp_label = None
        self.friend_hp_label = None

        self.battle_log = ""

        play_music("intro", loop=True)

        self.welcome_screen()

    def load_jpeg(self, filename):
        path = os.path.join(BASE_DIR, "_images", filename)
        if os.path.exists(path):
            try:
                pil_img = Image.open(path)
                return ImageTk.PhotoImage(pil_img)
            except:
                return None
        return None

    def load_tk_image(self, filename):
        path = os.path.join(BASE_DIR, "_images", filename)
        if os.path.exists(path):
            try:
                return tk.PhotoImage(file=path, master=self.root)
            except:
                return None
        return None

    def welcome_screen(self):
        """Intro screen with Oak image + text + Next button."""
        self.clear_screen()

        if self.prof_oak_img:
            tk.Label(self.root, image=self.prof_oak_img).pack(pady=5)

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
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showwarning("Warning", "Please enter a valid name!")
            return

        self.player_name = name
        stop_music()
        play_music("battle", loop=True)
        self.choose_pokemon()

    def choose_pokemon(self):
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
        self.player_pokemon = self.pokemon_var.get()
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

        # Player
        player_img = self.pokemon_images[self.player_pokemon]
        if player_img:
            tk.Label(images_frame, image=player_img).grid(row=0, column=0, padx=20)
        tk.Label(
            images_frame,
            text=f"Your Pokémon: {self.player_pokemon}",
            font=("Arial", 14, "bold")
        ).grid(row=1, column=0)

        # Friend
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
        """Main battle interface: HP, attacks, battle log, NO replay buttons yet."""
        self.clear_screen()

        top_frame = tk.Frame(self.root)
        top_frame.pack(pady=10)

        # Player
        player_img = self.pokemon_images[self.player_pokemon]
        if player_img:
            tk.Label(top_frame, image=player_img).grid(row=0, column=0, padx=10)

        # store references in self.player_hp_label for animation
        self.player_hp_label = tk.Label(
            top_frame,
            text=f"Your Pokémon: {self.player_pokemon}\nHP: {self.player_hp}",
            font=("Arial", 14),
            justify="center"
        )
        self.player_hp_label.grid(row=0, column=1)

        # Friend
        friend_img = self.pokemon_images[self.friend_pokemon]
        if friend_img:
            tk.Label(top_frame, image=friend_img).grid(row=0, column=2, padx=10)

        self.friend_hp_label = tk.Label(
            top_frame,
            text=f"{self.friend_name}'s Pokémon: {self.friend_pokemon}\nHP: {self.friend_hp}",
            font=("Arial", 14),
            justify="center"
        )
        self.friend_hp_label.grid(row=0, column=3)

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

    # ----------- ANIMATION FUNCTION -----------
    def animate_hp_decrease(self, current_hp, target_hp, hp_label, callback):
        """Decreases HP by 1 step until we reach target_hp, updating hp_label each time."""
        if current_hp > target_hp:
            current_hp -= 1
            hp_label.config(text=hp_label.cget("text").split("\n")[0] + f"\nHP: {current_hp}")
            # Re-schedule the next step
            self.root.after(30, lambda: self.animate_hp_decrease(current_hp, target_hp, hp_label, callback))
        else:
            # Once we reach the final HP, call the callback
            callback()

    def perform_attack(self):
        """Perform player's attack, then friend's counterattack, animating HP changes."""
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

        # If player's attack hits
        if random.random() <= accuracy:
            # friend takes damage
            new_friend_hp = self.friend_hp - damage
            text_hit = (
                f"Your {self.player_pokemon} used {attack_used}! "
                f"It hits {self.friend_name}'s {self.friend_pokemon} for {damage} damage!{extra_msg}"
            )
        else:
            # Miss
            new_friend_hp = self.friend_hp
            text_hit = f"Your {self.player_pokemon} used {attack_used} but missed!"

        # We'll animate friend HP, then do the rest
        def after_friend_animation():
            # Update internal friend HP
            self.friend_hp = new_friend_hp

            # If friend fainted
            if self.friend_hp <= 0:
                stop_music()
                play_music("victory")
                final_text = text_hit
                self.show_battle_result(final_text, "You won!")
                return

            # Otherwise, friend counterattacks
            friend_attack = random.choice(POKEMON_ATTACKS[self.friend_pokemon])
            f_accuracy = ATTACK_DATA[friend_attack]["accuracy"]
            f_damage = ATTACK_DATA[friend_attack]["damage"]

            if f_damage <= 15:
                friend_extra = "\nSoft Attack!"
            elif f_damage <= 20:
                friend_extra = "\nAverage Attack!!"
            else:
                friend_extra = "\nSUPER POWER!!!"

            # If friend hits
            if random.random() <= f_accuracy:
                new_player_hp = self.player_hp - f_damage
                text_friend = (
                    f"{self.friend_name}'s {self.friend_pokemon} used {friend_attack}! "
                    f"It hits your {self.player_pokemon} for {f_damage} damage!{friend_extra}"
                )
            else:
                new_player_hp = self.player_hp
                text_friend = (
                    f"{self.friend_name}'s {self.friend_pokemon} used {friend_attack} but missed!"
                )

            # Animate player's HP now
            def after_player_animation():
                self.player_hp = new_player_hp
                # If player fainted
                if self.player_hp <= 0:
                    stop_music()
                    play_music("defeat")
                    final_text = f"{text_hit}\n{text_friend}"
                    self.show_battle_result(final_text, f"{self.friend_name} won!")
                    return

                # If both alive, update log and reload battle screen
                self.battle_log = f"{text_hit}\n{text_friend}\n"
                self.battle_screen()

            # Animate player's HP decrease
            self.animate_hp_decrease(
                self.player_hp,
                new_player_hp,
                self.player_hp_label,
                after_player_animation
            )

        # Start by animating friend's HP
        self.animate_hp_decrease(
            self.friend_hp,
            new_friend_hp,
            self.friend_hp_label,
            after_friend_animation
        )

    def show_battle_result(self, last_moves, final_result):
        self.clear_screen()

        tk.Label(
            self.root,
            text=last_moves,
            font=("Arial", 14),
            justify="left",
            wraplength=650
        ).pack(pady=10)

        tk.Label(
            self.root,
            text=final_result,
            font=("Arial", 16, "bold")
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

        # Keep same friend_name, but random new friend Pokémon
        self.friend_pokemon = random.choice([
            p for p in ["🍃Bulbasaur", "🔥Charmander", "💧Squirtle"]
            if p != self.player_pokemon
        ])
        self.player_hp = 60
        self.friend_hp = 60
        self.battle_log = ""
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