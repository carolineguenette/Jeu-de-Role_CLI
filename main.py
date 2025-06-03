"""Main entry point of the program.
"""

from src.setupgame import SetupGame
from src.utils import get_valid_user_input

def main():
    """Let the user choose or create a setup game and play this game. 
    Loop until user choose to stop the program. The user can choose to use the same previous setup or new setup."""
    
    print("BIENVENUE - JEU DE RÔLE EN LIGNE DE COMMANDE")
    
    #Init
    setup = SetupGame()

    #Main loop: plain again
    user_want_to_play = True
    user_want_a_new_setup = True
    while user_want_to_play:

        if user_want_a_new_setup:
            setup.create()

        if setup.is_valid:
            game = setup.game

            #If user create a new setup, confirm it's OK, otherwise, juste begin the game
            if user_want_a_new_setup:   
                print(game.settings_info)
                if get_valid_user_input("Souhaitez-vous jouer avec ces paramètres (o/n)? ", ('o', 'n')) == 'o':
                    print() #put some space between sections...
                    game.play(print_settings=False)

            else:
                game.play()

        else:
            print("La configuration du jeu est invalide. Cette partie ne peut pas démarrer.")
    
        user_want_to_play = get_valid_user_input("Souhaitez-vous continuer à jouer (o/n)? ", ('o', 'n')) == 'o'
        print() #just a line to put some space between sections

        if user_want_to_play and setup.is_valid:
            user_want_a_new_setup = not get_valid_user_input("Souhaitez-vous jouer avec les mêmes paramètres (o/n)? ", ('o', 'n')) == 'o'
            print()




if __name__ == "__main__":
    main()
    
