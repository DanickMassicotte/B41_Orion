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
        self.estOccupee = False 
        self.estInfectee = False 
        self.estExploree = False 
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
        # ---------DM---------- #
        self.hp = 100
        self.atk = 10
        self.cout = 100
        self.pop = 1
        self.combat = False
        # --------------------- #
        
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
                
    def attaquevalide(self):
        pass
    
    def attaquer(self):
        pass
        
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
        if self.cible:
            if self.cible.mine:     # À réviser; n'entre pas dans le if...
                print("True")
                return True
            else:
                print("False")
                return False
    
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
        self.argent = 3000
        self.nourriture = 1000
        self.materiaux = 4000
        self.energie = 2000
        self.matiereNucleaire = 5000
        self.population = 10
        self.populationMaximale = 100
        self.connaissance = 6000
        self.fermes=[]
        self.pods=[] # Logements
        self.minesArgent=[]
        self.minesMateriaux=[]
        self.minesEnergie=[]
        self.hangars=[]
        self.reacteursNucleaires=[]
    # FIN AJOUTS JCB !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        
       # -----------DM------------- #
        self.flotte = []
        self.actions = {"creermineur" : self.creermineur,
                        "creerexploreur" : self.creerexploreur,
                        "creerfregate" : self.creerfregate,
                        "creerchasseur" : self.creerchasseur,
                        "creerbombarde" : self.creerbombarde,
                        "creerdreadnought" : self.creerdreadnought,
                        "creerdestructeur" : self.creerdestructeur, 
                        "ciblerflotte" : self.ciblerflotte,
                        "creerPod" : self.creerPod,
                        "creerFerme" : self.creerFerme,
                        "creerMineArgent" : self.creerMineArgent,
                        "creerMineMateriaux" : self.creerMineMateriaux,
                        "creerMineEnergie" : self.creerMineEnergie,
                        "creerHangar" : self.creerHangar,
                        "creerReacteurNucleaire" : self.creerReacteurNucleaire,
                        "productionFerme" : self.productionFerme,
                        "productionMineArgent" : self.productionMineArgent,
                        "productionMineMateriaux" : self.productionMineMateriaux,
                        "productionMineEnergie" : self.productionMineEnergie,
                        "productionReacteurNucleaire" : self.productionReacteurNucleaire,}
        # -------------------------- #
        
    def creermineur(self, planete):
        rx = randint(-25, 25)
        ry = randint(-25, 25)
        
        v = Mineur(self.nom, self.planetemere.x + rx, self.planetemere.y + ry)
        self.flotte.append(v)
        
        print("Vaisseau", v.id)
        print("Type: ", v.type)
        print("Combat: ", v.combat)
        print("HP: ", v.hp)
        print("Atk: ", v.atk)
        print("Vts: ", v.vitesse)
        print("Cout: ", v.cout)
        print("Pop: ", v.pop)
        
    def creerexploreur(self, planete):
        rx = randint(-25, 25)
        ry = randint(-25, 25)
        
        v = Exploreur(self.nom, self.planetemere.x + rx, self.planetemere.y + ry)
        self.flotte.append(v)
        
        print("Vaisseau", v.id)
        print("Type: ", v.type)
        print("Combat: ", v.combat)
        print("HP: ", v.hp)
        print("Atk: ", v.atk)
        print("Vts: ", v.vitesse)
        print("Cout: ", v.cout)
        print("Pop: ", v.pop)
        
    def creerfregate(self, planete):
        rx = randint(-25, 25)
        ry = randint(-25, 25)
        
        v = Fregate(self.nom, self.planetemere.x + rx, self.planetemere.y + ry)
        self.flotte.append(v)
        
        print("Vaisseau", v.id)
        print("Type: ", v.type)
        print("Combat: ", v.combat)
        print("HP: ", v.hp)
        print("Atk: ", v.atk)
        print("Vts: ", v.vitesse)
        print("Cout: ", v.cout)
        print("Pop: ", v.pop)
        
    def creerchasseur(self, planete):
        rx = randint(-25, 25)
        ry = randint(-25, 25)
        
        v = Chasseur(self.nom, self.planetemere.x + rx, self.planetemere.y + ry)
        self.flotte.append(v)
        
        print("Vaisseau", v.id)
        print("Type: ", v.type)
        print("Combat: ", v.combat)
        print("HP: ", v.hp)
        print("Atk: ", v.atk)
        print("Vts: ", v.vitesse)
        print("Cout: ", v.cout)
        print("Pop: ", v.pop)
    
    def creerbombarde(self, planete):
        rx = randint(-25, 25)
        ry = randint(-25, 25)
        
        v = Bombarde(self.nom, self.planetemere.x + rx, self.planetemere.y + ry)
        self.flotte.append(v)
        
        print("Vaisseau", v.id)
        print("Type: ", v.type)
        print("Combat: ", v.combat)
        print("HP: ", v.hp)
        print("Atk: ", v.atk)
        print("Vts: ", v.vitesse)
        print("Cout: ", v.cout)
        print("Pop: ", v.pop)
        
    def creerdreadnought(self, planete):
        rx = randint(-25, 25)
        ry = randint(-25, 25)
        
        v = Dreadnought(self.nom, self.planetemere.x + rx, self.planetemere.y + ry)
        self.flotte.append(v)
        
        print("Vaisseau", v.id)
        print("Type: ", v.type)
        print("Combat: ", v.combat)
        print("HP: ", v.hp)
        print("Atk: ", v.atk)
        print("Vts: ", v.vitesse)
        print("Cout: ", v.cout)
        print("Pop: ", v.pop)
        
    def creerdestructeur(self, planete):
        rx = randint(-25, 25)
        ry = randint(-25, 25)
        
        v = Destructeur(self.nom, self.planetemere.x + rx, self.planetemere.y + ry)
        self.flotte.append(v)
        
        print("Vaisseau", v.id)
        print("Type: ", v.type)
        print("Combat: ", v.combat)
        print("HP: ", v.hp)
        print("Atk: ", v.atk)
        print("Vts: ", v.vitesse)
        print("Cout: ", v.cout)
        print("Pop: ", v.pop)
        
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
                pass
                    
    def prochaineactionWIP(self):
        for i in self.flotte:
            if i.cible and isinstance(i, Mineur):
                if i.minevalide:
                    i.avancer()
                    i.miner()
                else:
                    print("Impossible de miner cet endroit")
            
            elif i.cible and isinstance(i, Exploreur):
                if i.explovalide:
                    i.avancer()
                    i.decouvrir()
                else:
                    print("Impossible d'explorer cet endroit")
                    
            elif i.cible and isinstance(i, Vaisseau):       # Pour les vaisseaux offensifs; Mineur et Exploreur déjà vérifiés
                pass
            
            else:
                pass

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
