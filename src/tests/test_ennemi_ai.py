import pytest

from src.ennemy_ai import EnnemyAI
from src.character import Character
from src.exceptions import DeadCharacterError

def test_EnnemiAI_decide_action():
    ennemy = Character.thief()  #can drink potion and have 1 potion
    assert ennemy.stats.can_drink_potion
    assert ennemy.inventory.has_potion()
    
    #Simulate battles damage
    ennemy.stats.max_life = 100
    ennemy.current_life = 0
    ennemy_ai = EnnemyAI(ennemy)

    with pytest.raises(DeadCharacterError):
        ennemy_ai.decide_action()
        
    #Case <5% life remaining: always try to take a potion
    ennemy_ai.character.current_life = 1
    assert ennemy_ai.decide_action() == Character.ACTION_DRINKPOTION

    #Case <25% of life remaining: randomly decide 50/50 between ATTACK and DRINK_POTION
    ennemy_ai.character.current_life = 10   
    for i in range(1,21):
        decided_action = ennemy_ai.decide_action()
        print(f"Decided action {i}= {ennemy_ai.decide_action()}")
        assert decided_action in (Character.ACTION_ATTACK, Character.ACTION_DRINKPOTION)
 




    