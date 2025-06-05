import pytest

from src.potion import Potion
from src.exceptions import PoisonPotionError, EmptyPotionError
import src.constants as c

def test_Potion_init_with_two_numbers():
    assert isinstance(Potion(5, 10), Potion)
    assert isinstance(Potion(0, 0), Potion)

    with pytest.raises(PoisonPotionError):
        Potion(10, 5)

    with pytest.raises(PoisonPotionError):
        Potion(-1, 20)


def test_Potion_str():
    potion = Potion(5, 10)
    assert (f'entre {c.GREEN}5{c.RESET} et {c.GREEN}10{c.RESET} points de vie.' in str(potion))
 
    potion.drink()
    assert ('bouteille vide' in str(potion).lower())


def test_Potion_repr():
    potion = Potion(10, 20)
    assert (potion.__repr__() == 'Potion(10, 20)')


def test_Potion_drink():
    potion = Potion(0, 10)
    assert potion.is_empty == False
    assert potion.drink() >= 0
    assert potion.is_empty == True

    with pytest.raises(EmptyPotionError):
        potion.drink()  #call another time