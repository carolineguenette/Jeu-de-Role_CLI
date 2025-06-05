from src.inventory import Inventory
from src.potion import Potion
from src.utils import is_iterable


def test_Inventory_additem_len_get():

    inventory = Inventory()
    assert(len(inventory) == 0)

    inventory.add("something")
    assert(len(inventory) == 1)

    inventory.add(False)
    assert(len(inventory) == 2)

    assert(inventory.get("something") == "something")
    assert(len(inventory) == 1)

    assert(inventory.get("not there") == None)
    assert(len(inventory) == 1)

    assert(inventory.get(False) == False)
    assert(len(inventory) == 0)


def test_Inventory_addlist_len_get():
    inventory = Inventory()
    assert(len(inventory) == 0)

    inventory.add([])
    assert(len(inventory) == 0)

    inventory.add([1,2,3])
    assert(len(inventory) == 3)

    inventory.add([4,5])
    assert(len(inventory) == 5)

    assert(inventory.get(5) == 5)
    assert(len(inventory) == 4)

    assert(inventory.get(10) == None)
    assert(len(inventory) == 4)


def test_Inventory_is_collection():
    inventory = Inventory()
    inventory.add([1,2,3])
    assert 3 in inventory
    assert 10 not in inventory
    

def test_Inventory_is_iterable():
    inventory = Inventory()
    assert is_iterable(inventory)

    inventory.add([1,2,3])

    for index, value in enumerate(inventory, start=1):
        if index == 1:
            assert value == 1


def test_Inventory_get_and_has_a_potion():
    inventory = Inventory()
    assert inventory.has_potion() == False

    #Insert 2 potions and anything else between them
    inventory.add(Potion(1,11))
    inventory.add(["something else", Potion(2,22)])
    assert inventory.has_potion() == True

    #Get the first potion
    potion = inventory.get_a_potion()
    assert isinstance(potion, Potion)
    assert potion.min_recup == 1

    #Get the second potion (skip "something else" and remove the next item)
    potion = inventory.get_a_potion()
    assert isinstance(potion, Potion)
    assert potion.min_recup == 2

    #Check if has_potion while the inventory is not empty (has "something else")
    assert inventory.has_potion() == False
    potion = inventory.get_a_potion()
    assert potion == None


def test_Inventory_with_potions_classmethod():
    inventory = Inventory.with_potions(2, 10, 20)
    assert inventory.has_potion() == True

    potion = inventory.get_a_potion()
    assert isinstance(potion, Potion)
    assert potion.min_recup == 10