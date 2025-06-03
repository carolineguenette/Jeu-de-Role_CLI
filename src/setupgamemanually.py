"""Setup a RolePlayGame by the user, in terminal.
- call create() to begin the creation of a setup
- get is_valid to check if a valid RolePlayGame setup has been created correctly
- get config to have a string representation of the actual setup
"""
from src.utils import get_valid_user_input, get_nonempty_string_input, get_valid_int_input
from src.character import Character
from src.potion import Potion
import src.constants_color as c

class SetupGameManually():

    CREATE_OR_MODIF_PERSO = 1
    CREATE_PREDEFINED_ENNEMY = 2
    CREATE_ENNEMY = 3
    MODIF_ENNEMY = 4
    DELETE_ENNEMY = 5
    DISPLAY_CONFIG = 6
    END_CONFIG = 7
    INVALID_CHOICE = 0

    ENNEMY_STANDARD = 1
    ENNEMY_GOBELIN = 2
    ENNEMY_THIEF = 3
    ENNEMY_DRAGON = 4

    CREATED = True
    MODIFIED = False

    def __init__(self):
        """ Init setup game manually"""

        #self.player : initialize during creation process 
        self.ennemmies = []


    def create(self):
        """Loop on options util the user finish his setup (create, modify or delete characters, display the current configuration). 
        The possible actions are defined as constants class. The final setup can be invalid when user finish.
        """
        print()
        print('*' * 20 + " Configuration manuelle " + '*' * 30)

        answer = self.INVALID_CHOICE
        while answer != SetupGameManually.END_CONFIG:

            valid_settings_choice = SetupGameManually._display_settings_menu()
            answer = int(get_valid_user_input(f"Choix ({SetupGameManually.CREATE_OR_MODIF_PERSO}-{SetupGameManually.END_CONFIG}) ", valid_settings_choice))
            print()

            match answer:
                case SetupGameManually.CREATE_OR_MODIF_PERSO:
                    create_or_modify = self._create_or_modif_player()     #create_or_modif always succeed. The 
                    print(f"Le personnage {self.player.name} a été {'créé' if create_or_modify==SetupGameManually.CREATED else 'modifié'}.\n")

                case SetupGameManually.CREATE_PREDEFINED_ENNEMY:
                    self._create_a_predefined_ennemy()
                    print(f"L'ennemi {self.ennemmies[len(self.ennemmies)-1].name} a été créé et ajouté aux ennemies à affronter.\n" )

                case SetupGameManually.CREATE_ENNEMY:
                    new_ennemy = Character.default_ennemy()
                    self.ennemmies.append(new_ennemy)
                    SetupGameManually._modif_character(new_ennemy, is_ennemy=True)
                    print(f"L'ennemi {new_ennemy.name} a été créé et ajouté aux ennemies à affronter.\n" )

                case SetupGameManually.MODIF_ENNEMY:
                    self._modify_or_delete_an_ennemy('modify')
                    #final print status is in the method...

                case SetupGameManually.DELETE_ENNEMY:
                    self._modify_or_delete_an_ennemy('delete')
                    #final print status is in the method...

                case SetupGameManually.DISPLAY_CONFIG:
                    print(self.config + "\n")
                
                case SetupGameManually.END_CONFIG:
                    answer = self.END_CONFIG if self._finalize_config() else self.INVALID_CHOICE
                    print() #Make some blank space for lisibilty...


    @property
    def config(self) -> str:
        """Get the current config with character info and inventory details

        Returns:
            str: A multilines str description of player, ennemies and there respective inventory
        """
        temp_str = "JOUEUR:"

        if hasattr(self, 'player'):
            temp_str += f"\n{SetupGameManually._get_character_and_inventory_info(self.player)}"
        else:
            temp_str += "\nLe personnage du joueur n'a pas encore été créé."

        temp_str += "\nENNEMIE(S):"
        if self.ennemmies:  #= len(self.ennemies) > 0
            temp_str += ''.join( [f"\n{SetupGameManually._get_character_and_inventory_info(ennemy)}" for ennemy in self.ennemmies])

        else:
            temp_str += "\nAucun ennemi n'a encore été créé."

        return temp_str

    @property
    def is_valid(self) -> bool:
        """Check if the current setup is valid

        Returns:
            bool: True if the current setup have a player and at least one ennemy
        """
        return hasattr(self, 'player') and len(self.ennemmies) > 0


    def _create_or_modif_player(self) -> bool:
        """Create or modify the player. The process will always succeed.

        Returns:
            str: 'CREATED' (True) or 'MODIFIED' (False: the player has been modified successfully)
        """
        creation_process = False
        if not hasattr(self, "player"):
            self.player = Character.player_without_any_potion() #The default_player has potion: player_without_any_potion create a more basic player so we take this one
            creation_process = True
        SetupGameManually._modif_character(self.player, is_ennemy=False)

        return SetupGameManually.CREATED if creation_process else SetupGameManually.MODIFIED


    def _create_a_predefined_ennemy(self):
        """Create a predefined ennemy and add it to the ennemy setup. The process will always succeed
        """
        
        valid_ennemies_choice = SetupGameManually._display_predefined_ennemies_menu()
        answer = int(get_valid_user_input(f"Choix ({SetupGameManually.ENNEMY_STANDARD}-{SetupGameManually.ENNEMY_DRAGON}) ", valid_ennemies_choice))

        match answer:
            case SetupGameManually.ENNEMY_STANDARD:
                new_ennemy = Character.default_ennemy()
            case SetupGameManually.ENNEMY_GOBELIN:
                new_ennemy = Character.gobelin()
            case SetupGameManually.ENNEMY_THIEF:
                new_ennemy = Character.thief()
            case SetupGameManually.ENNEMY_DRAGON:
                new_ennemy = Character.dragon()

        self.ennemmies.append(new_ennemy)


    def _modify_or_delete_an_ennemy(self, type:str):
        """Ask the user which ennemy must be modify of delete and launch the process to alter the enemy. Print back feedback to user.
        The process can be cancel by the user before the selection of the ennemy to alter.

        Args:
            type (str): 'modify' or 'delete'
        """
        nb_ennemies = len(self.ennemmies)
        if nb_ennemies > 0:
            self._display_ennemies_menu()
            
            range_choices_str = f'1-{nb_ennemies}' if nb_ennemies > 1 else '1'
            cancel_choice = 'ou retour pour annuler'
            valid_choices = tuple((i for i in range(1,nb_ennemies+1))) + ('',)
            
            ennemy_index_plus1 = get_valid_user_input(f"Quel ennemi souhaitez-vous {'modifier' if type =='modify' else 'supprimer'} ({range_choices_str } {cancel_choice})? ", valid_choices)
            if ennemy_index_plus1:
                ennemy_index_plus1 = int(ennemy_index_plus1)

                if type == 'modify':
                    SetupGameManually._modif_character(self.ennemmies[ennemy_index_plus1 - 1], is_ennemy=True)
                else: # type == 'delete'
                    self.ennemmies.pop(ennemy_index_plus1 - 1)

                print(f"L'ennemi {ennemy_index_plus1} a été {'modifié'if type =='modify' else 'supprimé'}.\n" )
            else:
                print(f"{'Modification' if type =='modify' else 'Suppression'} d'un ennemi annulée\n")
        else:
            print(f"Il n'y a aucun ennemi à {'modifier' if type =='modify' else 'supprimer'} pour le moment.\n")


    def _finalize_config(self) -> bool:
        """Ask the user if the final setup is correct. The user can confirm and exit the setup or continue the setup

        Returns:
            bool: True is finalyze is done, False if user want to continue doing configuration
        """
        confirm_config_end = False
        if get_valid_user_input("Souhaitez-vous afficher la configuration finale? (o/n) ", ('o', 'n')) == 'o':
            confirm_config_end = True
            print(self.config)

        setup_done = True
        if not self.is_valid:
            print("La configuration actuelle n'est pas valide.")
            setup_done = get_valid_user_input("Souhaitez-vous vraiment annuler la configuration? (o/n) ", ('o', 'n')) == 'o'

        elif confirm_config_end:
            setup_done = get_valid_user_input("Souhaitez-vous terminer avec cette configuration? (o/n) ", ('o', 'n')) == 'o'
        
        return setup_done


    def _display_ennemies_menu(self):
        """List the ennemies in an ordered list beginning wih 1
        """
        print('\n'.join([f"{i+1}. {ennemy}" for i, ennemy in enumerate(self.ennemmies)]) )


    @staticmethod
    def _modif_character(character: Character, is_ennemy: bool):
        """Ask all the information about the character to setup it, including his inventory of potions

        Args:
            character (Character): The Character to setup
            is_ennemy (bool): True if it's an ennemy, False if it's the player character
        """
        character.name = get_nonempty_string_input(f"Nom {"de l'ennemi" if is_ennemy else 'du personnage'}: ")
        character.stats.max_life = get_valid_int_input("Nombre de points de vie: ")[0]
        character.current_life = character.stats.max_life

        attacks_nb = get_valid_int_input("Attaque min et max (séparés par un espace): ", nb_of_int=2, valid_ascending_order=True)
        character.stats.attack_min = attacks_nb[0]
        character.stats.attack_max = attacks_nb[1]

        if is_ennemy:
            character.stats.can_drink_potion = get_valid_user_input(f"Cet ennemi peut-il boire des potions? (o/n): ", ('o', 'n')) == 'o'
        else: 
            character.stats.can_drink_potion = True   #The player Character can always drink potion

        if character.stats.can_drink_potion:
            character.inventory.clear() #We recreate the inventory
            potions_nb = get_valid_int_input("Nombre de potion(s) dans l'inventaire: ", valid_higher_than_0=False)    #Pourrait etre 0
            for i in range(potions_nb[0]):
                potion_params = get_valid_int_input(f"Paramètres de récupération de la potion {i+1} (min et max, séparés par un espace) ", nb_of_int=2, valid_ascending_order=True)
                potion = Potion(potion_params[0], potion_params[1])
                character.inventory.append(potion)
                

    @staticmethod
    def _get_character_and_inventory_info(character) -> str:
        """All the informations about a character and his inventory

        Args:
            character (_type_): the Character

        Returns:
            str: A multilines string with all the stats, current state and inventory or the character
        """
        temp_str = ''
        temp_str += f"{character}"  
        temp_str += ''.join([f"\n    {obj}" for obj in character.inventory ])
        return temp_str


    @staticmethod
    def _display_settings_menu() -> tuple:
        """Display the settings menu

        Returns:
            tuple: Valid setting choices
        """
        print(f"{'-' * 20} Menu principal de la configuration {'-' * 20}")
        print(f"{SetupGameManually.CREATE_OR_MODIF_PERSO}. Créer ou modifier mon personnage")
        print(f"{SetupGameManually.CREATE_PREDEFINED_ENNEMY}. Créer un ennemi prédéfini")
        print(f"{SetupGameManually.CREATE_ENNEMY}. Créer un ennemi")
        print(f"{SetupGameManually.MODIF_ENNEMY}. Modifier un ennemi")
        print(f"{SetupGameManually.DELETE_ENNEMY}. Supprimer un ennemi")
        print(f"{SetupGameManually.DISPLAY_CONFIG}. Afficher ma configuration")
        print(f"{SetupGameManually.END_CONFIG}. Terminer la configuration")

        return (SetupGameManually.CREATE_OR_MODIF_PERSO, SetupGameManually.CREATE_PREDEFINED_ENNEMY, SetupGameManually.CREATE_ENNEMY, SetupGameManually.MODIF_ENNEMY, SetupGameManually.DELETE_ENNEMY, SetupGameManually.DISPLAY_CONFIG, SetupGameManually.END_CONFIG)


    @staticmethod
    def _display_predefined_ennemies_menu() -> tuple:
        """Display a ordered list of the available predefined ennemies

        Returns:
            tuple: Valide ennemies choices
        """
        print(f"{'-' * 10} Menu des ennemies prédéfinis {'-' * 10}")
        print(f"{SetupGameManually.ENNEMY_STANDARD}. Créer un ennemi standard")
        print(f"{SetupGameManually.ENNEMY_GOBELIN}. Créer un gobelin")
        print(f"{SetupGameManually.ENNEMY_THIEF}. Créer un voleur")
        print(f"{SetupGameManually.ENNEMY_DRAGON}. Créer un dragon")

        return (SetupGameManually.ENNEMY_STANDARD, SetupGameManually.ENNEMY_GOBELIN, SetupGameManually.ENNEMY_THIEF, SetupGameManually.ENNEMY_DRAGON)

    
if __name__ == '__main__':
    manual_settings = SetupGameManually()

    print("Print de la configuration courante (devrait etre '...pas encore été créé'):")
    print(manual_settings.config)
    print(f"La configuration est-elle valide (devrait être False)? {manual_settings.is_valid}")
    
    manual_settings.create()
