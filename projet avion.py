import tkinter as tk
import tkinter.messagebox as msg
import random as rd
from random import choice


racine = tk.Tk()
racine.title("Simulation d'avion")


#########################################
# CONSTANTES

CANVAS_HEIGHT = 600
CANVAS_WIDTH = 140
BORD_WIDHT = 420
COTE = 20

COULEUR_PASSAGER_0_BAGAGE = 'orchid1'
COULEUR_PASSAGER_1_BAGAGE = 'DarkOrchid2'
COULEUR_PASSAGER_2_BAGAGES = 'purple4'
COULEUR_SIEGE_VIDE = 'grey'
COULEUR_SIEGE_REMPLI = 'lawn green'
COULEUR_BORD = 'royalblue2'
COULEUR_BOUTON_BORD = 'white'
COULEUR_I = 'yellow'

NB_RANG = 30
NB_COLONNE = 7
NB_PASSAGERS_MAX = 180
X_COULOIR = 4
TPS_ETAPES = 50  # temps entre chaque étape


#########################################
# VARIABLES

mat_passagers = []  # Liste de tous les passages.
mat_2 = []
liste_passagers_in = []  # Liste des passagers actuellement dans l'avion.
interdit_x = [4]
interdit_y = []
count_x = []
count_y = []

compteur_passager = -1
compteur_passager_assis = 0
demarre = 1
nb_etape = 0


#########################################
# FONCTIONS

# Fonctions qui créent la liste des passagers au hasard


def passagers(mat):
    """Créer un passager [[destination], bagage, couleur] dans une matrice."""

    global mat_2, interdit_x, interdit_y

    # Coordonnées de leur siège/destination
    x = choice([i for i in range(1, 8) if i not in interdit_x])
    y = choice([i for i in range(1, 31) if i not in interdit_y])

    if [x, y] in mat_2:
        while [x, y] in mat_2:
            x = choice([i for i in range(1, 8) if i not in interdit_x])
            y = choice([i for i in range(1, 31) if i not in interdit_y])
    mat_2.append([x, y])
    mat.append([[x, y]])

    interdit(x, y)

    # Détermination au hasard du/des bagage(s) avec la couleur associée
    mat[-1].append(rd.randint(0, 2))

    if mat[-1][1] == 0:
        mat[-1].append(COULEUR_PASSAGER_0_BAGAGE)
    elif mat[-1][1] == 1:
        mat[-1].append(COULEUR_PASSAGER_1_BAGAGE)
    else:
        mat[-1].append(COULEUR_PASSAGER_2_BAGAGES)


def interdit(x, y):
    """Compte combien de fois x, y sont apparus.
    Si x est apparu 30 fois ou y est apparu 6 fois, il est enlevé des
    possibilités de choix pour les places."""

    global interdit_x, interdit_y, count_x, count_y

    count_x.append(x)
    count_y.append(y)

    if count_x.count(x) >= 30:
        interdit_x.append(x)
    if count_y.count(y) >= 6:
        interdit_y.append(y)


# Fonctions relatives au déplacement des passagers

def convertit_siege_identifiant(x, y):  # x pour la colonne, y pour le rang
    """Cette fonction prend en argument x et y qui sont les coordonnées d'une
    case de l'avion, puis convertit ces coordonnées en identifiant de canvas.
    Retourne l'identifiant du canevas."""

    global NB_COLONNE, NB_RANG

    identifiant = 0
    for i in range(1, NB_RANG+1):
        for j in range(1, NB_COLONNE+1):
            identifiant += 1
            if x == j and y == i:
                return identifiant


def entree_passager():
    """Prend en argument la liste d'un passager qui n'est pas encore dans l'avion.
    Teste si un nouveau passager peut entrer dans l'avion.
    Si oui il rentre et on ajoute ses coordonnées actuelles à la liste des
    passagers déjà dans l'avion. Sinon rien ne se passe."""

    global compteur_passager, liste_passagers_in, mat_passagers

    if (avion.itemcget((convertit_siege_identifiant(4, 1)), "fill"))\
            == COULEUR_SIEGE_VIDE:
        # Prend le passager suivant dans la liste de tous les passagers.
        compteur_passager += 1
        # Si tous les passagers ne sont pas encore dans l'avion
        if compteur_passager < NB_PASSAGERS_MAX:
            avion.itemconfigure(convertit_siege_identifiant(4, 1),
                                fill=mat_passagers[compteur_passager][2])
            liste_passagers_in.append(mat_passagers[compteur_passager])
            liste_passagers_in[compteur_passager].extend([[4, 1]])


def deplace_passagers_in():
    """Déplace tous les passagers qui sont actuellement dans l'avion. Fait entrer
    un passager si possible. La fonction est répétée tous les TPS_ETAPES.
    Permet également de compter le nombre d'étapes nécessaires à
    l'installation des passagers."""

    global compteur_passager_assis, nb_etape, liste_passagers_in

    # Compteur d'étapes
    if compteur_passager_assis < 180:
        nb_etape += 1
        compteur_etape()

    # Déplace tous les passagers
    if liste_passagers_in != []:
        for i in range(len(liste_passagers_in)):
            deplace_1_passager(liste_passagers_in, i)

        entree_passager()

    avion.after(TPS_ETAPES, lambda: deplace_passagers_in())


def convertisseur_couleur_case(x, y, couleur):
    """Prend en entrée les coordonnées x et y d'une case et une couleur.
    Puis associe cette couleur à la case."""

    avion.itemconfig((convertit_siege_identifiant(x, y)), fill=couleur)


def swipe_place(liste, n1, x_prime, y_prime):
    """Permet de faire échanger deux places à des passagers dans le cas où
    l'un bloque l'autre dans une rangée.
    Prend en arguments:
    liste --> la liste de tous les passagers acutellement dans l'avion.
    n1 --> l'indice de la liste correspondant au passager bloqué.
    x_prime --> la coordonnée x où veut aller le passager n1
    y_prime --> la coordonnée y où veut aller le passager n1"""

    global compteur_passager_assis

    # Le passager 2 est à sa place, il bloque le passage au passager 1.
    x_passager1 = liste[n1][3][0]
    y_passager1 = liste[n1][3][1]
    couleur1 = liste[n1][2]

    if [[x_prime, y_prime], 0, COULEUR_SIEGE_REMPLI, [x_prime, y_prime]]\
            in liste:
        # Cherche le passager avec qui n1 doit échanger sa place.
        n2 = liste.index([[x_prime, y_prime], 0,
                         COULEUR_SIEGE_REMPLI, [x_prime, y_prime]])
        # Passager 2 à sa place
        x_passager2 = liste[n2][3][0]
        y_passager2 = liste[n2][3][1]
        couleur2 = liste[n2][2]
        # Inverse les places des 2 passagers
        liste[n2][3][0], liste[n1][3][0] = x_passager1, x_passager2
        couleur2 = COULEUR_PASSAGER_0_BAGAGE
        convertisseur_couleur_case(x_passager2, y_passager2, couleur2)
        convertisseur_couleur_case(x_passager1, y_passager1, couleur1)
        compteur_passager_assis -= 1

    return liste


def deplace_1_passager(liste, n):  # [[x, y], bagage, couleur, [x', y']]
    """Prend en entrée la liste des passagers actuellement dans l'avion ainsi que
    l'indice auquel correspond le passager dans cette liste (noté n).
    Puis déplace ou non le passager en fonction d'où il se trouve dans l'avion.
    Permet aussi de faire déposer les bagages de passagers."""

    global compteur_passager_assis

    # Coordonnées du siège du passager
    coordonnees_final = liste[n][0]
    x_final = liste[n][0][0]
    y_final = liste[n][0][1]
    # Coordonnées actuelles du passager dans l'avion
    coordonnees_etape = liste[n][3]
    x_etape = liste[n][3][0]
    y_etape = liste[n][3][1]

    if coordonnees_final == coordonnees_etape:  # si passager à sa place
        pass
    elif (y_final) != (y_etape):  # si passager pas dans sa rangée.
        liste[n][3][1] += 1  # Va dans la rangée suivante.
        # Si la case suivante est occupée
        if (avion.itemcget((convertit_siege_identifiant
                            (x_etape, liste[n][3][1])), "fill"))\
                != COULEUR_SIEGE_VIDE:
            liste[n][3][1] -= 1
        else:
            convertisseur_couleur_case(x_etape,
                                       (liste[n][3][1]-1), COULEUR_SIEGE_VIDE)
            convertisseur_couleur_case(x_etape, liste[n][3][1], liste[n][2])

    elif y_final == y_etape:  # Si dans sa rangée
        if liste[n][1] == 0:  # si pas de bagages
            if x_final < X_COULOIR:
                # Siège du passager à gauche (par rapport au canvas)
                if (avion.itemcget((convertit_siege_identifiant
                                    (x_etape-1, y_etape)), "fill"))\
                                        == COULEUR_SIEGE_VIDE:
                    # Si pas de passager qui gène
                    convertisseur_couleur_case(x_etape, y_etape,
                                               COULEUR_SIEGE_VIDE)
                    # La case redevient vide
                    liste[n][3][0] -= 1
                else:  # Si passager assis gène le passage.
                    swipe_place(liste, n, x_etape-1, y_etape)

            else:
                # Siège du passager à droite (par rapport au canvas)
                if (avion.itemcget((convertit_siege_identifiant
                                    (x_etape+1, y_etape)), "fill"))\
                                        == COULEUR_SIEGE_VIDE:
                    # Si pas de passager qui gène
                    convertisseur_couleur_case(x_etape, y_etape,
                                               COULEUR_SIEGE_VIDE)
                    # La case redevient vide
                    liste[n][3][0] += 1
                else:  # Si passager assis gène le passage.
                    swipe_place(liste, n, x_etape+1, y_etape)

            # Si le passager a atteint son siège
            if coordonnees_final == coordonnees_etape:
                liste[n][2] = COULEUR_SIEGE_REMPLI
                compteur_passager_assis += 1
            convertisseur_couleur_case(liste[n][3][0], y_etape, liste[n][2])
            # La case suivante prend la couleur du passager

        else:  # si a des bagages
            liste[n][1] -= 1
            if liste[n][1] == 0:
                liste[n][2] = COULEUR_PASSAGER_0_BAGAGE
            elif liste[n][1] == 1:
                liste[n][2] = COULEUR_PASSAGER_1_BAGAGE
            convertisseur_couleur_case(x_etape, y_etape, liste[n][2])


# Fonctions utilisées par les boutons du canvas

def demarrer():
    """Fonction démarrant la simulation.
    Définit le temps par défaut et exécute la simulation."""
    global TPS_ETAPES
    TPS_ETAPES = 50
    entree_passager()
    deplace_passagers_in()


def arreter():
    """Fonction arrêtant la simulation : ferme la fenêtre."""
    racine.destroy()


def pause():
    """Definit un temps d'étapes tellement grand que
    la fonction est en virtuellement en pause."""
    global TPS_ETAPES
    TPS_ETAPES = 3000000


def relancer():
    """Remet le temps entre les étapes à zéro.
    Relance la simulation après l'avoir mis en pause."""
    global TPS_ETAPES
    TPS_ETAPES = 50
    deplace_passagers_in()


def etape_1():
    """Permet d'avancer la simulation d'une étape.
    Met en pause la fonction après une étape."""
    global TPS_ETAPES
    TPS_ETAPES = 300000
    deplace_passagers_in()


def etape_par_etape():
    """Augmente le temps entre étapes, par conséquent les étapes se succèdent
    une par une de manière distincte."""
    global TPS_ETAPES
    TPS_ETAPES = 500
    deplace_passagers_in()


def recommencer():
    """Permet de recommencer la simulation du début.
    Remet les variable à "zéro", crée une nouvelle liste de passagers."""
    global mat_passagers, mat_2, liste_passagers_in, interdit_x, interdit_y,\
        count_x, count_y, compteur_passager, compteur_passager_assis,\
        demarre, nb_etape

    # Remet tous les variables à "zéro"
    mat_passagers = []  # Liste de tous les passages
    mat_2 = []
    liste_passagers_in = []  # Liste des passagers actuellement dans l'avion.
    interdit_x = [4]
    interdit_y = []
    count_x = []
    count_y = []
    compteur_passager = -1
    compteur_passager_assis = 0
    demarre = 1
    nb_etape = 0
    compteur_etape()

    # Remet la couleur des sièges à "zéro".
    for j in range((NB_COLONNE*NB_RANG+1)):
        avion.itemconfig(j, fill=COULEUR_SIEGE_VIDE)

    # Crée nouvelle liste de passagers.
    for i in range(180):
        passagers(mat_passagers)
    entree_passager()


def aide():
    """Affiche la fenetre d'aide et son message."""
    msg.showinfo(title="Information",
                 message="Bienvenue dans la fenêtre d'information."
                 + 2*"\n" + "Gris = Siège vide." + "\n"
                 + "Vert = Passager correctement assis." + "\n"
                 + "Rose = Passager sans bagage." + "\n"
                 + "Violet clair = Passager avec 1 bagage." + "\n"
                 + "Violet foncé = Passager avec 2 bagages.")


def compteur_etape():
    """Change le label: nombre_etape2 pour l'actualiser, ce label affiche le
    nombre d'étapes."""
    global nb_etape
    nombre_etape2["text"] = nb_etape


# Fonction qui crée le quadrillage de l'avion.

def quadrillage():
    """ Fonction permettant de créer les cases représentant l'intérieur
    de l'avion, avec les cases de sièges et celles de couloir."""
    i = 0
    j = 0
    while j < CANVAS_HEIGHT:
        while i < CANVAS_WIDTH:
            avion.create_rectangle(i, j, i+COTE, j+COTE,
                                   fill=COULEUR_SIEGE_VIDE)
            i += COTE
        j += COTE
        i = 0


#########################################
# WIDGETS


avion = tk.Canvas(racine, height=CANVAS_HEIGHT, width=CANVAS_WIDTH)
bord = tk.Canvas(racine, height=35, width=BORD_WIDHT, bg=COULEUR_BORD)
# Boutons
bouton_demarrer = tk.Button(racine, text='Démarrer', command=demarrer,
                            relief="flat", bg=COULEUR_BORD,
                            fg=COULEUR_BOUTON_BORD, font=('helvetica', '13'))
bouton_arreter = tk.Button(racine, text='Arrêter', command=arreter,
                           relief="flat", bg=COULEUR_BORD,
                           fg=COULEUR_BOUTON_BORD, font=('helvetica', '13'))
bouton_pause = tk.Button(racine, text='Pause', command=pause,
                         font=('helvetica', '10'))
bouton_relancer = tk.Button(racine, text='Relancer', command=relancer,
                            font=('helvetica', '10'))
bouton_etape_1 = tk.Button(racine, text='Etape +1', command=etape_1,
                           font=('helvetica', '10'))
bouton_etape_par_etape = tk.Button(racine, text='Etape par étape',
                                   command=etape_par_etape,
                                   font=('helvetica', '10'))
bouton_recommencer = tk.Button(racine, text='Recommencer', command=recommencer,
                               relief="flat", bg=COULEUR_BORD,
                               fg=COULEUR_BOUTON_BORD,
                               font=('helvetica', '13'))
bouton_aide = tk.Button(racine, bitmap="info", command=aide,  relief="flat",
                        bg=COULEUR_BORD, fg=COULEUR_I)
# Compteur d'étapes
label_nombre_etape = tk.Label(racine, text="Nombre d'étapes :",
                              font=('helvetica', '13'))
nombre_etape2 = tk.Label(racine, text='0', font=('helvetica', '15'))


#########################################
# POSITIONNEMENT


avion.grid(row=2, rowspan=12, column=3, columnspan=4)
bord.grid(row=0, column=0, columnspan=15)
# Boutons
bouton_demarrer.grid(row=0, column=0)
bouton_arreter.grid(row=0, column=3)
bouton_pause.grid(row=3, column=0)
bouton_relancer.grid(row=3, column=1)
bouton_etape_1.grid(row=5, column=0)
bouton_etape_par_etape.grid(row=5, column=1)
bouton_recommencer.grid(row=0, column=1)
bouton_aide.grid(row=0, column=8)
# Compteur d'étapes
label_nombre_etape.grid(row=9, column=0, columnspan=1)
nombre_etape2.grid(row=9, column=1, columnspan=2)


avion.bind(quadrillage())


#########################################
for i in range(180):
    passagers(mat_passagers)

#########################################
# BONUS


def changespeed(speed):
    """Crée un slider qui permet d'ajuster le temps inter-étapes."""
    global TPS_ETAPES
    TPS_ETAPES = w1.get()


w1 = tk.Scale(racine, from_=0, to=200, orient="horizontal",
              label='Temps entre les étapes (en ms)',
              command=changespeed, length=200, font=('helvetica', '10'))
w1.set(50)
w1.grid(row=7, column=0, columnspan=2)


racine.mainloop()
