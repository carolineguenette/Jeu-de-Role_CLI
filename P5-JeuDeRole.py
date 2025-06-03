from random import randint

POINTS_VIE_INIT_JOUEUR = 50
POINTS_VIE_INIT_ENNEMI = 50
POTION_INIT_JOUEUR = 3
RECUP_POTION_MIN = 15
RECUP_POTION_MAX = 50
ATTAQUE_JOUEUR_MIN = 5
ATTAQUE_JOUEUR_MAX = 10
ATTAQUE_ENNEMI_MIN = 5
ATTAQUE_ENNEMI_MAX = 15

ACTION_ATTAQUER = "1"
ACTION_BOIREPOTION = "2"
ACTIONS = [ACTION_ATTAQUER, ACTION_BOIREPOTION]

nouvelle_partie = True

while nouvelle_partie:

    #Init debut de partie
    point_vie_joueur = POINTS_VIE_INIT_JOUEUR
    point_vie_ennemi = POINTS_VIE_INIT_ENNEMI
    potion_joueur = POTION_INIT_JOUEUR
    passer_tour_joueur = False
    partie_terminee = False

    print("DEBUT DE PARTIE")
    print(f"  Vous avez {potion_joueur} potion{'s' if potion_joueur > 1 else ''}.")
    print(f"  Joueur: {point_vie_joueur} point{'s' if point_vie_joueur >1 else ''} de vie")
    print(f"  Ennemi: {point_vie_ennemi} point{'s' if point_vie_ennemi >1 else ''} de vie")

    
    while not partie_terminee:

        print('*' * 50)

        #Premiere action: joueur
        reponse_actionjoueur = ""
            
        if not passer_tour_joueur:

            while reponse_actionjoueur not in ACTIONS:        
                reponse_actionjoueur = input("Souhaitez-vous attaquer ["+ACTION_ATTAQUER+"] ou utiliser une potion ["+ACTION_BOIREPOTION+"]? ")

                if reponse_actionjoueur == ACTION_ATTAQUER:
                    dommage = randint(ATTAQUE_JOUEUR_MIN, ATTAQUE_JOUEUR_MAX)
                    point_vie_ennemi -= dommage
                    print(f"Vous attaquez l'ennemi!. Vous faites {dommage} point{'s' if dommage>1 else ''} de dommage.")

                elif reponse_actionjoueur == ACTION_BOIREPOTION:
                    if potion_joueur > 0:
                        pointvie_recuperer = randint(RECUP_POTION_MIN, RECUP_POTION_MAX)
                        point_vie_joueur += pointvie_recuperer
                        potion_joueur -= 1
                        print(f"Vous buvez une potion et récupérez {pointvie_recuperer} point{'s' if pointvie_recuperer>1 else ''} de vie.")
                    else:
                        print("Oh non! Vous avez utilsé toutes vos potions de vie!")
                    passer_tour_joueur = True
                    break
                        
                else:
                    print("Choix d'action invalide.")
            
        else:
            print("Vous passez votre tour (vous avez bu une potion, ça prend du temps ça)...")
            passer_tour_joueur = False #prochain tour Ok

        #Deuxieme action: l'ennemi attaque si encore vivant
        if point_vie_ennemi > 0:
            dommage = randint(ATTAQUE_ENNEMI_MIN, ATTAQUE_ENNEMI_MAX)
            point_vie_joueur -= dommage
            print(f"L'ennemi vous attaque!. Vous subissez {dommage} point{'s' if dommage>1 else ''} de dommage.")

        #Verifier si la partie est terminee
        if point_vie_ennemi <= 0 or point_vie_joueur <= 0 :
            partie_terminee = True
            
            if point_vie_ennemi <=0:
                print("Vous avez GAGNÉ!!")
            else:
                print("Vous avez PERDU!")

            print(f"  Joueur: {point_vie_joueur} point{'s' if point_vie_joueur >1 else ''} de vie")
            print(f"  Ennemi: {point_vie_ennemi} point{'s' if point_vie_ennemi >1 else ''} de vie")

            reponse_rejouer = input("Souhaite-vous rejouer (o/n)? ")
            if reponse_rejouer == 'n' or reponse_rejouer == '':
                nouvelle_partie = False