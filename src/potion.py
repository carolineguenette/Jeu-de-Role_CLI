from random import randint
import logging

from src.exceptions import EmptyPotionError, PoisonPotionError
import src.constants as c

#Init local logger
logger = logging.getLogger(__name__)


class Potion:
    """ A Potion that will give back a random number of life points after drinking

    Raises:
        PoisonPotionError: Raise if the range.start or .stop is negative
        EmptyPotionError: Raise if drink() is call more than one time
    """
    instance_counter: int = 0

    def __init__(self, min_recup: int, max_recup: int):
        """ Init the potion

        Args:
            min_recup (int): The minimum number of life points the potion will give. Must be >=0 and lower than max_recup
            max_recup (int): The maximum number of life points the potion will give. Must be >=0 and highter than min_recup

        Raises:
            PoisonPotionError: Raise if the recup_range.start or recup_range.stop is negative
        """
        if min_recup >=0 and max_recup >= 0 and min_recup <= max_recup:
            Potion.instance_counter += 1
            self.id = Potion.instance_counter
            self.min_recup = min_recup
            self.max_recup = max_recup
            self.is_empty = False
            logger.debug(f'Potion creation: {repr(self)} (id={self.id}).')
            
        else:
            raise PoisonPotionError(f"Magic potion do not exist (hum well...) so Potion(min_recup={min_recup}, max_recup={max_recup}) cannot be created.\n\tInit values must be : min_recup >= 0, max_recup >= 0 and min_recup <= max_recup")
        

    def __str__(self) -> str:
        if self.is_empty:
            return (f"Une très belle bouteille vide (Potion {c.YELLOW}{self.id}{c.RESET}).")
        else:
            return (f"{c.BLUE}Potion {self.id}{c.RESET} pouvant redonner entre {c.GREEN}{self.min_recup}{c.RESET} et {c.GREEN}{self.max_recup}{c.RESET} points de vie.")


    def __repr__(self) -> str:
        return f"Potion({self.min_recup}, {self.max_recup})"

        
    def drink(self) -> int:
        """Action to drink the potion. Can be call only once.

        Raises:
            EmptyPotionError: Raise if drink is call more than one time

        Returns:
            int: Number of point of life gain
        """
        logger.debug(f'Drink potion id={self.id}.')
        if not self.is_empty:       
            self.is_empty = True
            return randint(self.min_recup, self.max_recup)
        
        else:
            raise EmptyPotionError("Cannot drink an empty potion.")


if __name__ == "__main__":
    """Unit tests complete: check src/tests/test_potion.py"""