"""Main entry point of the program.
"""

from src.setup_game import SetupGame
from src.utils import get_valid_user_input

def main():
    """Let the user choose or create a setup game and play this game. 
    Loop until user choose to stop the program. The user can choose to use the same previous setup or a new setup."""
    
    print("BIENVENUE - JEU DE RÔLE EN LIGNE DE COMMANDE")
    
    #Init
    user_want_to_play = True
    user_want_a_new_setup = True
    user_create_a_new_setup = False
    while user_want_to_play:

        if user_want_a_new_setup:
            setup = SetupGame()
            setup.create()
            user_create_a_new_setup = True

        play_game(setup, user_create_a_new_setup)
    
        user_want_to_play = get_valid_user_input("Souhaitez-vous continuer à jouer (o/n)? ", ('o', 'n')) == 'o'
        print() #just a line to put some space between sections

        if user_want_to_play and setup.is_valid:
            user_want_a_new_setup = not get_valid_user_input("Souhaitez-vous jouer avec les mêmes paramètres (o/n)? ", ('o', 'n')) == 'o'

            if not user_want_a_new_setup:
                user_create_a_new_setup = False
            print()

    print("Aurevoir!")


def play_game(setup: SetupGame, is_new_setup: bool):
    if not setup.is_valid:
        print("La configuration du jeu est invalide. Cette partie ne peut pas démarrer.")
        return
    
    game = setup.get_game()

    if not is_new_setup:
        game.play(print_settings=True)
        return
    
    print(game.settings_info + "\n")
    if get_valid_user_input("Souhaitez-vous jouer avec ces paramètres (o/n)? ", ('o', 'n')) == 'n':
        print("Partie annulée.")
        return
        
    game.play(print_settings=False)
        
    


if __name__ == "__main__":
    main()
    
