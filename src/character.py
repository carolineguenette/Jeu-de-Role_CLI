from dataclasses import dataclass
from random import randint
import logging
from typing import Self

from src.inventory import Inventory
from src.potion import Potion
from src.exceptions import InvalidNameError, InvalidStatsError, DeadCharacterError, UnabledToDrinkPotionError
import src.constants as c

logger = logging.getLogger(__name__)

@dataclass
class CharacterStats:
    """Dataclass of Stat's Character

    Raises:
        InvalidNameError: A ValueError. Max life must be >0, stat cannot be negative and min must be lower than max
    """
    max_life: int
    attack_min: int
    attack_max: int
    can_drink_potion: bool

    def __post_init__(self):
        if self.max_life <= 0:
            raise InvalidStatsError("Maximum life points cannot be 0 or negative.")
        elif self.attack_min < 0:
            raise InvalidStatsError("Minimum attack's points cannot be negative.")
        elif self.attack_max < 0:
            raise InvalidStatsError("Maximum attack's points cannot be negative.")
        elif self.attack_min > self.attack_max:
            raise InvalidStatsError("Minimum attack's points must be lower than the maximum attack's point.")
        

class Character:
    """A Character for the RoleplayGame

    Raises:
        InvalidNameError: The name cannot be an empty string
        DeadCharacterError: Action cannot be done if the character is dead
        UnabledToDrinkPotionError: There is no potion in inventory
    """
    POTION_NOT_FOUND:int = -1   #Must be an integer <0 (valid return is >=0)

    ACTION_ATTACK = 1
    ACTION_DRINKPOTION = 2

    def __init__(self, name: str, stats: CharacterStats, inventory: Inventory = Inventory()):
        """Create a Character with his stats and an inventory

        Args:
            name (str): Name of the character. Raise an error if it's an empty string.
            stats (CharacterStats): Stats that define the Character. Stats do not change over time
            inventory (Inventory): Inventory of the Character. Default: Empty Inventory
        """

        self.name = name
        self.stats = stats
        self.inventory = inventory
        self.current_life = stats.max_life
        self._took_a_potion = False


    def __str__(self):
        """Get a description of the character, without details about his inventory
        Returns:
            _type_: return a one line string about the caracter
                ex: Joueur a 50/50 pts de vie, fait des attaques enre 10 et 15 pts de dommage et a 3 potions.
        """
        
        #Temporary variables for lisibility (long string caracters!)
        attack_info = f"des attaques entre {c.RED}{self.stats.attack_min}{c.RESET} et {c.RED}{self.stats.attack_max}{c.RESET} pts de dommage"
        nb_potions = len(self.inventory)     #Inventory can only contains Potion object for now.

        if self.stats.can_drink_potion:
            drink_potion_status = f"a {c.CYAN}{nb_potions}{c.RESET} potion{'s' if nb_potions > 1 else ''}"
        else:
            drink_potion_status = f"ne sait pas boire de potion"

        return (f"{self.life_status}, fait {attack_info} et {drink_potion_status}.")


    @property
    def who(self) -> str:
        """Get all informations about the character. Read-only stats
        Returns:
            str: A multiple lines string about the character, with inventory details
        """
        infos = f"{str(self)}"
        infos += ''.join([f"\n  {obj}" for obj in self.inventory])
        return infos


    @property
    def name(self):
        """Name

        Returns:
            _type_: A Yellow string name
        """
        return c.YELLOW + self._name + c.RESET
    

    @name.setter
    def name(self, name_value: str):
        if not name_value:
            raise InvalidNameError("The name cannot be an empty string")
        self._name = name_value


    @property
    def is_dead(self) -> bool:
        """Check if the caracter is dead

        Returns:
            bool: True if alive (current_life > 0), False otherwise
        """
        return self.current_life <= 0


    @property
    def life_status(self) -> str:
        """Life status. The current life is in green and a skull symbol is display at the end if player is dead 

        Returns:
            str: return examples: 
                    Player a 0/50 pts de vie 💀
                    Name a 20/35 pts de vie
        """
        return f"{self.name} a {c.GREEN}{self.current_life}{c.RESET}/{self.stats.max_life} pts de vie{' 💀' if self.is_dead else ''}"

    @property
    def took_a_potion(self) -> bool:
        return self._took_a_potion


    def attacks(self, ennemy:Self) -> int:
        """Attack another character by a random number of damage according to stats attack. The damage is reflect on ennemy.

        Args:
            ennemy (Character): The Caracter attacked

        Raises:
            DeadCharacterError: Action cannot be done if the caracter is dead

        Returns:
            int: Number of points of dammage
        """
        if self.is_dead:
            raise DeadCharacterError(f"Unable to attack because the character {self.name} is dead.")
        
        dammage = randint(self.stats.attack_min, self.stats.attack_max)
        ennemy._be_attacked(dammage)
        
        logger.info(f"{self.name} attacks {ennemy.name} and makes {dammage} point{"s" if dammage>1 else ''} of damage.")
        return dammage


    def _be_attacked(self, damage:int):
        """Action to do if the character is been attacked. Internal method
        By now, damage is apply directly on Caracter

        Args:
            dammage (int): Number of pts of damage inflicted to character
        """
        self.current_life = self.current_life - damage if self.current_life - damage > 0 else 0


    def drink_a_potion(self) -> int:
        """Drink a potion and gain current life point. After being drink, the potion is no more available in inventory (throw away)

        Raises:
            DeadCharacterError: Action cannot be done if the caracter is dead

        Returns:
            int: Number of point recovery by the potion or POTION_NOT_FOUND if no potion is available
        """
        if self.is_dead:
             raise DeadCharacterError(f"Unable to drink a potion because {self.name} is dead.") 

        if not self.stats.can_drink_potion:
            raise UnabledToDrinkPotionError(f"Unable to drink a potion because {self.name} is defined as unabled to drink a potion.")

        self._took_a_potion = True   #Even if the player has no potion: he search the bag for a potion so flag it
        potion = self.inventory.get_a_potion()

        if not isinstance(potion, Potion):
            logger.info("Unable to drink a potion because inventory contains none.")
            return Character.POTION_NOT_FOUND

        #The character is alive, can drink potion and a potion is found in inventory. Drink it and increase current life
        nb_pt_life_gain = potion.drink()
        self.current_life = nb_pt_life_gain + self.current_life if nb_pt_life_gain + self.current_life < self.stats.max_life else self.stats.max_life
        return nb_pt_life_gain


    def reset_took_a_potion(self): 
        self._took_a_potion = False


    @classmethod
    def default_player(cls, name: str = "Joueur"):
        """A shorcut to create a Default Player Character

        Args:
            name (str, optional): Name of the player. Defaults to "Joueur".

        Returns:
            Character: the character with predefined stats
        """
        return Character(name, 
                       CharacterStats(max_life=50, attack_min=5, attack_max=10, can_drink_potion=True), 
                       Inventory.with_potions(3,15, 50))
    
    
    @classmethod
    def player_without_any_potion(cls, name: str = "Joueur"):
        """A shorcut to create a Player Character with an empmty inventory

        Args:
            name (str, optional): _description_. Defaults to "Joueur".

        Returns:
            Character: the character with predefined stats
        """
        return Character(name, 
                       CharacterStats(max_life=50, attack_min=5, attack_max=10, can_drink_potion=True), 
                       Inventory())        


    @classmethod
    def default_ennemy(cls, name: str = "Ennemi"):
        """Shortcut to create a default ennemy character.
        The default ennemy cannot drink potion.

        Returns:
            Character: A Default ennemy Character
        """
        stats = CharacterStats(max_life=50, attack_min=5, attack_max=15, can_drink_potion=False)
        return cls(name, stats,  Inventory())


    @classmethod
    def dragon(cls, name: str = "Dragon"):
        """Shortcut to create a Dragon character

        Returns:
            Character: A Dragon Character
        """
        stats = CharacterStats(max_life=350, attack_min=0, attack_max=60, can_drink_potion=False)
        return cls(name, stats,  Inventory()) 


    @classmethod
    def gobelin(cls, name: str = "Gobelin"):
        """Shortcut to create a Gobelin character

        Returns:
            Character: A Gobelin Character
        """
        stats = CharacterStats(max_life=35, attack_min=2, attack_max=10, can_drink_potion=True)
        bag = Inventory.with_potions(nb_of_potions=2, potion_min_recup=10, potion_max_recup=35)
        return cls(name, stats,  bag)


    @classmethod
    def thief(cls, name: str = "Voleur"):
        """Shortcut to create a Thief character.
        Thief have 1 potion in inventory.

        Returns:
            Character: A Thief Character
        """
        stats = CharacterStats(max_life=60, attack_min=0, attack_max=25, can_drink_potion=True)
        bag = Inventory.with_potions(nb_of_potions=1, potion_min_recup=15, potion_max_recup=50)
        return cls(name, stats, bag)
    



if __name__ == "__main__":
    """Unit tests complete: check src/tests/test_character.py"""
    