# -*- coding: utf-8 -*-

from tkinter import *
import os,os.path
import sys
import xmlrpc.client
import socket
import random
from random import randint
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
        self.estInfectee = False #ajout Simon
        self.taille=random.randrange(4,6)
    # Debut ajouts JCB !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # Creation de listes de batiments
        self.fermes=[]
        self.pods=[]
        self.minesArgent=[]
        self.minesMateriaux=[]
        self.minesEnergie=[]
        self.hangars=[]
        self.reacteursNucleaires=[]
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
        self.matiereNucleaire = 0
        self.population = 0
        self.populationMaximale = 0
        self.connaissance = 1000
        self.fermes=[]
        self.pods=[] # Logements
        self.minesArgent=[]
        self.minesMateriaux=[]
        self.minesEnergie=[]
        self.hangars=[]
        self.reacteursNucleaires=[]
    # FIN AJOUTS JCB !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        
        # Debut des modifications; change "flotte" de liste a dictionnaire de listes
        self.flotte={"M": [],       # Mineurs
                     "E": [],       # Exploreurs
                     "A1": [],      # Fregates
                     "A2": [],      # Chasseurs
                     "A3": [],      # Bombardes
                     "A4": [],      # Dreadnoughts
                     "A5": []}      # Destructeurs
        self.actions = { "creervaisseau" : self.creervaisseau, 
                        "ciblerflotte" : self.ciblerflotte,
                        "creerPod" : self.creerPod,
                        "creerFerme" : self.creerFerme,
                        "creerMineArgent" : self.creerMineArgent,
                        "creerMineMateriaux" : self.creerMineMateriaux,
                        "creerMineEnergie" : self.creerMineEnergie,
                        "creerHangar" : self.creerHangar,
                        "creerReacteurNucleaire" : self.creerReacteurNucleaire}
        
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
        
        rx = randint(-25, 25)
        ry = randint(-25, 25)
        
        v = self.choix[choix](self.nom, self.planetemere.x + rx, self.planetemere.y + ry)
        print("Vaisseau", v.id)
        print("Type: ", v.type)
        print("Combat: ", v.combat)
        print("HP: ", v.hp)
        print("Atk: ", v.atk)
        print("Vts: ", v.vitesse)
        print("Cout: ", v.cout)
        print("Pop: ", v.pop)
        self.flotte[choix].append(v)
        
    def ciblerflotte(self,ids, choix):
        idori,iddesti=ids
        for i in self.flotte[choix]:
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
                pass
            
    def prochaineaction2(self):
        for i in self.flotte:
            i.avancer()

# DEBUT AJOUTS CREATION BATIMENTS JCB !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! 

    # Création d'une ferme qui accumule de la nourriture   
    def creerFerme(self,vide):
        if self.argent >= Batiments.Ferme.coutEnArgent and self.materiaux >= Batiments.Ferme.coutEnMateriaux:
            print("Creation d'une ferme")
            self.argent -= Batiments.Ferme.coutEnArgent                     # Total argent - cout
            self.materiaux -= Batiments.Ferme.coutEnMateriaux               # Total materiaux - cout
            f=Batiments.Ferme()
            self.fermes.append(f)
            self.planetemere.fermes.append(f)
            print("Total Argent Joueur:", self.argent)
            print("Total Materiaux Joueur:", self.materiaux)
            print("Nombre de Ferme: ",len(self.fermes))
        else:
            print("Manque de ressource!")
            #print("Cout d'une ferme en argent:", Batiments.Ferme.coutEnArgent)
            #print("Cout d'une ferme en matériaux:", Batiments.Ferme.coutEnMateriaux)
            #print("Total Argent Joueur:", self.argent)
            #print("Total Materiaux Joueur:", self.materiaux)
            
    # Création d'un logement    
    def creerPod(self,vide):
        if self.argent >= Batiments.Pod.coutEnArgent and self.materiaux >= Batiments.Pod.coutEnMateriaux:
            print("Creation d'un Pod")
            self.argent -= Batiments.Pod.coutEnArgent                       # Total argent - cout
            self.materiaux -= Batiments.Pod.coutEnMateriaux                 # Total materiaux - cout
            p=Batiments.Pod()
            self.pods.append(p)
            self.planetemere.pods.append(p)
            self.populationMaximale += Batiments.Pod.capaciteOccupants      # Population maximale ++
            self.population += Batiments.Pod.nbOccupants                    # Population ++
            print("Total Argent Joueur:", self.argent)
            print("Total Materiaux Joueur:", self.materiaux)
            print("Nombre de Pods: ",len(self.pods))
            print("Population: ", self.population)
            print("Population Maximale: ", self.populationMaximale)
        else:
            print("Manque de ressource!")
            #print("Total Argent Joueur:", self.argent)
            #print("Total Materiaux Joueur:", self.materiaux)
            
            
    # Permet de créer des vaisseaux        
    def creerHangar(self,vide):
        if len(self.hangars) == 0:
            if self.argent >= Batiments.Hangar.coutEnArgent and self.materiaux >= Batiments.Hangar.coutEnMateriaux:
                print("Creation d'un Hangar")
                self.argent -= Batiments.Hangar.coutEnArgent                       # Total argent - cout
                self.materiaux -= Batiments.Hangar.coutEnMateriaux                 # Total materiaux - cout
                p=Batiments.Hangar()
                self.hangars.append(p)
                self.planetemere.hangars.append(p)
                print("Nombre de hangars: ",len(self.hangars))
                print("Total Argent Joueur:", self.argent)
                print("Total Materiaux Joueur:", self.materiaux)
            else:
                print("Manque de ressource!")
                #print("Total Argent Joueur:", self.argent)
                #print("Total Materiaux Joueur:", self.materiaux)
        else:
            print("Vous avez déjà un hangar!")
            
            
    # Création d'une mine qui accumule de l'argent         
    def creerMineArgent(self,vide):
        if self.materiaux >= Batiments.MineArgent.coutEnMateriaux:
            print("Creation d'une mine d'argent")
            self.materiaux -= Batiments.MineArgent.coutEnMateriaux          # Total materiaux - cout
            ma=Batiments.MineArgent()
            self.minesArgent.append(ma)
            self.planetemere.minesArgent.append(ma)
            print("Total Argent Joueur:", self.argent)
            print("Total Materiaux Joueur:", self.materiaux)
        else:
            print("Manque de ressource!")
            #print("Total Argent Joueur:", self.argent)
            #print("Total Materiaux Joueur:", self.materiaux)
            
            
    # Création d'une mine qui accumule des materiaux de construction      
    def creerMineMateriaux(self,vide):
        if self.argent >= Batiments.MineMateriaux.coutEnArgent:
            print("Creation d'une mine de materiel")
            self.argent -= Batiments.MineMateriaux.coutEnArgent              # Total argent - cout
            mm=Batiments.MineMateriaux()
            self.minesMateriaux.append(mm)
            self.planetemere.minesMateriaux.append(mm)
            print("Total Argent Joueur:", self.argent)
            print("Total Materiaux Joueur:", self.materiaux)
        else:
            print("Manque de ressource!")
            #print("Total Argent Joueur:", self.argent)
            #print("Total Materiaux Joueur:", self.materiaux)
            
            
    # Création d'une mine qui accumule des materiaux sources d'energie   
    def creerMineEnergie(self,vide):
        if self.argent >= Batiments.MineEnergie.coutEnArgent and self.materiaux >= Batiments.MineEnergie.coutEnMateriaux:
            print("Creation d'une mine d'energie")
            self.argent -= Batiments.MineEnergie.coutEnArgent                       # Total argent - cout
            self.materiaux -= Batiments.MineEnergie.coutEnMateriaux                 # Total materiaux - cout
            me=Batiments.MineEnergie()
            self.minesEnergie.append(me)
            self.planetemere.minesEnergie.append(me)
            print("Total Argent Joueur:", self.argent)
            print("Total Materiaux Joueur:", self.materiaux)
        else:
            print("Manque de ressource!")
            #print("Total Argent Joueur:", self.argent)
            #print("Total Materiaux Joueur:", self.materiaux)
            
            
    # Création d'une mine qui accumule des materiaux sources d'energie   
    def creerReacteurNucleaire(self,vide):
        if self.argent >= Batiments.ReacteurNucleaire.coutEnArgent and self.materiaux >= Batiments.ReacteurNucleaire.coutEnMateriaux:
            print("Creation d'un reacteur nucleaire")
            self.argent -= Batiments.ReacteurNucleaire.coutEnArgent                       # Total argent - cout
            self.materiaux -= Batiments.ReacteurNucleaire.coutEnMateriaux                 # Total materiaux - cout
            rn=Batiments.ReacteurNucleaire()
            self.reacteursNucleaires.append(rn)
            self.planetemere.reacteursNucleaires.append(rn)
            print("Total Argent Joueur:", self.argent)
            print("Total Materiaux Joueur:", self.materiaux)
        else:
            print("Manque de ressource!")
            #print("Total Argent Joueur:", self.argent)
            #print("Total Materiaux Joueur:", self.materiaux)
            
    def productionFerme(self):
        if len(self.fermes) > 0:
            for i in self.fermes:
                self.nourriture+=i.produire()
                #print("Total nourriture joueur: ",self.nourriture)
                
    def productionMineArgent(self):
        if len(self.minesArgent) > 0:
            for i in self.minesArgent:
                self.argent+=i.miner()
                #print("Total argent joueur: ",self.argent)
                
    def productionMineMateriaux(self):
        if len(self.minesMateriaux) > 0:
            for i in self.minesMateriaux:
                self.materiaux+=i.miner()
                #print("Total materiaux joueur: ",self.materiaux)
                
    def productionMineEnergie(self):
        if len(self.minesEnergie) > 0:
            for i in self.minesEnergie:
                self.matiereNucleaire+=i.miner()
                #print("Total matiere nucleaire joueur: ",self.matiereNucleaire)
                #print("Total energie joueur: ",self.energie)
                
    def productionReacteurNucleaire(self):
        if len(self.reacteursNucleaires) > 0:
            if self.matiereNucleaire > 0:
                for i in self.reacteursNucleaires:
                    self.energie += i.produire()
                    self.matiereNucleaire -= i.produire()/2
                    #print("Total matiere nucleaire joueur: ",self.matiereNucleaire)
                    #print("Total energie joueur: ",self.energie)
            else:
                print("Manque de ressource nucléaire ! Production arrêté!!!")
                
    def coutEnergitique(self):
        totalCoutEnergitique = 0
        for i in self.pods:
            totalCoutEnergitique += i.consommationEnergie
        for i in self.fermes:
            totalCoutEnergitique += i.consommationEnergie
        for i in self.minesArgent:
            totalCoutEnergitique += i.consommationEnergie
        for i in self.minesMateriaux:
            totalCoutEnergitique += i.consommationEnergie
        for i in self.minesEnergie:
            totalCoutEnergitique += i.consommationEnergie
        for i in self.hangars:
            totalCoutEnergitique += i.consommationEnergie
        for i in self.reacteursNucleaires:
            totalCoutEnergitique += i.consommationEnergie
        
        self.energie -= totalCoutEnergitique / 60
        #print("Total cout energitique", totalCoutEnergitique)
        #print("Total Energie", self.energie)
        
    # FIN AJOUTS CREATION BATIMENTS JCB !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!        
