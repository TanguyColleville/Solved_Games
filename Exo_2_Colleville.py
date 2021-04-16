## Auteur: Tanguy Colleville
import time as time 

import matplotlib.pyplot as plt 
import numpy as np
import seaborn as sns
from tkinter import * 
from z3 import * 


csp=Solver()## Création d'un Solver z3

main = Tk()###création d'une fenêtre vide qui s'appelle main 
main.title("Carré Magique")### titre de la fenêtre
N=StringVar()## variable d'entrée du nombre de côté du carré magique

Label(main, text= "Longeur du côté").grid(row = 1, column = 0)
Entry(main,textvariable=N).grid(row=1,column=1)## zone d'entrée du texte
Button(main,text="Valider",command=main.destroy).grid(row=2, column= 0)## bouton de validation qui ferme la fenêtre
main.mainloop()# on maintient la fenêtre

N=int(N.get())# on récupère la valeur donnée par l'utilisateur

t1=time.time()# on lance le chronomètre

Carre=[[Int("C_%i_%i"%(i+1,j+1))for j in range(N)]for i in range(N)]## on crée le carré avec une déclaration de variable pour chaque case
# Carre=[[BitVec("C_%i_%i"%(i+1,j+1),32)for j in range(N)]for i in range(N)]## BitVec est un moyen d'obtenir une solution plus rapide

diag1,diag2=np.diag(Carre).tolist(),np.diag(np.fliplr(Carre)).tolist()# on récupère les deux diagonales principales en les restransformants en liste

Ma_somme=Sum(diag1) ##on garde une somme de référence en mémoire

csp.add(Sum(diag1)==Ma_somme)## contrainte sur la seconde diagonale
csp.add(Sum(diag2)==Ma_somme)## contrainte sur la seconde diagonale

for i in range(N):# chaque ligne et chaque colonne doivent être égale à la somme de référence 
    csp.add(And(Sum(Carre[:][i])==Ma_somme,Sum(np.transpose(Carre).tolist()[i])==Ma_somme)) # on impose la condition à la ligne et à la colonne de rang i 

csp.add(Distinct(np.asarray(Carre).flatten().tolist()))# toutes les cases doivent avoir une valeur différente 

for element in np.asarray(Carre).flatten().tolist() :
    csp.add(And(element>=1,element<=N*N))## les cases doivent être à valeurs dans [|1,n²|]


if csp.check()==sat:## si c'est solvable
    print("This problem has a solution")
    deltaT=round(time.time()-t1,3)# on stop le chronomètre
    Carre_magique=[]
    for ligne in range(1,N+1):# on récupère pour chaque ligne
        liste_ligne=[]
        for colonne in range(1,N+1): # chaque colonne, la variable
            liste_ligne.append(csp.model()[Int("C_{}_{}".format(ligne,colonne))].as_long())# on récupère les valeurs du solveur
        Carre_magique.append(liste_ligne)# on ajoute la ligne au carré magique 
    sns.heatmap(Carre_magique,annot=True)# représentation graphique du carré
    plt.title("Carré magique pour n={} en t={} s".format(N,deltaT))
    plt.show()
else :
    print("No solution")



