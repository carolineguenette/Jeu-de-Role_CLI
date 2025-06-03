from typing import Self

class Character:
    def __init__(self, name):
        self.name = name

    def attacks(self, ennemy):
        print(f"{self.name} attacks {ennemy.name}")

class EnnemyAI(Character):
    pass    #A spcecialized Character class where Character can do something more.

# Test
mike = Character("Mike")
gobelin = EnnemyAI("Gobelin")

mike.attacks(gobelin)
gobelin.attacks(mike)