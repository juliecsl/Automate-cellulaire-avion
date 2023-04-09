# Projet remplissage d'un avion par automates cellulaires
## Présentation du projet
Modélisation d'une interface graphique d'un avion mono-couloir avec 3 sigèes de chaque coté du couloir.
Une cellule peut etre une cellule de couloir ou de siège. Les cellules du centre sont celles du couloirs les autres sont des sièges. 

Une cellule ne peut contenir qu'un passager à la fois. Un passager a une destination (son siège) et entre zéro et deux bagages qu'il doit déposer dans un coffre. A chaque simulation un numéro de siège est aléatoirement attribué au passager.

Un passager avance dans le couloir de 1 cellule par unité de temps, s'il n'y a personne sur la cellule suivante, sinon il est bloqué à cet instant.

Un seul passager peut entrer dans l'avion par unité de temps. Dès que l'entrée est vide un nouveau passager arrive si l'avion n'est pas plein.

Lorsque le passager a fini de s'avancer dans le couloir, il doit ranger ses bagages avant de rejoindre son siège. Déposer un bagage prend une unité de temps, pendant ce temps là le passager reste dans le couloir et bloque le couloir.

Le remplissage de l'avion s'arrete quand tous les passagers sont assis à leur place.

## Prérequis
* Version Python: 3.8.16
* Librairies: ```tkinter``` et ```random```(déjà installées par défaut)

## Execution
Pour executer le programme il faut utiliser un interpréteur python tel que VSCODE.
Une fois le fichier .py executer, l'interface graphique s'ouvre vous pouvez alors cliquer sur les boutons suivants:
* Démarrer: démarre la simulation
* Pause: met en pause la simulation
* Arreter: ferme l'interface graphique
* Recommencer: recommence la simulation
* Etape +1: pour avancer d'une unité de temps
* i : pour avoir des informations complémentaires

## Interpréation de l'interface graphique
Voici la signification des couleurs présentes lors de la simulation:
* Gris: siège vide
* Vert: passager assis
* Rose: passager sans bagage
* Violet: passager avec 1 bagage
* Violet foncé: passager avec 2 bagages

