def get_valid_user_input(question: str, valid_answers: tuple) -> str:
    # NOTES: POUrrait retourner le string converti directement.
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
    ask_again = True
    while ask_again:
        answer = input(question)

        if not answer:
            print('Valeur invalide (chaîne de caractère vide)')
        ask_again = not answer

    return answer


def get_int_input(question: str, nb_of_int: int = 1, valid_higher_than_0: bool = True, valid_ascending_order: bool = False) -> list[int]:
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
    answer = get_int_input("Entrer 1 int: ", 1, valid_higher_than_0=True)
    print(answer)

    answer = get_int_input("Entrer 2 int (x y): ", 2, valid_higher_than_0=True, valid_ascending_order=False)
    print(answer)

    answer = get_int_input("Entrer 3 int séparés par des espaces: ", 3, valid_higher_than_0=True, valid_ascending_order=True)
    print(answer)


