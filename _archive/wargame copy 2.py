import random
import pygame
from vikingsClasses import Viking, Saxon, War


# Initialize pygame mixer
pygame.mixer.init()

# Define paths to music files
MUSIC_PATHS = {
    "intro": "week_2\project_vikings\project-vikings-en\BlueTeam-project-vikings-en\Music\Intro_music_edited_1.ogg",
    "battle": "week_2\project_vikings\project-vikings-en\BlueTeam-project-vikings-en\Music\Battle_track_mixdown.ogg",
    "victory": "week_2\project_vikings\project-vikings-en\BlueTeam-project-vikings-en\Music\success_mixdown.ogg",
    "defeat": "week_2\project_vikings\project-vikings-en\BlueTeam-project-vikings-en\Music\defeat_mixdown.ogg"
}

# Function to play music
def play_music(track, loop=False):
    pygame.mixer.music.load(MUSIC_PATHS[track])
    pygame.mixer.music.play(-1 if loop else 0)  # -1 for looping, 0 for one-time play

# Function to stop music
def stop_music():
    pygame.mixer.music.stop()


def start_game(player_name=None, player_pokemon=None):
    POKEMON_CHOICES = {
        "🍃Bulbasaur": ["Tackle", "Scratch", "Vine Whip"],
        "🔥Charmander": ["Tackle", "Scratch", "Ember"],
        "💧Squirtle": ["Tackle", "Scratch", "Water Gun"]
    }
    ATTACK_DAMAGE = {
        attack: random.randint(10, 30) for moves in POKEMON_CHOICES.values() for attack in moves
    }
    
    if not player_name:
        play_music("intro", loop=True)  # Play intro music in loop
        print("""
███████████████████████████████████████
█                                       █
█  WELCOME TO YOUR POKÉMON FIRST BATTLE   █
█                                       █
███████████████████████████████████████    
          
🔥 Hello everyone! The moment every Pokémon master has been waiting for has arrived!
It's time to meet Professor Oak and choose your first Pokémon!
👨‍🔬 Professor Oak: Hello there! Welcome to the world of Pokémon!
🌍 My name is Oak, and this here is my grandson, Gary! (Gary smirks)
😏 We’ve known each other for a long time, but today, you will begin your journey as a Pokémon Trainer!
""")
        player_name = input("But first, tell me your name: ")

    stop_music()  # Stop intro music
    play_music("battle", loop=True)  # Start battle music
    
    print(f"🎮 Welcome, {player_name}! Your adventure begins now!\n")
    
    if not player_pokemon:
        while True:
            print("Now, it's time for you to choose your very first Pokémon!")
            for i, pokemon in enumerate(POKEMON_CHOICES.keys()):
                print(f"{i+1}. {pokemon}")
            try:
                choice = int(input("\nEnter the number: ")) - 1
                if 0 <= choice < len(POKEMON_CHOICES):
                    break
            except ValueError:
                pass
            print("Invalid choice! Please select a valid Pokémon.")
        
        player_pokemon = list(POKEMON_CHOICES.keys())[choice]
    player_attacks = POKEMON_CHOICES[player_pokemon]
    
    print(f"🏆 Great choice! You picked {player_pokemon}!")
    gary_pokemon = random.choice([p for p in POKEMON_CHOICES.keys() if p != player_pokemon])
    gary_attacks = POKEMON_CHOICES[gary_pokemon]
    print(f"😈 Your rival Gary chose {gary_pokemon}!")
    
    great_war = War()
    player = Viking(player_name, 100, 50, None)
    gary = Saxon(100, 50, None)
    great_war.addViking(player)
    great_war.addSaxon(gary)
    
    while great_war.showStatus() == "Vikings and Saxons are still in the thick of battle.":
        print("\n⚠️  NEW TURN ⚠️")
        print(f"{player_name}'s {player_pokemon} HP: {player.health}")
        print(f"Gary's {gary_pokemon} HP: {gary.health}")
        
        while True:
            print("\nChoose an attack:")
            for i, attack in enumerate(player_attacks):
                print(f"{i+1}. {attack}")
            try:
                attack_choice = int(input("Enter the attack number: ")) - 1
                if 0 <= attack_choice < len(player_attacks):
                    break
            except ValueError:
                pass
            print("Invalid choice! Please select a valid attack.")
        
        attack_used = player_attacks[attack_choice]
        attack_effect = random.randint(1, 30)
        if attack_effect <= 10:
            print("\nNice try! The Pokémon defended your attack.")
        elif attack_effect <= 20:
            print("\nThe Pokémon has received damage.")
        else:
            print("\nGreat attack! The opponent suffered damage.")
        
        print(f"{player_pokemon} used {attack_used}! ⚔️")
        print(gary.receiveDamage(ATTACK_DAMAGE[attack_used]))
        if gary.health <= 0:
            break
        
        gary_attack = random.choice(gary_attacks)
        print(f"Gary's {gary_pokemon} used {gary_attack}! 😈")
        print(player.receiveDamage(ATTACK_DAMAGE[gary_attack]))
        if player.health <= 0:
            break
    

    stop_music()  # Stop battle music


    if player.health > 0:
        play_music("victory")  # Play victory music
        print("🎉 You won! You have a bright future as a Pokémon master! 🎉")
    else:
        play_music("defeat")  # Play defeat music
        print("😈 Ha! I proved I'm the best! 😈")
    
    while True:
        print("What do you want to do?")
        print("1. Play again with the same Pokémon")
        print("2. Choose a different Pokémon")
        print("3. End the game")
        choice = input("Enter your choice: ")
        if choice in ["1", "2", "3"]:
            break
        print("Invalid choice! Please enter 1, 2, or 3.")
    
    if choice == "1":
        print("Restarting battle with the same Pokémon... ⚔️")
        stop_music()  # Stop current music
        play_music("battle", loop=True)  # Restart battle music
        start_game(player_name, player_pokemon)
    elif choice == "2":
        print("Restarting... Choose your Pokémon again! 🏆")
        stop_music()  # Stop current music
        play_music("battle", loop=True)  # Restart battle music
        start_game()
    elif choice == "3":
        stop_music()  # Stop music when exiting the game
        print("Goodbye, Pokémon Master! See you on your next adventure! 🎮")

start_game()
