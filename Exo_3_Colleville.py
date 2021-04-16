###Auteur : Tanguy Colleville
import time as time

import matplotlib.pyplot as plt 
import numpy as np 
import seaborn as sns 
from tkinter.filedialog import *
from z3 import * 


csp=Solver()## initilisation du solver

def lecture_grille(filepath):## Fonction qui lie la grille et créer les variables contraintes à partir d'un filepath vers un fichier txt
    grid = []
    with open(filepath, 'r') as textfile:# lecture en mode reading
        compteur_ligne=0
        for line in textfile:
            liste_ligne=[]
            compteur_colonne=0
            for element in line :
                if element!="\n":
                    if element=="1" :# si on a une valeur imposée on la rentre comme valeur fixée
                        liste_ligne.append(1)
                    elif element=="0":
                        liste_ligne.append(0)
                    else : # sinon on déclare la case comme une variable
                        liste_ligne.append(Int("T{},{}".format(compteur_ligne,compteur_colonne)))
                        csp.add(Or(liste_ligne[-1]==0,liste_ligne[-1]==1))# on ajoute la contrainte de binarité par la même occasion
                    compteur_colonne+=1
            compteur_ligne+=1
            grid.append(liste_ligne)
    return grid

filename = askopenfilename(title="Ouvrir une grille",filetypes=[('text files','.txt')])##récupération du chemin de la grille

t1=time.time()## Lancement du chrono afin de connaitre le temps de résolution du problème
ma_grille=lecture_grille(filename) ## on prépare la grille et déclare les variables du problème à partir du filepath du fichier selectionné par l'utilisateur

N=len(ma_grille[1])# on récupère la dimension de la grille
Ma_somme=Sum(ma_grille[1])## on récupère une somme quelqueconque qui va nous servir de référence pour connaitre le nombre de zéros et de uns un peu de la même manière que pour l'exercice 2

for ligne in range(len(ma_grille)):# pour chaque ligne et colonne on vérifie que les sommes sont égales i.e. mêmes nombre de zéros et de uns
    csp.add(And(Sum(ma_grille[:][ligne])==Ma_somme,Sum(np.transpose(ma_grille).tolist()[ligne])==Ma_somme))
    if ligne < len(ma_grille)-1:## on ajoute la condition de différences séquences sur les lignes et colonnes de manière chaînée
        csp.add(ma_grille[ligne]!=ma_grille[ligne+1])
        csp.add(np.transpose(ma_grille).tolist()[ligne]!=np.transpose(ma_grille).tolist()[ligne+1])
    for colonne in range(len(ma_grille)-3):# on ajoute ici la condition de ne pas avoir  plus que deux uns ou deux zéros qui se suivent
            if len(ma_grille[ligne][colonne:colonne+3])==3:## on vérifie qu'on récupère bien trois termes consécutifs sur une ligne
                csp.add(And(Sum(ma_grille[ligne][colonne:colonne+3])<=2, Sum(ma_grille[ligne][colonne:colonne+3])>0))# la somme doit être supérieure ou égale à 2 et strictement supérieure à 0
            if len(np.transpose(ma_grille)[ligne][colonne:colonne+3])==3: ## de la même manière sur les colonnes      
                csp.add(And(Sum(np.transpose(ma_grille).tolist()[ligne][colonne:colonne+3])<=2, Sum(np.transpose(ma_grille).tolist()[ligne][colonne:colonne+3])>0))          
      
if csp.check()==sat:## si c'est solvable
    print("This problem has a solution")
    print(csp)# on affiche les conditions du modèle
    deltaT=round(time.time()-t1,3)# on stop le chronomètre
    Grille_resolue=[]# on récupère la grille résolue
    for ligne in range(0,N):# on balaye les lignes
        liste_ligne=[]
        for colonne in range(0,N):# on balaye les colonnes
            if ma_grille[ligne][colonne]==1 or ma_grille[ligne][colonne]==0 :# on distinque s'il s'agit de valeurs imposées ou bien de valeurs issues du solver
                liste_ligne.append(ma_grille[ligne][colonne])
            else :
                liste_ligne.append(int(csp.model()[Int("T{},{}".format(ligne,colonne))].as_long()))# on récupère les valeurs issues du solveur
        Grille_resolue.append(liste_ligne)

    sns.heatmap(Grille_resolue,annot=True)# affichage de la grille de binero résolue
    plt.title("Grille Binero pour n*n={}*{} solved in t={} s".format(N,N,deltaT))# titre
    plt.show()
else :
    print("No solution")