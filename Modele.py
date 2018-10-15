# -*- coding: utf-8 -*-

from tkinter import *
import os,os.path
import sys
import xmlrpc.client
import socket
import random
from subprocess import Popen 
from helper import Helper as hlp
from ObjetsJeu import *
from MonstreIntersideral import *
from PIL import Image, ImageTk

class Modele():
    def __init__(self,parent,joueurs):
        self.parent=parent
        self.largeur=1920 #self.parent.vue.root.winfo_screenwidth()
        self.hauteur=700 #self.parent.vue.root.winfo_screenheight()
        self.joueurs={}
        self.actionsafaire={}
        self.planetes=[]
        self.listeVaisseaux = []
        self.listeEtoiles = []
        self.listeAsteroides = []
        self.terrain=[]
        self.creerplanetes(joueurs)
        self.creerterrain()
        self.monstre = MonstreIntersideral (self, 95, 60)
            # peut changer pour un init pour choisir une position random parmis choix
#         self.progenitures = ProgenitureInfernale (self, 120, 140)
        self.genererAstres()
        
    def creerterrain(self):
        self.terrain=[]
        for i in range(10):
            ligne=[]
            for j in range(10):
                n=random.randrange(5)
                if n==0:
                    ligne.append(1)
                else:
                    ligne.append(0)
            self.terrain.append(ligne)
        
    def creerplanetes(self,joueurs):
        bordure=10
        for i in range(100):
            x=random.randrange(self.largeur-(2*bordure))+bordure
            y=random.randrange(self.hauteur-(2*bordure))+bordure
            self.planetes.append(Planete(x,y)) # ajouter false quand class sera mise � jour
        np=len(joueurs)
        planes=[]
        while np:
            p=random.choice(self.planetes)
            if p not in planes:
                planes.append(p)
                self.planetes.remove(p)
                np-=1
        couleurs=["red","blue","lightgreen","yellow",
                  "lightblue","pink","gold","purple"]
        for i in joueurs:
            self.joueurs[i]=Joueur(self,i,planes.pop(0),couleurs.pop(0))
            
    def genererAstres(self):
        for i in range(10):
            self.listeEtoiles.append(Etoile(random.randint(0,1000), random.randint(0,1000))) 
            self.listeAsteroides.append(Asteroide(random.randint(0,1000), random.randint(0,1000)))   
            
    def prochaineaction(self,cadre):
        if cadre in self.actionsafaire:
            for i in self.actionsafaire[cadre]:
                #print(i)
                self.joueurs[i[0]].actions[i[1]](i[2])
                """
                print("4- le modele distribue les actions au divers participants")
                print("4...- en executant l'action qui est identifie par i[1] le dico")
                print("4...- qui est dans l'attribut actions",i[0],i[1],i[2])
                print("NOTE: ici on applique immediatement cette action car elle consiste soit")
                print("NOTE... a changer la vitesse (accelere/arrete) soit l'angle de l'auto")
                print("NOTE... dans ce cas-ci faire la prochaine action (le prochain for en bas)")
                print("NOTE... c'est seulement changer la position de l'auto si sa vitesse est non-nul")
                """
            del self.actionsafaire[cadre]
                
        for i in self.joueurs:
            self.joueurs[i].prochaineaction()
            # DEBUT AJOUTS JCB !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.joueurs[i].productionFerme()
            self.joueurs[i].productionMineArgent()
            self.joueurs[i].productionMineMateriaux()
            self.joueurs[i].productionMineEnergie()
            self.joueurs[i].productionReacteurNucleaire()
            self.joueurs[i].coutEnergitique()
            # FIN AJOUTS JCB !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! 

class Etoile():
    def __init__(self,x,y):
        self.x = x
        self.y = y
        
class Asteroide():
    def __init__(self,x,y):
        self.x = x
        self.y = y
        
if __name__ == "__main__":
    joueur = {"joueur1": "joueur1"}
    modele = Modele(0,joueur)
    while 1:
        modele.monstre.choixAction()
        time.sleep(2)
    