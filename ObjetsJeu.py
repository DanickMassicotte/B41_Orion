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
        self.combat = False
        self.cargo=0            # Necessaire?
        self.energie=100        # Necessaire?
        self.hp = 100
        self.atk = 10
        self.vitesse=2
        self.cout = 100
        self.pop = 1
        self.cible=None
        
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
              
class Joueur():
    def __init__(self,parent,nom,planetemere,couleur):
        self.id=Id.prochainid()
        self.parent=parent
        self.nom=nom
        self.planetemere=planetemere
        self.planetemere.proprietaire=self.nom
        self.couleur=couleur
        self.planetescontrolees=[planetemere]
        self.flotte=[]
        self.actions={"creervaisseau":self.creervaisseau,
                      "ciblerflotte":self.ciblerflotte}
        
    def creervaisseau(self,planete):
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