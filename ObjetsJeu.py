# -*- coding: utf-8 -*-

from tkinter import *
import os,os.path
import sys
import xmlrpc.client
import socket
import random
from subprocess import Popen 
from helper import Helper as hlp
import Batiments # Ajout JCB !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

choix = "A1"

class Id():
    id=0
    def prochainid():
        Id.id+=1
        return Id.id
        
class Planete():
    def __init__(self,x,y):
        self.id=Id.prochainid()
        self.proprietaire="inconnu"
        self.x=x
        self.y=y
        self.estOccupee = False # ajout Simon
        self.taille=random.randrange(4,6)
    # Debut ajouts JCB !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # Creation de listes de batiments
        self.fermes=[]
        self.pods=[]
        self.minesArgent=[]
        self.minesMateriaux=[]
        self.minesEnergie=[]
        self.hangars=[]
    # Fin ajouts JCB !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        
class Vaisseau():
    def __init__(self,nom,x,y):
        self.id=Id.prochainid()
        self.proprietaire=nom
        self.x=x
        self.y=y
        self.cargo=0
        self.energie=100
        self.vitesse=2
        self.cible=None 
        
        # Debut des modifications
        self.hp = 100
        self.atk = 10
        self.cout = 100
        self.pop = 1
        self.combat = False
        # Fin des modifications -- DM
        
    def avancer(self):
        if self.cible:
            x=self.cible.x
            y=self.cible.y
            ang=hlp.calcAngle(self.x,self.y,x,y)
            x1,y1=hlp.getAngledPoint(ang,self.vitesse,self.x,self.y)
            self.x,self.y=x1,y1 #int(x1),int(y1)
            if hlp.calcDistance(self.x,self.y,x,y) <=self.vitesse:
                self.cible=None
                #print("Change cible")
        else:
            print("PAS DE CIBLE")
    
    def avancer1(self):
        if self.cible:
            x=self.cible.x
            if self.x>x:
                self.x-=self.vitesse
            elif self.x<x:
                self.x+=self.vitesse
            
            y=self.cible.y
            if self.y>y:
                self.y-=self.vitesse
            elif self.y<y:
                self.y+=self.vitesse
            if abs(self.x-x)<(2*self.cible.taille) and abs(self.y-y)<(2*self.cible.taille):
                self.cible=None
                
# Debut des modifications/differents types de vaisseaux
        
class Mineur(Vaisseau):
    def __init__(self, nom, x, y):
        Vaisseau.__init__(self, nom, x, y)
        self.type = "Mineur"                # Sert à certain tests
        self.hp = self.hp * 1
        self.atk = self.atk * 0
        self.vitesse = self.vitesse * 1
        self.cout = self.cout * 1.5
        self.pop = self.pop * 3
        
    def minevalide(self):
        pass
    
    def miner(self):
        pass
    
class Exploreur(Vaisseau):
    def __init__(self, nom, x, y):
        Vaisseau.__init__(self, nom, x, y)
        self.type = "Exploreur"             # Sert à certains tests
        self.hp = self.hp * 1
        self.atk = self.atk * 0
        self.vitesse = self.vitesse * 1
        self.cout = self.cout * 1.5
        self.pop = self.pop * 1
        
    def explovalide(self):
        pass
    
    def decouvrir(self):
        pass
    
class Fregate(Vaisseau):
    def __init__(self, nom, x, y):
        Vaisseau.__init__(self, nom, x, y)
        self.combat = True
        self.type = "Fregate"               # Sert à certains tests
        self.hp = self.hp * 1
        self.atk = self.atk * 1
        self.vitesse = self.vitesse * 1
        self.cout = self.cout * 0.5
        self.pop = self.pop * 1
        
    def attaquevalide(self):
        pass
        
    def attaquer(self):
        pass
                
class Chasseur(Vaisseau):
    def __init__(self, nom, x, y):
        Vaisseau.__init__(self, nom, x, y)
        self.type = "Chasseur"              # Sert à certains tests
        self.combat = True
        self.hp = self.hp * 2
        self.atk = self.atk * 3
        self.vitesse = self.vitesse * 5
        self.cout = self.cout * 2
        self.pop = self.pop * 1

    def attaquevalide(self):
            pass
        
    def attaquer(self):
            pass
        
class Bombarde(Vaisseau):
    def __init__(self, nom, x, y):
        Vaisseau.__init__(self, nom, x, y)
        self.combat = True
        self.type = "Bombarde"              # Sert à certains tests
        self.hp = self.hp * 2
        self.atk = self.atk * 2
        self.vitesse = self.vitesse * 2
        self.cout = self.cout * 2.5
        self.pop = self.pop * 3
        
    def attaquevalide(self):
                pass
        
    def attaquerBombe(self):
        pass
    
class Dreadnought(Vaisseau):
    def __init__(self, nom, x, y):
        Vaisseau.__init__(self, nom, x, y)
        self.combat = True
        self.type = "Dreadnought"
        self.hp = self.hp * 5
        self.atk = self.atk * 5
        self.vitesse = self.vitesse * 0.5
        self.cout = self.cout * 5
        self.pop = self.pop * 10
        
    def attaquevalide(self):
        pass
        
    def attaquer(self):
        pass
    
class Destructeur(Vaisseau):
    def __init__(self, nom, x, y):
        Vaisseau.__init__(self, nom, x, y)
        self.combat = True
        self.type = "Destructeur"
        self.hp = self.hp * 5
        self.atk = self.atk * 10
        self.vitesse = self.vitesse * 0
        self.cout = self.cout * 10
        self.pop = self.pop * 25
        
    def attaquevalide(self):
        pass
        
    def attaquerPlanete(self):
        pass   
    
# Fin des modifications/types de vaisseaux -- DM
              
class Joueur():
    def __init__(self,parent,nom,planetemere,couleur):
        self.id=Id.prochainid()
        self.parent=parent
        self.nom=nom
        self.planetemere=planetemere
        self.planetemere.proprietaire=self.nom
        self.couleur=couleur
        self.planetescontrolees=[planetemere]
    # DEBUT AJOUTS JCB !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        self.argent = 1000
        self.nourriture = 1000
        self.materiaux = 1000
        self.energie = 1000
        self.population = 100
        self.populationMaximale = 1000
        self.connaissance = 1000
        self.fermes=[]
        self.pods=[] # Logements
        self.minesArgent=[]
        self.minesMateriaux=[]
        self.minesEnergie=[]
        self.hangars=[]
    # FIN AJOUTS JCB !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        
        # Debut des modifications; change "flotte" de liste a dictionnaire de listes
        self.flotte={"M": [],       # Mineurs
                     "E": [],       # Exploreurs
                     "A1": [],      # Fregates
                     "A2": [],      # Chasseurs
                     "A3": [],      # Bombardes
                     "A4": [],      # Dreadnoughts
                     "A5": []}      # Destructeurs
        # Fin des modifications -- DM
        
    def creervaisseau(self,planete,choix):
        self.choix = {"M": Mineur,          # Mineurs
                      "E": Exploreur,       # Exploreur
                      "A1": Fregate,        # Fregates
                      "A2": Chasseur,       # Chasseurs
                      "A3": Bombarde,       # Bombardes
                      "A4": Dreadnought,    # Dreadnought
                      "A5": Destructeur     # Destructeurs
                      }
        
        v = self.choix[choix](self.nom, self.planetemere.x+10, self.planetemere.y)
        print("Vaisseau", v.id)
        print("Type: ", v.type)
        print("Combat: ", v.combat)
        print("HP: ", v.hp)
        print("Atk: ", v.atk)
        print("Vts: ", v.vitesse)
        print("Cout: ", v.cout)
        print("Pop: ", v.pop)
        self.flotte[choix].append(v)
        
    def ciblerflotte(self,ids):
        idori,iddesti=ids
        for i in self.flotte:
            if i.id== int(idori):
                for j in self.parent.planetes:
                    if j.id== int(iddesti):
                        i.cible=j
                        print("GOT TARGET")
                        return
        

# DEBUT AJOUTS CREATION BATIMENTS JCB !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! 

    # Création d'une ferme qui accumule de la nourriture   
    def creerFerme(self):
        if self.argent >= Batiments.Ferme.coutEnArgent and self.minerai >= Batiments.Ferme.coutEnMateriaux:
            self.argent -= Batiments.Ferme.coutEnArgent                     # Total argent - cout
            self.materiaux -= Batiments.Ferme.coutEnMateriaux               # Total materiaux - cout
            f=Batiments.Ferme()
            self.fermes.append(f)
            self.planetemere.fermes.append(f)
        else:
            print("Manque de ressource!")
            
    # Création d'un logement    
    def creerpod(self):
        if self.argent >= Batiments.Pod.coutEnArgent and self.minerai >= Batiments.Pod.coutEnMateriaux:
            self.argent -= Batiments.Pod.coutEnArgent                       # Total argent - cout
            self.materiaux -= Batiments.Pod.coutEnMateriaux                 # Total materiaux - cout
            p=Batiments.Pod()
            self.pods.append(p)
            self.planetemere.pods.append(p)
            self.populationMaximale += Batiments.Pod.capaciteOccupants      # Population maximale ++
            self.population += Batiments.Pod.nbOccupants                    # Population ++
        else:
            print("Manque de ressource!")
            
    def creerhangar(self):
        if self.argent >= Batiments.Hangar.coutEnArgent and self.minerai >= Batiments.Hangar.coutEnMateriaux:
            self.argent -= Batiments.Hangar.coutEnArgent                       # Total argent - cout
            self.materiaux -= Batiments.Hangar.coutEnMateriaux                 # Total materiaux - cout
            p=Batiments.Hangar()
            self.hangars.append(p)
            self.planetemere.hangars.append(p)
        else:
            print("Manque de ressource!")
            
    # Création d'une mine qui accumule de l'argent         
    def creerMineArgent(self):
        if self.minerai >= Batiments.MineArgent.coutEnMateriaux:
            self.materiaux -= Batiments.MineArgent.coutEnMateriaux          # Total materiaux - cout
            ma=Batiments.MineArgent()
            self.minesArgent.append(ma)
            self.planetemere.minesArgent.append(ma)
        else:
            print("Manque de ressource!")
            
    # Création d'une mine qui accumule des materiaux de construction      
    def creerMineMateriaux(self):
        if self.argent >= Batiments.MineMateriaux.coutEnArgent:
            self.argent -= Batiments.MineMateriaux.coutEnArgent              # Total argent - cout
            mm=Batiments.MineMateriaux()
            self.minesMateriaux.append(mm)
            self.planetemere.minesMateriaux.append(mm)
        else:
            print("Manque de ressource!")
            
    # Création d'une mine qui accumule des materiaux sources d'energie   
    def creerMineEnergie(self):
        if self.argent >= Batiments.MineEnergie.coutEnArgent and self.minerai >= Batiments.MineEnergie.coutEnMateriaux:
            self.argent -= Batiments.MineEnergie.coutEnArgent                       # Total argent - cout
            self.materiaux -= Batiments.MineEnergie.coutEnMateriaux                 # Total materiaux - cout
            me=Batiments.MineEnergie()
            self.minesEnergie.append(me)
            self.planetemere.minesEnergie.append(me)
        else:
            print("Manque de ressource!")
    # FIN AJOUTS CREATION BATIMENTS JCB !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    
    def prochaineaction(self):
        for i in self.flotte:
            if i.cible:
                i.avancer()
            else:
                i.cible=random.choice(self.parent.planetes)
            
    def prochaineaction2(self):
        for i in self.flotte:
            i.avancer()