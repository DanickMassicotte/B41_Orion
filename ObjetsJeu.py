# -*- coding: utf-8 -*-

from tkinter import *
import os,os.path
import sys
import xmlrpc.client
import socket
import random
from subprocess import Popen 
from helper import Helper as hlp

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
        
        # Debut des modifications; change "flotte" de liste a dictionnaire de listes
        self.flotte={"M": [],       # Mineurs
                     "E": [],       # Exploreurs
                     "A1": [],      # Fregates
                     "A2": [],      # Chasseurs
                     "A3": [],      # Bombardes
                     "A4": [],      # Dreadnoughts
                     "A5": []}      # Destructeurs
        self.actions = { "creervaisseau" : self.creervaisseau, 
                        "ciblerflotte" : self.ciblerflotte }
        
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
        
        
    def prochaineaction(self):
        for i in self.flotte[choix]:
            if i.cible:
                i.avancer()
            else:
                i.cible=random.choice(self.parent.planetes)
            
    def prochaineaction2(self):
        for i in self.flotte:
            i.avancer()