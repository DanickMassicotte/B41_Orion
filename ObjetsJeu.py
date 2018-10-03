# -*- coding: utf-8 -*-

from tkinter import *
import os,os.path
import sys
import xmlrpc.client
import socket
import random
from subprocess import Popen 
from helper import Helper as hlp

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
        self.taille=random.randrange(4,6)
        
class Vaisseau():
    def __init__(self,nom,x,y):
        self.id=Id.prochainid()
        self.proprietaire=nom
        self.x=x
        self.y=y
        self.cargo=0            # Necessaire?
        self.energie=100        # Necessaire?
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
    def __init__(self):
        Vaisseau.__init__(self, nom, x, y, combat)
        self.hp = Vaisseau.hp * 1
        self.atk = Vaisseau.atk * 0
        self.vts = Vaisseau.vitesse * 1
        self.cout = Vaisseau.cout * 1.5
        self.pop = Vaisseau.pop * 3
        
    def minevalide(self):
        pass
    
    def miner(self):
        pass
    
class Exploreur(Vaisseau):
    def __init__(self):
        Vaisseau.__init__(self, nom, x, y, combat)
        self.hp = Vaisseau.hp * 1
        self.atk = Vaisseau.atk * 0
        self.vts = Vaisseau.vitesse * 1
        self.cout = Vaisseau.cout * 1.5
        self.pop = Vaisseau.pop * 2
        
    def explovalide(self):
        pass
    
    def decouvrir(self):
        pass

class Fregate(Vaisseau):
    def __init__(self):
        Vaisseau.__init__(self, nom, x, y, combat)
        self.combat = True
        self.hp = Vaisseau.hp * 1
        self.atk = Vaisseau.atk * 1
        self.vts = Vaisseau.vitesse * 1
        self.cout = Vaisseau.cout * 1
        self.pop = Vaisseau.pop * 1
        
    def attaquevalide(self):
        pass
        
    def attaquer(self):
        pass

class Chasseur(Vaisseau):
    def __init__(self):
        Vaisseau.__init__(self, nom, x, y, combat)
        self.combat = True
        self.hp = Vaisseau.hp * 2
        self.atk = Vaisseau.atk * 3
        self.vts = Vaisseau.vitesse * 5
        self.cout = Vaisseau.cout * 2
        self.pop = Vaisseau.pop * 1

    def attaquevalide(self):
            pass
        
    def attaquer(self):
            pass
        
class Bombarde(Vaisseau):
    def __init__(self):
        Vaisseau.__init__(self, nom, x, y, combat)
        self.combat = True
        self.hp = Vaisseau.hp * 2
        self.atk = VaisseauCombat.atk * 2
        self.vts = Vaisseau.vitesse * 2
        self.cout = Vaisseau.cout * 2.5
        self.pop = Vaisseau.pop * 3
        
    def attaquevalide(self):
                pass
        
    def attaquerBombe(self):
        pass
        
class Dreadnought(Vaisseau):
    def __init__(self):
        Vaisseau.__init__(self, nom, x, y, combat)
        self.combat = True
        self.hp = Vaisseau.hp * 5
        self.atk = Vaisseau.atk * 5
        self.vts = Vaisseau.vitesse * 1
        self.cout = Vaisseau.cout * 5
        self.pop = Vaisseau.pop * 10
        
    def attaquevalide(self):
        pass
        
    def attaquer(self):
        pass
        
class Destructeur(Vaisseau):
    def __init__(self):
        Vaisseau.__init__(self, nom, x, y, combat)
        self.combat = True
        self.hp = Vaisseau.hp * 5
        self.atk = Vaisseau.atk * 10
        self.vts = Vaisseau.vitesse * 0
        self.cout = Vaisseau.cout * 10
        self.pop = Vaisseau.pop * 25
        
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
        # Fin des modifications -- DM
        
        self.actions={"creervaisseau":self.creervaisseau,
                      "ciblerflotte":self.ciblerflotte}
    
    # Modification de la methode pour inclure les types de vaisseaux
    def creervaisseau(self,planete,choix):
        if choix == "M":
            v = Mineur(self.nom, self.planetemere.x+10, self.planetemere.y)
            print("Mineur", v.id)
            self.flotte["M"].append(v)
            
        elif choix == "E":
            v = Exploreur(self.nom, self.planetemere.x+10, self.planetemere.y)
            print("Exploreur", v.id)
            self.flotte["E"].append(v)
            
        elif choix == "A1":
            v = Fregate(self.nom, self.planetemere.x+10, self.planetemere.y)
            print("Fregate", v.id)
            self.flotte["A1"].append(v)
            
        elif choix == "A2":
            v = Chasseur(self.nom, self.planetemere.x+10, self.planetemere.y)
            print("Chasseur", v.id)
            self.flotte["A2"].append(v)
            
        elif choix == "A3":
            v = Bombarde(self.nom, self.planetemere.x+10, self.planetemere.y)
            print("Bombarde", v.id)
            self.flotte["A3"].append(v)
            
        elif choix == "A4":
            v = Dreadnought(self.nom, self.planetemere.x+10, self.planetemere.y)
            print("Dreadnought", v.id)
            self.flotte["A4"].append(v)
            
        elif choix == "A5":
            v = Destructeur(self.nom, self.planetemere.x+10, self.planetemere.y)
            print("Destructeur", v.id)
            self.flotte["A5"].append(v)
    # Fin des modifications -- DM
        
        v=Vaisseau(self.nom,self.planetemere.x+10,self.planetemere.y)
        print("Vaisseau",v.id)
        self.flotte.append(v)
        
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
        for i in self.flotte:
            if i.cible:
                i.avancer()
            else:
                i.cible=random.choice(self.parent.planetes)
            
    def prochaineaction2(self):
        for i in self.flotte:
            i.avancer()