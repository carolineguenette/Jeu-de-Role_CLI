"""Utils methods
"""

def get_valid_user_input(question: str, valid_answers: tuple) -> str:
    """Ask question to user and loop until the answer is in valid_answers.
    Print "Choix invalide" as feedback if the answer is not valid

    Args:
        question (str): The str give to the input method
        valid_answers (tuple): Every acceptable answer to the question. Must be a type convertible to str.

    Returns:
        str: str entered by the user, that is in the valid_answers
    """
    #Init
    valid_str_answers = []

    #Convert valid_answers to str to be able to compare with input return
    for value in valid_answers:
        valid_str_answers.append(str(value))

    ask_again = True
    while ask_again:
        answer = input(question)

        if answer not in valid_str_answers:
            print('Choix invalide.')
            ask_again = True
        else:
            ask_again = False

    return answer


def get_nonempty_string_input(question: str) -> str:
    """Ask question to user and loop until the answer is not a empty string.
    Print 'Valeur invalide (chaîne de caractère vide)' as feedback if invalid entry

    Args:
        question (str): The str give to the input method
 
    Returns:
        str: the user answer, that will not be an empty string
    """
    ask_again = True
    while ask_again:
        answer = input(question)

        if not answer:
            print('Valeur invalide (chaîne de caractère vide)')
        ask_again = not answer

    return answer


def get_valid_int_input(question: str, nb_of_int: int = 1, valid_higher_than_0: bool = True, valid_ascending_order: bool = False) -> list[int]:
    """_summary_

    Args:
        question (str):  The str display to the user (in the input method)
        nb_of_int (int, optional): how many int is expected, separated by a space. Defaults to 1.
        valid_higher_than_0 (bool, optional): If True, method will validate that the number is not 0. Defaults to True.
        valid_ascending_order (bool, optional): If T,rue, method will validate that the first number is lower than the second, etc (ascending order). Defaults to False.

    Returns:
        list[int]: A list of nb_of_int integers
    """
    int_answers = []
    is_valid = False

    while not is_valid:
        answer = input(question)

        #Validations
        split_answer_on_space = answer.split(" ")

        #First: check numbers of entries is the number of int expected
        still_valid_continue_validation = len(split_answer_on_space) == nb_of_int
 
        #Second: try to convert every entries to int
        if still_valid_continue_validation:
            for value in split_answer_on_space:
                try:
                    int_answers.append(int(value))
                except ValueError:
                    still_valid_continue_validation = False
                    break

        #Third: check if every int_value are higher than 0
        if still_valid_continue_validation and valid_higher_than_0:
            for int_value in int_answers:
                if int_value <= 0:
                    still_valid_continue_validation = False
                    break
        
        #Fourth and last: check numeric ascending order
        if still_valid_continue_validation and valid_ascending_order:
            for i, value in enumerate(int_answers):
                #value must be >= to previous value.
                if i != 0: 
                    if int_value < int_answers[i-1]:
                        still_valid_continue_validation = False
                        break

        if still_valid_continue_validation: #Everything is valid and validation is done
            is_valid = True
        else: 
            #Error message: explain what is valid. Use of temporary variable for lisibility
            msg_base = f"Valeur{'s' if nb_of_int > 1 else ''} invalide{'s' if nb_of_int > 1 else ''}."
            msg_nb = f"{nb_of_int} chiffre{'s' if nb_of_int > 1 else ''} entier{'s' if nb_of_int > 1 else ''}"
            msg_higher_than_0 = f"{' > 0' if valid_higher_than_0 else ''}"
            msg_ascending_order = f"{' en ordre croissant' if valid_ascending_order else ''}"
            msg_expected = f"{'sont' if nb_of_int > 1 else 'est'} attendu{'s' if nb_of_int > 1 else ''}"
            msg_separator = f"{', séparés par un espace' if nb_of_int > 1 else ''}"

            print(f'{msg_base} {msg_nb}{msg_higher_than_0}{msg_ascending_order} {msg_expected}{msg_separator}.')
            int_answers = []
            is_valid = False
        
    return int_answers


if __name__ == "__main__":

#    answer = get_valid_user_input("Choix option (1 ou 2): ", (1,2))
#    answer = get_nonempty_string_input("Entrer votre nom: ")
    answer = get_valid_int_input("Entrer 1 int: ", 1, valid_higher_than_0=True)
    print(answer)

    answer = get_valid_int_input("Entrer 2 int (x y): ", 2, valid_higher_than_0=True, valid_ascending_order=False)
    print(answer)

    answer = get_valid_int_input("Entrer 3 int séparés par des espaces: ", 3, valid_higher_than_0=True, valid_ascending_order=True)
    print(answer)


