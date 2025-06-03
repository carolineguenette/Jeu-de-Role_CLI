from random import randint
import logging

import constants_color

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
            logging.info(f'Création de la potion {repr(self)}.')
            
        else:
            raise PoisonPotionError(f"Magic potion do not exist (hum well...) so Potion(min_recup={min_recup}, max_recup={max_recup}) cannot be created.\n\tInit values must be : min_recup >= 0, max_recup >= 0 and min_recup <= max_recup")
        

    def __str__(self):
        if self.is_empty:
            return (f"Une très belle bouteille vide (Potion {constants_color.YELLOW}{self.id}{constants_color.RESET}).")
        else:
            return (f"{constants_color.BLUE}Potion {self.id}{constants_color.RESET} pouvant redonner entre {constants_color.GREEN}{self.min_recup}{constants_color.RESET} and {constants_color.GREEN}{self.max_recup}{constants_color.RESET} points de vie.")
        
    def __repr__(self):
        return f"Potion(min_recup={self.min_recup}, max_recup={self.max_recup}) - auto id : {self.id}"

        
    def __del__(self):
        logging.info(f'Destruction de la potion {self.id}!')

    def drink(self) -> int:
        """Action to drink the potion. Can be call only once.

        Raises:
            EmptyPotionError: Raise if drink is call more than one time

        Returns:
            int: Number of point of life gain
        """
        if not self.is_empty:
            logging.info(f"La potion {self.id} est bue...")
            self.is_empty = True
            return randint(self.min_recup, self.max_recup)
        else:
            logging.info("Tentative de boire une potion vide!")
            raise EmptyPotionError("Cannot drink an empty potion.")

class EmptyPotionError(Exception):
    pass

class PoisonPotionError(Exception):
    pass


if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG)

    a_potion = Potion(10,30)
    print(a_potion)

    super_potion = Potion(20,40)
    print(super_potion)
    print(f"Boire et retrouve {super_potion.drink()} points de vie.")
   # super_potion.boire() #Boire again: raise an error