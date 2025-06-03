"""Setup a RolePlayGame by a user, in terminal.
- A RoleplayGame object is available after a call of the create method (if user do not cancel during setup process) by the game property.
- Check if settings are valid before getting the game otherwise a ValueError will be raised.
- It's possible de display directly the available game settings. This method will need to be modify if more predefined setting game are create in 
  the RolePlayGame class.
"""
import copy

from game import RoleplayGame
from setupgamemanually import SetupGameManually
from utils import get_valid_user_input


class SetupGame:
    """Let the user choose a preconfigure setup or create a new setup.

    Raises:
        ValueError: when trying to get the RoleplayGame (game property getter) while the setup is not valid
    """
    SETTINGS_DEFAULT = 1
    SETTINGS_TWO_WEAKS_ENNEMIES = 2
    SETTINGS_MANUAL = 3
    CANCEL = ''

    def __init__(self):
        self._game = None


    def create(self) -> bool:
        """Create a new setup for the game. 
        Ask the user to choose a setup for a RoleplayGame between pre-setup game or a new manual setup configuration.
        If creation is cancel, the setup will not be valid.

        Returns:
            bool: True if creation succeed with a valid game object, False otherwise
        """
        valid_setting_choices = self.display_possible_game_settings()
        valid_choices = valid_setting_choices + (SetupGame.CANCEL,)
        setting_choice = get_valid_user_input("Veuillez choisir une option de configuration pour le jeu (ou retour pour annuler): ", valid_choices)

        if setting_choice == SetupGame.CANCEL:
            self._game = None
            print("Configuration du jeu annulée")

        else:
            setting_choice = int(setting_choice)
            match setting_choice:
                case SetupGame.SETTINGS_DEFAULT:
                    self._game = RoleplayGame.default_settings()
                
                case SetupGame.SETTINGS_TWO_WEAKS_ENNEMIES:
                    self._game = RoleplayGame.settings_with_two_weak_ennemies()
                
                case SetupGame.SETTINGS_MANUAL:
                    manual_settings = SetupGameManually()
                    manual_settings.create()
                    if manual_settings.is_valid:
                        self._game = RoleplayGame(manual_settings.player, manual_settings.ennemmies)

            if self.is_valid:
                return  True
            
        return False


    @property
    def info(self) -> str:
        """Info about the current setup
        
        Returns:
            str: Player and ennemies infos on ultiple lines or 'Configuration invalide' if game setup is not done
        """
        if isinstance(self._game, RoleplayGame):
            return self._game.settings_info
        return 'Configuration invalide'


    @property
    def is_valid(self) -> bool:
        return isinstance(self._game, RoleplayGame)


    @property
    def game(self) -> RoleplayGame:
        """A RoleplayGame object ready to be play, as setup during the creation process. Read-only property.
        Check if is_valid before getting.

        Raises:
            ValueError: when trying to access the property while the game setups are not valid.

        Returns:
            RoleplayGame: A copy of the RoleplayGame object
        """
        if isinstance(self._game, RoleplayGame):    #Note: if we used is_valid instead, deepcopy do not reconize that the None is eliminated and parse a possible error
            return copy.deepcopy(self._game)
        raise ValueError("The game is not setup properly.")
        

    def display_possible_game_settings(self) -> tuple:
        """Display the possible games settings

        Returns:
            tuple: Valid possible choices of settings
        """
        print("Configurations possibles: ")
        print(f"  {SetupGame.SETTINGS_DEFAULT}. Jeu par défaut")
        print(f"  {SetupGame.SETTINGS_TWO_WEAKS_ENNEMIES}. Jeu avec deux adversaires faibles")
        print(f"  {SetupGame.SETTINGS_MANUAL}. Configuration manuelle")
    
        return (SetupGame.SETTINGS_DEFAULT, SetupGame.SETTINGS_TWO_WEAKS_ENNEMIES, SetupGame.SETTINGS_MANUAL)




if __name__ == "__main__":
    setup = SetupGame()

    #setup.display_possible_game_settings()
    print(f"Setup est valide (False attendu)? : {setup.is_valid}")

    #print(f"Setup info ('Setup invalide' attendu):{setup.info}")    
    #game = setup.game   #Raise ValueError: setup is not done yet

    setup.create()
    print(f"Setup est valide? : {setup.is_valid}")
    print(f"Setup info: \n{setup.info}")

    #Simulate a game end...
    if isinstance(setup.is_valid, RoleplayGame):
        game = setup.game
        game.player.current_life = 0
        game.player.inventory.clear()

    print(f"Setup info after a simulate game (must be the same): \n{setup.info}")
  
    