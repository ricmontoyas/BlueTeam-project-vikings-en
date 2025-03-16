import random



# Soldier
class Soldier:
    def __init__(self, health, strength, weapons):
        self.health = health
        self.strength = strength
        self.weapons = weapons
    
    def attack(self):
        return self.strength
    def receiveDamage(self, damage):
        self.health -= damage
    

# Viking
class Viking(Soldier):
    def __init__(self, name, health, strength, weapons):
        super().__init__(health, strength, weapons)
        self.name = name

    def battleCry(self):
        return "Odin Owns You All!"

    def receiveDamage(self, damage):
        self.health -= damage
        if self.health > 0:
            return f"{self.name} has received {damage} points of damage"
        else:
            return f"{self.name} has died in act of combat"

# Saxon
class Saxon(Soldier):
    def __init__(self, health, strength, weapons):
        super().__init__(health, strength, weapons)

    def receiveDamage(self, damage):
        self.health -= damage
        if self.health > 0:
            return f"Gary has received {damage} points of damage"
        else:
            return "Gary has died in combat"

# WAAAAAAAAAR

class War():
    def __init__(self):
        self.vikingArmy = []
        self.saxonArmy = []

    def addViking(self, viking):
        self.vikingArmy.append(viking)
    
    def addSaxon(self, saxon):
        self.saxonArmy.append(saxon)
    
    def vikingAttack(self):
        if self.saxonArmy and self.vikingArmy:
            saxon = random.choice(self.saxonArmy)
            viking = random.choice(self.vikingArmy)
            result = saxon.receiveDamage(viking.attack())
            if saxon.health <= 0:
                self.saxonArmy.remove(saxon)
            return result
    
    def saxonAttack(self):
        if self.vikingArmy and self.saxonArmy:
            saxon = random.choice(self.saxonArmy)
            viking = random.choice(self.vikingArmy)
            result = viking.receiveDamage(saxon.attack())
            if viking.health <= 0:
                self.vikingArmy.remove(viking)
            return result

    def showStatus(self):
        if not self.saxonArmy:
            return "Vikings have won the war of the century!"
        elif not self.vikingArmy:
            return "Saxons have fought for their lives and survive another day..."
        else:
            return "Vikings and Saxons are still in the thick of battle."
    pass