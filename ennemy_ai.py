"""A really simple way to give so AI to an ennemy"""
from random import randint

from character import Character

class EnnemyAI():
    """Simulate actions choice for a Ennemy Character
    Actions possibles are ACTION_ATTACK and ACTION_DRINKPOTION
    """

    def __init__(self, character: Character):
        self.character = character


    def decide_action(self) -> str:
        """Decide witch actions to take and return it

        Returns:
            str: One of the possible action between Character.ACTIONS
                can be ACTION_ATTACK or ACTION_DRINKPOTION
        """
        if self.character.stats.can_drink_potion:

            # Wil decide randomly (50/50) to take a potion if life points is below 25% of max life and he has potion
            # Otherwise, he decide to attack
            if self.character.inventory.has_potion:   #He has a potion
                pourcent_life_remains = self.character.current_life / self.character.stats.max_life * 100

                if pourcent_life_remains < 25:
                    if randint(False, True):
                        return Character.ACTION_DRINKPOTION
        
        return Character.ACTION_ATTACK

        

if __name__ == "__main__":

    ennemy = Character.default_ennemy()
    ennemy.current_life = 2
    ennemy_ai = EnnemyAI(ennemy)
    print(f"Action = {ennemy_ai.decide_action()}")  # Must always be ATTACK (default ennemy cannot drink potion)

    thief = Character.thief()
    thief.current_life = 2
    thief_ai = EnnemyAI(thief)
    print(f"Action = {EnnemyAI.decide_action(thief_ai)}")