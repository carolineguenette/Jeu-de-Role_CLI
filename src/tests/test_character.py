import pytest

from src.character import Character, CharacterStats
from src.inventory import Inventory
from src.potion import Potion
from src.exceptions import InvalidNameError, InvalidStatsError, DeadCharacterError, UnabledToDrinkPotionError
import src.constants as c

def test_CharacterStat_init():

    with pytest.raises(InvalidStatsError):
        CharacterStats(max_life=0, attack_min=10, attack_max=20, can_drink_potion=True)

    with pytest.raises(InvalidStatsError):
        CharacterStats(max_life=50, attack_min=-1, attack_max=10, can_drink_potion=True)

    with pytest.raises(InvalidStatsError):
        CharacterStats(max_life=50, attack_min=10, attack_max=-1, can_drink_potion=False)

    with pytest.raises(InvalidStatsError):
        CharacterStats(max_life=50, attack_min=20, attack_max=10, can_drink_potion=True)
    
    stats = CharacterStats(max_life=1, attack_min=0, attack_max=0, can_drink_potion=True)
    assert isinstance(stats, CharacterStats)

    stats = CharacterStats(max_life=50, attack_min=0, attack_max=40, can_drink_potion=True)
    assert isinstance(stats, CharacterStats)


def test_Character_init():
    valid_stats = CharacterStats(max_life=40, attack_min=10, attack_max=20, can_drink_potion=True)
    inventory = Inventory.with_potions(5, 10, 20)

    with pytest.raises(InvalidNameError):
        Character('', valid_stats)

    assert isinstance(Character('Name', valid_stats), Character)
    assert isinstance(Character('Name', valid_stats, inventory), Character)

    
def test_Character_who():
    valid_stats = CharacterStats(max_life=50, attack_min=0, attack_max=30, can_drink_potion=True)
    inventory = Inventory()
    inventory.add(['AAA', 'BBB'])
    character = Character('My name', valid_stats, inventory)

    assert('My name' in character.who)
    assert('BBB' in character.who)
    assert('CCC' not in character.who)


def test_Character_attacks_and_be_attacked():
    ENNEMY_LIFE_POINTS = 20
    valid_stats = CharacterStats(max_life=50, attack_min=30, attack_max=35, can_drink_potion=True)
    player = Character('My name', valid_stats)

    valid_stats = CharacterStats(ENNEMY_LIFE_POINTS, 10, 20, False)
    ennemy = Character("Fake Ennemi", valid_stats)

    damage = player.attacks(ennemy)
    assert damage >= player.stats.attack_min and damage <= player.stats.attack_max
    assert ennemy.current_life == ENNEMY_LIFE_POINTS - damage or ennemy.current_life == 0

    player.current_life = 0  #Simulate death
    with pytest.raises(DeadCharacterError):
        damage = player.attacks(ennemy)


def test_Character_is_dead_and_life_status():
    valid_stats = CharacterStats(max_life=50, attack_min=0, attack_max=30, can_drink_potion=True)
    character = Character('My name', valid_stats)

    assert character.is_dead == False

    character.current_life = 0
    assert character.is_dead == True

    assert(f"{c.GREEN}{character.current_life}{c.RESET}/{character.stats.max_life}" in character.who)


def test_Character_drink_a_potion():
    character = Character('My name', CharacterStats(20, 10, 20, False))
    
    character.current_life = 0  #Dead caracter
    with pytest.raises(DeadCharacterError):
        character.drink_a_potion()

    character.current_life = 10
    character.stats.can_drink_potion = False
    with pytest.raises(UnabledToDrinkPotionError):
        character.drink_a_potion()

    character = Character.player_without_any_potion()
    recovery_pts = character.drink_a_potion()
    assert character.took_a_potion == True
    assert recovery_pts == Character.POTION_NOT_FOUND

    inventory = Inventory()
    for _ in range(10):
        potion = Potion(50,50)
        inventory.add(potion)
    
    character = Character("My name", CharacterStats(50, 50, 50, True), inventory)
    for _ in range(10):
        recovery_pts = character.drink_a_potion()
        assert recovery_pts == 50
        assert character.current_life <= character.stats.max_life


def test_Character_factory():
    character = Character.default_player("A name")
    assert "A name" in character.name

    character = Character.default_ennemy("A name")
    assert "A name" in character.name

    character_without_potion = Character.player_without_any_potion()
    assert isinstance(character, Character)

    dragon = Character.dragon()
    assert isinstance(dragon, Character)

    gobelin = Character.gobelin()
    assert isinstance(gobelin, Character)

    thief = Character.thief()
    assert isinstance(thief, Character)