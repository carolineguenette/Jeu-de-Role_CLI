# Games constants
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

#Codes to print color text in CLI
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"
DARKGRAY = "\033[90m"
RESET = "\033[0m"



if __name__ == "__main__":

    print(f"This text is {RED}RED{RESET}.")
    print(f"This text is {GREEN}GREEN{RESET}.")
    print(f"This text is {YELLOW}YELLOW{RESET}.")
    print(f"This text is {BLUE}BLUE{RESET}.")
    print(f"This text is {MAGENTA}MAGENTA{RESET}.")
    print(f"This text is {CYAN}CYAN{RESET}.")
    print(f"This text is {WHITE}WHITE{RESET}.")
    print(f"This text is {DARKGRAY}DARKGRAY{RESET}.")

    