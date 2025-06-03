"""Roleplay Game in command line."""

import logging

from character import Character, CharacterStats
from ennemy_ai import EnnemyAI
from inventory import Bag
from utils import get_valid_user_input
import constants_color as c

DEFAULT_LIFE_PTS_INIT_PLAYER = 50
DEFAULT_LIFE_PTS_INIT_ENNEMY = 50
DEFAULT_POTION_NB_INIT_JOUEUR = 3
DEFAULT_POTION_NB_INIT_ENNEMY = 0
DEFAULT_POTION_RECUP_MIN = 15
DEFAULT_POTION_RECUP_MAX = 50
DEFAULT_ATTACK_PLAYER_MIN = 5
DEFAULT_ATTACK_PLAYER_MAX = 10
DEFAULT_ATTACK_ENNEMY_MIN = 5
DEFAULT_ATTACK_ENNEMY_MAX = 15

class RoleplayGame:

    def __init__(self, player_character: Character, ennemy_characters: list[Character]):
        self.player = player_character
        self.ennemies = ennemy_characters
        self.tour_nb = 0


    def play(self, print_settings = True):
        """Manage the game. Launch each tour until the game is over.

        Args:
            print_settings (bool, optional): Indicated to print the settings at the beginning of the game. Defaults to True.

        Raises:
            ValueError: player and ennnemies are not properly setup
        """
        if self.player and len(self.ennemies) > 0:

            print("DÉBUT DE LA PARTIE")
            if print_settings:
                print("Voici les participants:")
                print(self.settings_info)

            while not self.gameover:
                self._tour()
            
            self._finalize_end()
        else:
            raise ValueError("Game cannot be start because the settings are invalids (player is missing or there is no ennemy. ")


    @property
    def settings_info(self) -> str:
        """Get the game settings

        Returns:
            str: A multiple lines str that give all details about player and ennemy Characters and there inventory
        """
        str = "Joueur:\n"             
        str += f"  {self.player}"         #spaces before: for indent infos. Do not remove...
        str += ''.join([f"\n    {obj}" for obj in self.player.inventory])
        
        str +=  "\nEnnemi(s):"
        for ennemy in self.ennemies:
            str += f"\n  {ennemy}"
            str += ''.join([f"\n    {obj}" for obj in ennemy.inventory])

        return str


    def _finalize_end(self):
        print(f"{c.BLUE}{'-' * 20} 🏁 Fin de partie 🏁 {'-' * 50}{c.RESET}")
        
        if self.player.is_dead:
            print("Vous avez PERDU 💀")
        else:
            print("Vous avez GAGNÉ 🏆!")


    def _tour(self):
        """Manage the game playing tour. Check if the pass tour rule must be apply. 
        Player plays, then ennemies. Display the tour recap at the end of the tour."""
        self.tour_nb += 1

        print(f"{c.BLUE}{'-' * 20} Tour {self.tour_nb} {'-' * 70}{c.RESET}")

        #Player play always first
        print("C'est votre tour!")
        if not self.player.took_a_potion:
            self._tour_player()

        else:
            print(f"{c.MAGENTA}Vous{c.RESET} passez votre tour puisque vous avez fouillé votre sac pour une potion au tour précédent ⌛.")
            self.player.reset_took_a_potion()
            get_valid_user_input('Appuyer sur retour pour continuer...', ('',))
        
        #Ennemies play next
        print(f"C'est au tour {"des ennemies" if len(self.ennemies) >1 else "de l'ennemi."} ")
        for ennemy in self.ennemies:
            if not ennemy.is_dead:

                if not ennemy.took_a_potion:
                    self._tour_ennemy(ennemy)
                else:
                    print(f"{ennemy.name} passe son tour puisqu'il a fouillé son sac pour une potion au tour précédent ⌛.")

            else:
                print(f"{ennemy.name} est {c.RED}mort{c.RESET} 💀.")

        #Tour end: display life points of each Character
        print("Récapitulatif du tour:")
        print("\t"+ self.player.life_status)
        for ennemy in self.ennemies:
            print("\t"+ ennemy.life_status)


    def _tour_player(self):

        #Action choice
        #note: the ⚔️ seams to delete the next caracter: 2 spaces add in string
        player_answer = get_valid_user_input(f"Souhaitez-vous attaquer ⚔️  ({Character.ACTION_ATTACK}) ou utliser une potion ✨ ({Character.ACTION_DRINKPOTION})? ", Character.ACTIONS)
        
        # Action management
        if player_answer == Character.ACTION_ATTACK:
            if len(self.ennemies) > 1:
                self._display_ennemies()
                valid_choice = tuple(str(x) for x in range(1, len(self.ennemies)+1))
                valid_choice_display = tuple(x for x in range(1, len(self.ennemies)+1)) #To display a tuple without the '' around str value...

                attack_ennemy_index = int(get_valid_user_input(f"Quel ennemi attaquez-vous {valid_choice_display}? ", valid_choice)) - 1   # -1 because display list begin to 1 (not 0)
            else:
                attack_ennemy_index = 0 #Only one ennemy : attack this one

            damage = self.player.attacks(self.ennemies[attack_ennemy_index])
            print(f"{c.MAGENTA}Vous{c.RESET} attaquez {self.ennemies[attack_ennemy_index].name} et lui faites {c.RED}{damage}{c.RESET} point{'s' if damage > 1 else ''} de dommage. ⚔️")
        
        elif player_answer == Character.ACTION_DRINKPOTION:
            life_pt_gain = self.player.drink_a_potion()

            if  life_pt_gain == Character.POTION_NOT_FOUND:
                #Comment: Changement dans règle -> si pas de potion alors pas de recup et perte du tour...
                print(f"{c.MAGENTA}Vous{c.RESET} avez fouillé votre sac mais il n'y a plus de potion. Vie: {self.player.life_status}.")
            else:
                print(f"{c.MAGENTA}Vous{c.RESET} buvez une potion et récupérez {c.GREEN}{life_pt_gain}{c.RESET} point{'s' if life_pt_gain > 1 else ''} de vie ❤️. Vie: {self.player.life_status}.")

        else:   #Just a safety display. This else should never be performed becaue every valid player_answer are already managed
            logging.error("Un événement qui ne devait pas se produire est survenu: le _tour_player semble mal géré.")
            print("Hein? Ça ne devrait pas se produire ça")


    def _tour_ennemy(self, ennemy: Character):
        
        # Action choice
        ennemy_ai = EnnemyAI(ennemy)
        action_to_do = ennemy_ai.decide_action()
        
        # Action management
        if action_to_do == Character.ACTION_ATTACK:
           damage = ennemy.attacks(self.player)
           print(f"{ennemy.name} vous attaque et fait {c.RED}{damage}{c.RESET} point{"s" if damage > 1 else ''} de dommage ⚔️")

        elif action_to_do == Character.ACTION_DRINKPOTION:
            life_pt_gain = ennemy.drink_a_potion()

            if life_pt_gain == Character.POTION_NOT_FOUND:
                print(f"{ennemy.name} a fouillé son sac mais il n'y a plus de potion. Vie: {ennemy.life_status}.")
            else:
                print(f"{ennemy.name} récupère {c.GREEN}{life_pt_gain}{c.RESET} point{'s' if life_pt_gain > 1 else ''} de vie ❤️. Vie: {ennemy.life_status}).")


    def _display_ennemies(self):
        print(f"Liste des ennemies:")
        for i, ennemy in enumerate(self.ennemies):
            print(f"\t{i+1}. {ennemy}")


    @property
    def _all_ennemies_are_dead(self) -> bool:
        for ennemy in self.ennemies:
            if not ennemy.is_dead:
                return False
        return True


    @property
    def gameover(self) -> bool:
        return self._all_ennemies_are_dead or self.player.is_dead


    @classmethod
    def default_settings(cls, player_name = "Joueur", ennemy_name = "Ennemi"):

        player = Character(player_name, 
                    CharacterStats(max_life=DEFAULT_LIFE_PTS_INIT_PLAYER, 
                                   attack_min=DEFAULT_ATTACK_PLAYER_MIN,
                                   attack_max=DEFAULT_ATTACK_PLAYER_MAX, 
                                   can_drink_potion=True),
                    Bag.with_potions(nb_of_potions=DEFAULT_POTION_NB_INIT_JOUEUR, 
                                    potion_min_recup=DEFAULT_POTION_RECUP_MIN,
                                    potion_max_recup=DEFAULT_POTION_RECUP_MAX)
                )
        
        ennemy = Character(ennemy_name, 
                    CharacterStats(max_life=DEFAULT_LIFE_PTS_INIT_ENNEMY, 
                                   attack_min=DEFAULT_ATTACK_ENNEMY_MIN,
                                   attack_max=DEFAULT_ATTACK_ENNEMY_MAX, 
                                   can_drink_potion=False),
                    Bag())

        return cls(player, [ennemy])


    @classmethod
    def settings_with_two_weak_ennemies(cls, player_name = "Joueur", ennemy_names = ("Ennemi 1","Ennemi 2")):

        player = Character(player_name, 
                    CharacterStats(max_life=DEFAULT_LIFE_PTS_INIT_PLAYER, 
                                   attack_min=DEFAULT_ATTACK_PLAYER_MIN,
                                   attack_max=DEFAULT_ATTACK_PLAYER_MAX, 
                                   can_drink_potion=True),
                    Bag.with_potions(nb_of_potions=DEFAULT_POTION_NB_INIT_JOUEUR, 
                                potion_min_recup=DEFAULT_POTION_RECUP_MIN,
                                potion_max_recup=DEFAULT_POTION_RECUP_MAX)
                )
        
        ennemy1 = Character(ennemy_names[0], 
                    CharacterStats(max_life=20, 
                                   attack_min=0,
                                   attack_max=8, 
                                   can_drink_potion=True),
                    Bag.with_potions(nb_of_potions=1,
                                    potion_min_recup=DEFAULT_POTION_RECUP_MIN,
                                    potion_max_recup=DEFAULT_POTION_RECUP_MAX))

        ennemy2 = Character(ennemy_names[1], 
                    CharacterStats(max_life=20, 
                                   attack_min=0,
                                   attack_max=8, 
                                   can_drink_potion=True),
                    Bag())

        return cls(player, [ennemy1, ennemy2])


if __name__ == "__main__":
    
    logging.basicConfig(level=logging.DEBUG, filename='game.log', filemode='w')

    # game = RoleplayGame.default_settings()
    # game.start()

    game = RoleplayGame.settings_with_two_weak_ennemies()
    game.play()

    # print(f"all ennemies dead (must be False): {game._all_ennemies_are_dead}")
    # print(f"Fin de partie (must be False): {game.end_of_game}")

    # game.ennemies[0].current_life = 0
    # game.ennemies[1].current_life = 0
    # print(f"all ennemies dead (must be True): {game._all_ennemies_are_dead}")
    # print(f"Fin de partie (must be True): {game.end_of_game}")
