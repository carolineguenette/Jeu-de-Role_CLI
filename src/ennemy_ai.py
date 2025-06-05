"""A really simple way to give so AI to an ennemy"""
from random import randint

from src.character import Character
from src.exceptions import DeadCharacterError

class EnnemyAI():
    """Simulate actions choice for a Ennemy Character
    Actions possibles are ACTION_ATTACK and ACTION_DRINKPOTION
    """

    def __init__(self, character: Character):
        self.character = character


    def decide_action(self) -> int:
        """Decide witch actions to take and return it

        Returns:
            int: One of the possible action between
                 Character.ACTION_ATTACK or Character.ACTION_DRINKPOTION
        """

        if self.character.is_dead:
            raise DeadCharacterError("Character is dead: he cannot decide anything.")

        if not self.character.stats.can_drink_potion:
            return Character.ACTION_ATTACK

        pourcent_life_remains = self.character.current_life / self.character.stats.max_life * 100
        
        if pourcent_life_remains < 5: #He is somehow stupid: he try to take a potion before checking if he has potion
            return Character.ACTION_DRINKPOTION
        
        if pourcent_life_remains < 25 and self.character.inventory.has_potion():
            if randint(False, True):
                return Character.ACTION_DRINKPOTION

        return Character.ACTION_ATTACK
        

        

if __name__ == "__main__":

    """Unit tests complete: check src/tests/test_ennemy_ai.py"""