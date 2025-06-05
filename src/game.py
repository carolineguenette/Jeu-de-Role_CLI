"""Roleplay Game in command line."""

import logging

from src.character import Character, CharacterStats
from src.ennemy_ai import EnnemyAI
from src.inventory import Inventory
from src.utils import get_valid_user_input
import src.constants as c

logger = logging.getLogger("__name__")


class RoleplayGame:

    def __init__(self, player_character: Character, ennemy_characters: list[Character]):
        """Initialize the RoleplayGame

        Args:
            player_character (Character): The player. Must be a valid Character
            ennemy_characters (list[Character]): A list of ennemies. Must contains at least one ennemy
        """
        self._player = player_character
        self._ennemies = ennemy_characters
        self._tour_nb = 0

        logger.debug("Creation of RoleplayGame with the followings parameters:")
        logger.debug(self.settings_info)


    def play(self, print_settings = True):
        """Manage the game. Launch each tour until the game is over.

        Args:
            print_settings (bool, optional): If True, print the settings at the beginning of the game. Defaults to True.

        Raises:
            ValueError: player and ennnemies are not properly setup
        """
        #Valid if game setup is ok
        if not self._player or len(self._ennemies) <= 0:
            raise ValueError("Game cannot be start because the settings are invalids (player is missing or there is no ennemy). ")

        #Play!
        print("DÉBUT DE LA PARTIE")
        if print_settings:
            print("Voici les participants:")
            print(self.settings_info)

        while not self.gameover:
            self._turn()
        
        self._finalize_gameover()


    @property
    def settings_info(self) -> str:
        """Get the game settings. Read-Only property

        Returns:
            str: A multiple lines str that give all details about player and ennemy Characters and there inventory
        """
        str = "Joueur:\n"             
        str += f"  {self._player}"         #spaces before: for indent infos. Do not remove...
        str += ''.join([f"\n    {obj}" for obj in self._player.inventory])
        
        str +=  "\nEnnemi(s):"
        for ennemy in self._ennemies:
            str += f"\n  {ennemy}"
            str += ''.join([f"\n    {obj}" for obj in ennemy.inventory])

        return str


    def _turn(self):
        """Manage the game playing tour. Check if the pass tour rule must be apply. 
        Player plays, then ennemies. Display the tour recap at the end of the tour."""
        self._tour_nb += 1

        print(f"{c.BLUE}{'-' * 20} Tour {self._tour_nb} {'-' * 70}{c.RESET}")

        #Player play first
        print("C'est votre tour!")
        if self._player.took_a_potion:
            print(f"{c.MAGENTA}Vous{c.RESET} passez votre tour puisque vous avez fouillé votre sac pour une potion au tour précédent ⌛.")
            self._player.reset_took_a_potion()
            input('Appuyer sur retour pour continuer...')
        else:
            self._player_turn()
        
        #Ennemies play next
        print(f"C'est au tour {"des ennemies" if len(self._ennemies) >1 else "de l'ennemi."} ")
        for ennemy in self._ennemies:
            if ennemy.is_dead:
                print(f"{ennemy.name} est {c.RED}mort{c.RESET} 💀.")
                continue

            #Ennemy is alive
            if ennemy.took_a_potion:
                print(f"{ennemy.name} passe son tour puisqu'il a fouillé son sac pour une potion au tour précédent ⌛.")
                ennemy.reset_took_a_potion()
                continue

            self._ennemy_turn(ennemy)

        #Tour end: display life points of each Character
        print("Récapitulatif du tour:")
        print("\t"+ self._player.life_status)
        print('\n'.join(["\t"+ ennemy.life_status for ennemy in self._ennemies]))


    def _player_turn(self):
        """Ask action to do to user (between Attack and Drink a potion) and manage it
        """

        #Action choice
        #note: the ⚔️ seams to delete the next caracter: 2 spaces add in string
        player_answer = get_valid_user_input(f"Souhaitez-vous attaquer ⚔️  ({Character.ACTION_ATTACK}) ou boire une potion ✨ ({Character.ACTION_DRINKPOTION})? ", (Character.ACTION_ATTACK, Character.ACTION_DRINKPOTION))
        player_answer = int(player_answer)

        # Action management
        #   Attack
        if player_answer == Character.ACTION_ATTACK:
            
            #If there is more than 1 ennemy, need to ask the user which one he want to attack. Otherwise, there is only one annemy.
            if len(self._ennemies) > 1:
                self._display_ennemies()
                valid_choices = tuple(x for x in range(1, len(self._ennemies)+1)) 
                attack_ennemy_index = int(get_valid_user_input(f"Quel ennemi attaquez-vous {valid_choices}? ", valid_choices)) - 1   # -1 because display list begin to 1 (not 0)
            
            else:   #Only one ennemy : attack this one
                attack_ennemy_index = 0

            damage = self._player.attacks(self._ennemies[attack_ennemy_index])
            print(f"{c.MAGENTA}Vous{c.RESET} attaquez {self._ennemies[attack_ennemy_index].name} et lui faites {c.RED}{damage}{c.RESET} point{'s' if damage > 1 else ''} de dommage. ⚔️")
        
        #   Drink a potion
        elif player_answer == Character.ACTION_DRINKPOTION:
            life_pt_gain = self._player.drink_a_potion()

            if  life_pt_gain == Character.POTION_NOT_FOUND:
                #Comment: Changement dans règle -> si pas de potion alors pas de recup et perte du tour...
                print(f"{c.MAGENTA}Vous{c.RESET} avez fouillé votre sac mais il n'y a plus de potion. Vie: {self._player.life_status}.")
            else:
                print(f"{c.MAGENTA}Vous{c.RESET} buvez une potion et récupérez {c.GREEN}{life_pt_gain}{c.RESET} point{'s' if life_pt_gain > 1 else ''} de vie ❤️. Vie: {self._player.life_status}.")

        else:   #Just a safety display. This else should never be performed becaue every valid player_answer are already managed
            logger.error("Un événement qui ne devait pas se produire est survenu: le _tour_player semble mal géré.")
            print("Hein? Ça ne devrait pas se produire ça")


    def _ennemy_turn(self, ennemy: Character):
        """Manage the ennemy tour
        Certain ennemy can drink potion so EnnemiAI need to decide whick action to take between Attack and Drink potion.

        Args:
            ennemy (Character): _description_
        """

        # Action choice: Attack or Drink a potion
        if ennemy.stats.can_drink_potion:
            ennemy_ai = EnnemyAI(ennemy)
            action_to_do = ennemy_ai.decide_action()
        else:
            action_to_do = Character.ACTION_ATTACK
        
        # Action management
        #   Attack
        if action_to_do == Character.ACTION_ATTACK:
           damage = ennemy.attacks(self._player)
           print(f"{ennemy.name} vous attaque et fait {c.RED}{damage}{c.RESET} point{"s" if damage > 1 else ''} de dommage ⚔️")

        #   Drink potion
        elif action_to_do == Character.ACTION_DRINKPOTION:
            life_pt_gain = ennemy.drink_a_potion()

            if life_pt_gain == Character.POTION_NOT_FOUND:
                print(f"{ennemy.name} a fouillé son sac mais il n'y a plus de potion. Vie: {ennemy.life_status}.")
            else:
                print(f"{ennemy.name} récupère {c.GREEN}{life_pt_gain}{c.RESET} point{'s' if life_pt_gain > 1 else ''} de vie ❤️. Vie: {ennemy.life_status}).")


    def _finalize_gameover(self):
        """Display the final gameover status result"""

        print(f"{c.BLUE}{'-' * 20} 🏁 Fin de partie 🏁 {'-' * 50}{c.RESET}")
        
        if self._player.is_dead:
            print("Vous avez PERDU 💀")
        else:
            print("Vous avez GAGNÉ 🏆!")


    def _display_ennemies(self):
        """Display the ordered list of ennemies. Useful to let the user choose who he wants to attack"""
        print(f"Liste des ennemies:")
        print('\n'.join( [f"\t{i+1}. {ennemy}" for i, ennemy in enumerate(self._ennemies) ]))


    @property
    def _all_ennemies_are_dead(self) -> bool:
        for ennemy in self._ennemies:
            if not ennemy.is_dead:
                return False
        return True


    @property
    def gameover(self) -> bool:
        return self._all_ennemies_are_dead or self._player.is_dead


    @classmethod
    def default_settings(cls, player_name = "Joueur", ennemy_name = "Ennemi"):
        """A shortcut to create a valid default game setup

        Args:
            player_name (str, optional): Player name. Defaults to "Joueur".
            ennemy_names (tuple, optional): Ennemy names. Defaults to ("Ennemi 1","Ennemi 2").

        Returns:
            _type_: A RoleplayGame ready to be play.
        """
        player = Character(player_name, 
                    CharacterStats(max_life=c.DEFAULT_LIFE_PTS_INIT_PLAYER, 
                                   attack_min=c.DEFAULT_ATTACK_PLAYER_MIN,
                                   attack_max=c.DEFAULT_ATTACK_PLAYER_MAX, 
                                   can_drink_potion=True),
                    Inventory.with_potions(nb_of_potions=c.DEFAULT_POTION_NB_INIT_JOUEUR, 
                                    potion_min_recup=c.DEFAULT_POTION_RECUP_MIN,
                                    potion_max_recup=c.DEFAULT_POTION_RECUP_MAX)
                )
        
        ennemy = Character(ennemy_name, 
                    CharacterStats(max_life=c.DEFAULT_LIFE_PTS_INIT_ENNEMY, 
                                   attack_min=c.DEFAULT_ATTACK_ENNEMY_MIN,
                                   attack_max=c.DEFAULT_ATTACK_ENNEMY_MAX, 
                                   can_drink_potion=False),
                    Inventory())

        return cls(player, [ennemy])


    @classmethod
    def settings_with_two_weak_ennemies(cls, player_name = "Joueur", ennemy_names = ("Ennemi 1","Ennemi 2")):
        """A shortcut to create a valid setup game with two weak ennemies and a default player

        Args:
            player_name (str, optional): Player name. Defaults to "Joueur".
            ennemy_names (tuple, optional): Ennemy names. Defaults to ("Ennemi 1","Ennemi 2").

        Returns:
            _type_: A RoleplayGame ready to be play.
        """
        player = Character(player_name, 
                    CharacterStats(max_life=c.DEFAULT_LIFE_PTS_INIT_PLAYER, 
                                   attack_min=c.DEFAULT_ATTACK_PLAYER_MIN,
                                   attack_max=c.DEFAULT_ATTACK_PLAYER_MAX, 
                                   can_drink_potion=True),
                    Inventory.with_potions(nb_of_potions=c.DEFAULT_POTION_NB_INIT_JOUEUR, 
                                potion_min_recup=c.DEFAULT_POTION_RECUP_MIN,
                                potion_max_recup=c.DEFAULT_POTION_RECUP_MAX)
                )
        
        ennemy1 = Character(ennemy_names[0], 
                    CharacterStats(max_life=20, 
                                   attack_min=0,
                                   attack_max=8, 
                                   can_drink_potion=True),
                    Inventory.with_potions(nb_of_potions=1,
                                    potion_min_recup=c.DEFAULT_POTION_RECUP_MIN,
                                    potion_max_recup=c.DEFAULT_POTION_RECUP_MAX))

        ennemy2 = Character(ennemy_names[1], 
                    CharacterStats(max_life=20, 
                                   attack_min=0,
                                   attack_max=8, 
                                   can_drink_potion=True),
                    Inventory())

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
