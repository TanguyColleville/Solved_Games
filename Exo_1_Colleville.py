### Auteur : Tanguy Colleville
## Exercie 1
from z3 import *
csp = Solver()

N=[Int('N_%i'%(i)) for i in range(1,6)]# Contraintes de nationalité indicées
Nprim=["Anglais","Espagnol","Japonais","Italien","Norvégien"]

C=[Int('C_%i'%(i)) for i in range(1,6)]# Contraintes de couleur indicées
Cprim=["Rouge","Vert","Blanc","Jaune","Bleu"]

B=[Int('B_%i'%(i)) for i in range(1,6)]# Contraintes de boisson indicées
Bprim=["Thé","Café","Lait","Jus de fruit","Eau"]

P=[Int('P_%i'%(i)) for i in range(1,6)]# Contraintes de profession indicées
Pprim=["Peintre","Sculpteur","Diplomate","Violoniste","Médecin"]

A=[Int('A_%i'%(i)) for i in range(1,6)]# Contraintes d'animal indicées
Aprim=["Chien","Escargot","Renard","Cheval","Zèbre"]

for list in [N,C,B,P,A]:# Parmi toutes ces variables on indique qu'au sein d'une même caractéristique (nationalité, boisson etc.) elles doivent toutes avoir une valeur distincte
    csp.add(Distinct(list))
    for element in list:
        csp.add(And(element>=1, element<=5))# les éléments doivent s'assignés mutuellement d'où leurs appartenances à {1,2,3,4,5}


csp.add(N[0]==C[0])# Anglais vit dans la maison rouge 
csp.add(N[1]==A[0])# L’espagnol possède un chien
csp.add(N[2]==P[0])# Le Japonais est peintre
csp.add(N[3]==B[0])# L’Italien boit du thé
csp.add(N[4]==1)# Le Norvégien vit dans la première maison à gauche
csp.add(C[1]==B[1])# Le propriétaire de la maison verte boit du café
csp.add(C[1]==C[2]+1)# La maison verte est juste à droite de la maison blanche
csp.add(P[1]==A[1])# Le sculpteur élève des escargots
csp.add(P[2]==C[3])# Le diplomate vit dans la maison jaune
csp.add(B[2]==3)# Le propriétaire de la maison du milieu boit du lait
csp.add(Or(N[4]==C[4]+1, N[4]==C[4]-1))# Le Norvégien est voisin de la maison bleue
csp.add(P[3]==B[3])# Le violoniste boit des jus de fruits
csp.add(Or(A[2]==P[4]-1, A[2]==P[4]+1))# Le renard est dans la maison voisine de celle du médecin
csp.add(Or(A[3]==P[2]-1, A[3]==P[2]+1))# Le cheval est dans la maison voisine de celle du diplomate.

if csp.check()==sat:
    print(csp.model())# on affiche les résultats du modèle. Le nombre auquel est associé chaque variable correspond à la maison 
else:
    print('no_solution')