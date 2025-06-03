import logging

from potion import Potion

class Bag(list):

    def __init__(self):
        """Create an empty Bag"""
        self = []

    def add(self, new_object: object):
        """Add the new object in the bag.

        Args:
            new_object (object): object or list of objects. A list will be extend to the bag.
        """
        if isinstance(new_object, list):
            self.extend(new_object)
        else:
            self.append(new_object)
    
    def get(self, object_to_remove: object):
        """ Get an object from the bag.

        Args:
            object_to_remove (object): Object to remove

        Returns:
            _type_: object or None if not found
        """
        try:
            self.remove(object_to_remove)
            return object_to_remove
        except ValueError:
            logging.info("Object not found in the bag.")
            return None

    def get_a_potion(self):
        """Return the first Potion found in the bag

        Returns:
            _type_: a Potion or None if not found
        """
        for object_in_bag in self:
            if isinstance(object_in_bag, Potion):
                potion = object_in_bag
                break
        else:
            return None
        
        return self.get(potion)
    
    
    def has_potion(self) -> bool:
        """Check if a potion is in the bag

        Returns:
            bool: True if a Potion is found, False otherwise
        """        
        for object_in_bag in self:
            if isinstance(object_in_bag, Potion):
                return True
        else:
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

    logging.basicConfig(level=logging.DEBUG)

    print("Inventaire 1, Bag() and .add(Potion(x,y)) 2x")
    my_inventory = Bag()
    potion1 = Potion(10,50)
    potion2 = Potion(5,15)
    my_inventory.add(potion1)
    my_inventory.add(potion2)
    print(f"Y a-t-il au moins une potion en inventaire? {my_inventory.has_potion()}")
    print(my_inventory)

    potion_out_of_bag = my_inventory.get(potion1)
    print(type(potion_out_of_bag))
    if isinstance(potion_out_of_bag, Potion):
        potion_out_of_bag.drink()

    print("-" * 40)

    print("Inventaire 2: Bag.potions(3,10,20)")
    my_inventory2 = Bag.with_potions(3, 10, 20)
    print(f"Y a-t-il au moins une potion en inventaire? {my_inventory2.has_potion()}")
    print(my_inventory2)

    print()
    print(f"Retrait d'une potion...")
    my_potion = my_inventory2.get_a_potion()
    print(type(my_potion))
    if isinstance(my_potion, Potion):
        my_potion.drink()
        #my_potion.drink()   #Raise EmptyPotionError
    else:
        print("Aucune potion.")

    print("-" * 40)