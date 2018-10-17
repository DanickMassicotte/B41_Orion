# -*- coding: utf-8 -*-
import random
import time
from threading import Timer
import math
from ObjetsJeu import *


class MonstreIntersideral():
    def __init__(self,pointeurModele,x,y): #bcp de placeholders à ajuster au fur et à mesure
        self.pointeurModele = pointeurModele
        # -----------DM------------ #
        self.id = 9999
        # ------------------------- #
        self.x = x
        self.y = y
        self.frequenceTour = 3.0    #nb de secondes entre chaque tour du monstre
        self.genese = 0
        self.seed = 0
        self.hp = 1000
        self.puissance = 100
        self.grandeurInvasion = 0
        self.porteeMonstre = 0
        self.compteurHorsPortee = 0  
        self.distanceCritique = 100
        self.cible = None
        self.tempsPreparation = 10  #nb de secondes de préparation avant d'attaquer
        self.nbPlanetesInfectees = 0
        self.nbEtoilesDevorees = 0
        self.nbAsteroidesDevores = 0
        self.idProgeniture = 77777
        self.listeProgenitures = []
        self.initProgenitures()
        self.listeMessages= []
        self.initMessages()
        self.messageCourant = "Ma sombre conquête... débute!!!"
        self.choixAction()
        
        
    def initMessages(self):
        self.listeMessages.append("Je vais dévorer votre monde!")
        self.listeMessages.append("Vos étoiles s'éteignent, une à une!")
        self.listeMessages.append("Votre futile résistance... nourrie ma haine!")
        self.listeMessages.append("Je suis éternel! JE SUIS INFINI!")
        self.listeMessages.append("J'ai éteint des trillons d'espèces, vous n'êtes que les plus récentes à subir mon étreinte mortelle!")
        self.listeMessages.append("ph'nglui mglw'nafh Cthulhu R'lyeh wgah'nagl fhtagn")
        self.listeMessages.append("Cahf ah nafl mglw'nafh hh' ahor syha'h ah'legeth, ng llll or'azath syha'hnahh n'ghftephai n'gha ahornah ah'mglw'nafh")
        self.listeMessages.append("Y'ephairemake ymg'nilgh'rishuggogg")
        self.listeMessages.append("Og mgn'ghftephai ot ya ymg'ephaich'nglui'ahog feeble lloigg")
        
    def initProgenitures(self):
        for i in range(3):
            progeniture = ProgenitureInfernale(self, self.x, self.y, self.idProgeniture)
            self.idProgeniture += 777
            self.listeProgenitures.append(progeniture)
            
        
    def updateGrandeurInvasion(self):
        grandeurInvasionActuelle = self.grandeurInvasion
        nombreMinutesPassees = math.floor(( (time.time() - self.genese) / 60 )) 
        self.grandeurInvasion = 3 + nombreMinutesPassees + self.nbAsteroidesDevores + ( 2 * self.nbPlanetesInfectees) + (3 * self.nbEtoilesDevorees) - grandeurInvasionActuelle
        #print("Grandeur invasion =", self.grandeurInvasion)
    
    def updatePortee(self):
        porteeAnterieure = self.porteeMonstre
        self.porteeMonstre = 25 * ( self.nbPlanetesInfectees + self.compteurHorsPortee )
        if porteeAnterieure < self.porteeMonstre:
            print("JE M'ÉTEND MONSTRUEUSEMENT : (portée à:", self.porteeMonstre, ")")
        
    def determinerProiesAPortee(self, proie):
        if proie == "planete" and self.pointeurModele.planetes :
            random.shuffle(self.pointeurModele.planetes)
            for planete in self.pointeurModele.planetes:
                portee = math.sqrt( ( (planete.x -self.x) ** 2 + (planete.y - self.y) ** 2 ) )
                if portee <= self.porteeMonstre and not planete.estOccupee and not planete.estInfectee:
                   return planete
        
        elif proie == "vaisseau":
            for key in self.pointeurModele.joueurs:
                random.shuffle(joueurs[key].flotte)
                for vaisseau in joueurs[key].flotte:
                    portee = math.sqrt( ( (vaisseau.x -self.x) ** 2 + (vaisseau.y - self.y) ** 2 ) )
                    if portee <= self.porteeMonstre:
                        return vaisseau
        
        elif proie == "etoile" and self.pointeurModele.listeEtoiles:
            random.shuffle(self.pointeurModele.listeEtoiles)
            for indiceEtoile in range(len(self.pointeurModele.listeEtoiles)):
                portee = math.sqrt( ( (self.pointeurModele.listeEtoiles[indiceEtoile].x -self.x) ** 2 + (self.pointeurModele.listeEtoiles[indiceEtoile].y - self.y) ** 2 ) )
                if portee <= self.porteeMonstre:
                    return self.pointeurModele.listeEtoiles.pop(indiceEtoile)
        
        elif proie == "asteroide" and self.pointeurModele.listeAsteroides:
            random.shuffle(self.pointeurModele.listeAsteroides)
            for indiceAsteroide in range(len(self.pointeurModele.listeAsteroides)):
                portee = math.sqrt( ( (self.pointeurModele.listeAsteroides[indiceAsteroide].x -self.x) ** 2 + (self.pointeurModele.listeAsteroides[indiceAsteroide].y - self.y) ** 2 ) )
                if portee <= self.porteeMonstre:
                   return self.pointeurModele.listeAsteroides.pop(indiceAsteroide)
        
        return -1
        

    def choixAction(self):
       #synchronisation des seeds, probablement pas optimal mais fonctionne pour l'instant
        random.seed(self.seed)
        self.seed += 75737 #incrément magique 
      
        #si une vaisseau est trop près de lui, le monstre va l'attaquer
        if self.hp <= 0: #p-e mettre dans modele ***
            self.pointeurModele.parent.gameOver()
        self.cible = self.detectionMenace()
        if self.cible is not None:
            self.attaquer()
        #sinon, son tour est basé sur la probabilité
        else: 
            probabiliteNiveau1 = random.randint(0,100) + self.modulateurProbabiliteNiveau1()
            if probabiliteNiveau1 < 50:
                self.messageCourant = self.message()
            else:
                probabiliteNiveau2 = random.randint(0,100) + self.modulateurProbabiliteNiveau2()
                if  probabiliteNiveau2 < 50:
                    self.invasion()
                else:
                    probabiliteNiveau3 = random.randint(0,100) + self.modulateurProbabiliteNiveau3()
                    if probabiliteNiveau3 < 40:   
                        self.devorerAsteroides()
                    elif 40 >= probabiliteNiveau3 < 85:
                        self.infecterPlanete()
                    elif probabiliteNiveau3 >= 85:
                        self.devorerEtoile()

        if self.hp > 0:
            prochainTour = Timer(self.frequenceTour,self.choixAction).start() # si le monstre vie, on rappel la fonction après t temps où t = self.frequenceTour

        
    def modulateurProbabiliteNiveau1(self):
        if time.time() - self.genese  < self.tempsPreparation: # profil néophyte == plus de chances tomber sur messag
            return -10 
        else:
            return 25
        
    def modulateurProbabiliteNiveau2(self):
        profilBelligerant = 0
        profilExpansionniste = 0
        if self.pointeurModele.planetes:
            for planeteOccupee in self.pointeurModele.planetes:
                if planeteOccupee.estOccupee:
                    profilExpansionniste += 1
            for key in self.pointeurModele.joueurs:
                for vaisseau in self.pointeurModele.joueurs[key].flotte:
                    if isinstance(vaisseau, Mineur) or isinstance(vaisseau, Exploreur):
                        profilExpansionniste += 1
                    else:
                        profilBelligerant += 1
        if profilBelligerant > profilExpansionniste:
            return -10
        elif profilExpansionniste > profilBelligerant:
            return 10
        else:           
            return 0;
        
    def modulateurProbabiliteNiveau3(self):
        return 0; #ne semble pas nécessaire pour l'instant
            
    def detectionMenace(self):
        for key in self.pointeurModele.joueurs:
            for vaisseau in self.pointeurModele.joueurs[key].flotte:
                if math.sqrt( ( (vaisseau.x - self.x) ** 2 + (vaisseau.y - self.y) ** 2 ) ) < self.distanceCritique and vaisseau.hp > 0:
                    return vaisseau
        return None
    
    def attaquer(self):
        if self.cible.hp > 0:
            self.cible.hp -= self.puissance
            #print("Le monstre attaque:", self.cible)
        else:
            self.cible = None
    
    def message(self):
        message = random.choice(self.listeMessages) # *** faudrait que la vue affiche le message dans frame en haut ou en bas ***
        return message
    
    def invasion(self):
        self.updateGrandeurInvasion()
        for nbProgenitures in range(self.grandeurInvasion):
            progeniture = ProgenitureInfernale(self, self.x, self.y, self.idProgeniture)
            self.listeProgenitures.append(progeniture)
            self.idProgeniture += 777
        #print("Invasion")
        
    def devorerEtoile(self):
        self.updatePortee()
        etoileCible = self.determinerProiesAPortee("etoile")
        if etoileCible != -1:
            print("je dévore étoile à:", etoileCible.x, etoileCible.y)
            del etoileCible
            self.nbEtoilesDevorees += 1
        else:
            #print("Aucune étoile à portée...")
            self.compteurHorsPortee += 1
        
    def devorerAsteroides(self):
        self.updatePortee()
        asteroideCible = self.determinerProiesAPortee("asteroide")
        if asteroideCible != -1:
            print("je dévore astéroïde à:", asteroideCible.x, asteroideCible.y)
            del asteroideCible
            self.nbAsteroidesDevores += 1
        else:
            #print("Aucun astéroïde à portée...")
            self.compteurHorsPortee += 1
    
    def infecterPlanete(self):
        self.updatePortee()
        planeteCible = self.determinerProiesAPortee("planete")
        if planeteCible != -1:
            planeteCible.estInfectee = True
            print("j'infecte planète à:", planeteCible.x, planeteCible.y, planeteCible.estInfectee)
            self.nbPlanetesInfectees += 1
        else:
            self.compteurHorsPortee += 1
    
    def actionsProgenitures(self):
        if self.listeProgenitures:
            for progeniture in self.listeProgenitures:
                progeniture.procedure()
            
class ProgenitureInfernale():
    def __init__(self,pointeurMonstre,x,y, idProgeniture):
        self.pointeurMonstre = pointeurMonstre
        self.x = x
        self.y = y
        self.id = idProgeniture
        self.seedProgeniture = self.pointeurMonstre.genese + self.id
        self.geneseProgeniture = time.time()
        self.tempsGestation = 200
        self.mutant = False
        self.hp = 10
        self.puissance = 2
        self.porteeAttaque = 50
        self.vitesse = 1
        self.cible = None
        self.frequenceTourProgeniture = 0.1 
        self.procedure()

    def procedure(self):
        random.seed(self.seedProgeniture)
        self.seedProgeniture += self.id
        self.confirmKills()
        if self.hp <= 0:
            self.pointeurMonstre.listeProgenitures.remove(self)
        
        self.interception()
        self.patrouille()
        if (not self.mutant) and (time.time() - self.geneseProgeniture > self.tempsGestation):
            self.mutation()
            
        #if self.cible is None or self.cible.hp <=0 :
           # self.choixCible()
        else:
            if math.sqrt( ( (self.cible.x -self.x) ** 2 + (self.cible.y - self.y) ** 2 ) ) > self.porteeAttaque:
                self.deplacement()
            else:
                self.attaquer()
        if self.hp > 0:
            prochainTourProgeniture = Timer(self.frequenceTourProgeniture,self.procedure).start()   #*****

        
    def choixCible(self):
        listeCibles = []
        for key in self.pointeurMonstre.pointeurModele.joueurs:
            for vaisseau in self.pointeurMonstre.pointeurModele.joueurs[key].flotte:
                listeCibles.append(vaisseau)
            for planeteControlee in self.pointeurMonstre.pointeurModele.joueurs[key].planetescontrolees:
                listeCibles.append(planeteControlee)
        if listeCibles:
            self.cible = random.choice(listeCibles)
        #else:
           # self.cible = random.choice( self.pointeurMonstre.pointeurModele.planetes)
           
        
    def deplacement(self):
        #print("deplacement de ", self.x, self.y, "vers", round(self.cible.x), round(self.cible.y))
        if self.x > round(self.cible.x):
            self.x -= self.vitesse
        if self.x < round(self.cible.x):
            self.x += self.vitesse
            
        if self.y > round(self.cible.y):
            self.y -= self.vitesse
        if self.y < round(self.cible.y):
            self.y += self.vitesse
        
        
    def attaquer(self):
        #print("progéniture à",self.x,self.y, "attaque", self.cible.x, self.cible.y, "vie cible:", self.cible.hp)
        if isinstance(self.cible,Planete):
            if not self.cible.estOccupee:
                return None
        if self.cible.hp > 0:
            self.cible.hp -= self.puissance
        else:
            self.cible = None
            
    
    def mutation(self):
        self.mutant = True
        self.hp = 20
        self.puissance = 5
        self.vitesse = 3
        self.porteeAttaque = 25
        
    def confirmKills(self):
        for key in self.pointeurMonstre.pointeurModele.joueurs:
            for vaisseau in self.pointeurMonstre.pointeurModele.joueurs[key].flotte:
                if vaisseau.hp <= 0:
                    self.pointeurMonstre.pointeurModele.joueurs[key].flotte.remove(vaisseau)
                    
    def interception(self):
        for key in self.pointeurMonstre.pointeurModele.joueurs:
            for vaisseau in self.pointeurMonstre.pointeurModele.joueurs[key].flotte:
                if math.sqrt( ( (vaisseau.x - self.pointeurMonstre.x) ** 2 + (vaisseau.y - self.pointeurMonstre.y) ** 2 ) ) < self.pointeurMonstre.distanceCritique and vaisseau.hp > 0:
                    self.cible = vaisseau
    
    def patrouille(self):
        absenceCible = True
        for key in self.pointeurMonstre.pointeurModele.joueurs:
            if self.pointeurMonstre.pointeurModele.joueurs[key].flotte:
                absenceCible = False
            if self.pointeurMonstre.pointeurModele.joueurs[key].planetescontrolees:
                absenceCible = False

        if absenceCible:
            if ( self.cible is None ) or math.sqrt( ( (self.x - self.cible.x) ** 2) + ( (self.y - self.cible.y) ** 2)  ) < 100:
                random.shuffle(self.pointeurMonstre.pointeurModele.planetes)
                self.cible = random.choice( self.pointeurMonstre.pointeurModele.planetes)
        
        elif not absenceCible and ( self.cible is None or self.cible.hp <=0):
            self.choixCible()
        
 
                    
            
        
                 
