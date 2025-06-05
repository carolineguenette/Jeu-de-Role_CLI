"""Wrapper around a list"""
import logging

from src.potion import Potion

logger = logging.getLogger(__name__)


class Inventory():

    def __init__(self):
        """Create an empty Inventory"""
        self._list = []


    def __len__(self):
        return len(self._list)


    def __iter__(self):
        return self._list.__iter__()


    def add(self, new_object: object):
        """Add the new object in the bag.

        Args:
            new_object (object): object or list of objects. A list of objects will be extend in the inventory.
        """
        if isinstance(new_object, list):
            logger.debug(f"Add items {new_object} in Inventory")
            self._list.extend(new_object)
        else:
            logger.debug(f"Add item {new_object} in Inventory")
            self._list.append(new_object)


    def get(self, object_to_remove: object):
        """Get an object from the bag.

        Args:
 i           object_to_remove (object): Object to remove

        Returns:
            _type_: object or None if not found
        """
        logger.debug(f"Inventory.get{object_to_remove}.")
        try:
            self._list.remove(object_to_remove)
            logger.debug("Object found in the inventory (return the object).")
            return object_to_remove
        except ValueError:
            logger.debug("Object not found in the inventory (return None).")
            return None
        

    def clear(self):
        self._list.clear()


    def get_a_potion(self):
        """Return the first Potion found in the bag

        Returns:
            _type_: a Potion or None if not found
        """
        for object_in_bag in self._list:
            if isinstance(object_in_bag, Potion):
                potion = object_in_bag
                return self.get(potion)
        return None
        
        
    
    
    def has_potion(self) -> bool:
        """Check if a potion is in the bag

        Returns:
            bool: True if a Potion is found, False otherwise
        """        
        for object_in_bag in self._list:
            if isinstance(object_in_bag, Potion):
                return True
        return False


    @classmethod
    def with_potions(cls, nb_of_potions: int, potion_min_recup: int, potion_max_recup: int):
        """Shortcut to create a bag of identical potions

        Args:
            total (int): Total number of potions to add in the bag
            potion_min_recup (int): The minimum recuperation life points of each potion
            potion_max_recup (int): The maximum recuperation life points of each potion

        Returns:
            _type_: Bag of Potions
        """
        potions_bag = cls()
        potions_bag.add( [Potion(potion_min_recup, potion_max_recup) for _ in range(nb_of_potions) ])
        return potions_bag


if __name__ == "__main__":

    """Unit tests complete: check src/tests/test_inventory.py"""