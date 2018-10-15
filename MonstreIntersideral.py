# -*- coding: utf-8 -*-
import random
import time
from threading import Timer
import math

class MonstreIntersideral():
    def __init__(self,pointeurModele,seed,x,y): #bcp de placeholders à ajuster au fur et à mesure
        self.pointeurModele = pointeurModele
        self.x = x
        self.y = y
        self.seed = seed #prendre la mm seed que le serveur pour synchroniser les monstres
        random.seed(self.seed)
        self.frequenceTour = 1.0 #nb de secondes entre chaque tour du monstre
        self.genese = time.time() 
        self.hp = 1000
        self.puissance = 100
        self.grandeurInvasion = 0
        self.porteeMonstre = 0
        self.compteurHorsPortee = 0  
        self.distanceCritique = 100
        self.cible = None
        self.tempsPreparation = 0          #nb de secondes de préparation avant d'attaquer
        self.nbPlanetesInfectees = 0
        self.nbEtoilesDevorees = 0
        self.nbAsteroidesDevores = 0
        self.listeProgenitures = []
        self.listeMessages= []
        self.initMessages()
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
        
    def updateGrandeurInvasion(self):
        nombreMinutesPassees = math.floor(( (time.time() - self.genese) / 60 )) 
        self.grandeurInvasion = nombreMinutesPassees + self.nbAsteroidesDevores + ( 2 * self.nbPlanetesInfectees) + (3 * self.nbEtoilesDevorees)
        print("Grandeur invasion =", self.grandeurInvasion)
    
    def updatePortee(self):
        porteeAnterieure = self.porteeMonstre
        self.porteeMonstre = 25 * ( self.nbPlanetesInfectees + self.compteurHorsPortee )
        if porteeAnterieure < self.porteeMonstre:
            print("JE M'ÉTEND MONSTRUEUSEMENT : (portée à:", self.porteeMonstre, ")")
        
    def determinerProiesAPortee(self, proie):
        if proie == "planete":
            random.shuffle(self.pointeurModele.planetes)
            for planete in self.pointeurModele.planetes:
                portee = math.sqrt( ( (planete.x -self.x) ** 2 + (planete.y - self.y) ** 2 ) )
                if portee <= self.porteeMonstre and not planete.estOccupee and not planete.estInfectee:
                   return planete
        
        elif proie == "vaisseau":
            random.shuffle(self.pointeurModele.listeVaisseaux)
            for key in self.pointeurModele.joueurs:
                for vaisseau in joueurs[key].flotte:
                    portee = math.sqrt( ( (vaisseau.x -self.x) ** 2 + (vaisseau.y - self.y) ** 2 ) )
                    if portee <= self.porteeMonstre:
                        return vaisseau
        
        elif proie == "etoile":
            random.shuffle(self.pointeurModele.listeEtoiles)
            for indiceEtoile in range(len(self.pointeurModele.listeEtoiles)):
                portee = math.sqrt( ( (self.pointeurModele.listeEtoiles[indiceEtoile].x -self.x) ** 2 + (self.pointeurModele.listeEtoiles[indiceEtoile].y - self.y) ** 2 ) )
                if portee <= self.porteeMonstre:
                    return self.pointeurModele.listeEtoiles.pop(indiceEtoile)
        
        elif proie == "asteroide":
            random.shuffle(self.pointeurModele.listeAsteroides)
            for indiceAsteroide in range(len(self.pointeurModele.listeAsteroides)):
                portee = math.sqrt( ( (self.pointeurModele.listeAsteroides[indiceAsteroide].x -self.x) ** 2 + (self.pointeurModele.listeAsteroides[indiceAsteroide].y - self.y) ** 2 ) )
                if portee <= self.porteeMonstre:
                   return self.pointeurModele.listeAsteroides.pop(indiceAsteroide)
        
        return -1
        

    def choixAction(self):
        #si une vaisseau est trop près de lui, le monstre va l'attaquer
        if self.hp <= 0: #p-e mettre dans modele ***
            self.pointeurModele.parent.gameOver()
        self.cible = self.detectionMenace()
        if self.cible is not None:
            self.attaquer()
        #sinon, son tour est basé sur la probabilité
        else:    
            probabilite = random.randint(0,100) + self.modificateurProbabilite()
            #print("probabilite=",probabilite)
            if 0 <= probabilite < 20:
                print(self.message())
            elif 20 <= probabilite <= 85:
                choixAstre = random.randint(0,100) 
                #print("choix astre=",choixAstre)
                if 0 <= choixAstre < 20:   
                    self.devorerEtoile()
                elif 20 <= choixAstre < 70:
                    self.devorerAsteroides()
                elif 70 <= choixAstre < 100:
                    self.infecterPlanete()
            elif 85 <= probabilite:
                self.invasion()

        if self.hp > 0: # p-e enlever si on garde le check en haut ***
            prochainTour = Timer(self.frequenceTour,self.choixAction).start() # si le monstre vie, on rappel la fonction après t temps où t = self.frequenceTour
        #dans les deux cas, les progénitures font leur tour, s'il y en a
        self.actionsProgenitures()
        
    def modificateurProbabilite(self):
        #l'AI reconnait 3 profils:  néophyte, expansionniste et belligérant 
        
        if time.time() - self.genese  < self.tempsPreparation: # profil néophyte
            return -10 # plus de chance de tomber sur message
        else:
            profilBelligerant = 0
            profilExpansionniste = 0
            if self.pointeurModele.planetes:
                for planeteOccupee in self.pointeurModele.planetes:
                    if planeteOccupee.estOccupee:
                        profilExpansionniste += 1
                for key in self.pointeurModele.joueurs:
                    for vaisseau in self.pointeurModele.joueurs[key].flotte:
                        if isinstance(vaisseau, Mineur) or isinstance(vaisseau, Explorateur):
                            profilExpansionniste += 1
                        else:
                    
                            if profilBelligerant > profilExpansionniste:
                                return 5
                            elif profilExpansionniste > profilBelligerant:
                                return -5
                            
            return 0;
            
    def detectionMenace(self):
        for key in self.pointeurModele.joueurs:
            for vaisseau in self.pointeurModele.joueurs[key].flotte:
                if math.sqrt( ( (vaisseau.x - self.x) ** 2 + (vaisseau.y - self.y) ** 2 ) ) < self.distanceCritique and vaisseau.hp > 0:
                    return vaisseau
        return None
    
    def attaquer(self):
        if self.cible.hp > 0:
            self.cible.hp -= self.puissance
            print("Le monstre attaque:", self.cible)
        else:
            self.cible = None
    
    def message(self):
        message = random.choice(self.listeMessages) # *** faudrait que la vue affiche le message dans frame en haut ou en bas ***
        return message
    
    def invasion(self):
        self.updateGrandeurInvasion()
        for nbProgenitures in range(self.grandeurInvasion):
            progeniture = ProgenitureInfernale(self, self.x, self.y)
            self.listeProgenitures.append(progeniture)
        print("Invasion")
        
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
            #print("Aucune planète à portée...")
            self.compteurHorsPortee += 1
    
    def actionsProgenitures(self):
        if self.listeProgenitures:
            for progeniture in self.listeProgenitures:
                progeniture.procedure()
            
class ProgenitureInfernale():
    def __init__(self,pointeurMonstre,x,y):
        self.pointeurMonstre = pointeurMonstre
        self.x = x
        self.y = y
        self.hp = 25
        self.puissance = 20
        self.porteeAttaque = 15
        self.vitesse = 10
        self.cible = None

    def procedure(self):
        if not self.isAlive():
            self.pointeurMonstre.listeProgenitures.remove(self)

        if self.cible == None: #si n'a pas de cible, on en sélectionne une
            self.choixCible()
            
        if math.sqrt( ( (self.cible.x -self.x) ** 2 + (self.cible.y - self.y) ** 2 ) ) > self.porteeAttaque:
            self.deplacement()
        else:
            self.attaquer()
            
    def isAlive(self):
        if self.hp>0:
            return True
        else:
            return False
        
    def choixCible(self):
        listeCibles = []
        listeMenaces = []
        listePlanetesOccupees = []
        
        for planete in self.pointeurMonstre.pointeurModele.planetes:
            if planete.estOccupee:
                listePlanetesOccupees.append(planete)
        for key in self.pointeurMonstre.pointeurModele.joueurs:
            for vaisseau in self.pointeurMonstre.pointeurModele.joueurs[key].flotte:
                if vaisseau.hp > 0:
                    if math.sqrt( ( (vaisseau.x - self.pointeurMonstre.x) ** 2 + (vaisseau.y - self.pointeurMonstre.y) ** 2 ) ) < self.pointeurMonstre.distanceCritique:
                        listeMenaces.append(vaisseau)
                        print("détection d'un vaisseau dans une distance critique")
                    else:
                        listeCibles.append(vaisseau)
        
        if listeMenaces:
            self.cible = random.choice(listeMenaces)
        elif listeCibles:
            self.cible = random.choice(listeCibles)
        else:
            self.cible = None
        

    
    def deplacement(self):
        print("deplacement de ", self.x, self.y, "vers", self.cible.x, self.cible.y)
        if self.x > self.cible.x:
            self.x -= self.vitesse
        if self.x < self.cible.x:
            self.x += self.vitesse
            
        if self.y > self.cible.y:
            self.y -= self.vitesse
        if self.y < self.cible.y:
            self.y += self.vitesse
        
        
    def attaquer(self):
        print("progéniture à",self.x,self.y, "attaque", self.cible.x, self.cible.y, "vie cible:", self.cible.hp)
        if self.cible.hp > 0:
            self.cible.hp -= self.puissance
            print("vie cible après attaque", self.cible.hp)
        else:
            self.cible = None
            print("cible détruite")
        

# ----------------------------------------------------- #
#               section tests locaux
# ----------------------------------------------------- #
class ControleurMonstre():
    def __init__(self):
        self.modele = ModeleMonstre(self)
    
    def gameOver(self):
        print("game over")
        
class ModeleMonstre():
    def __init__(self, parent):
        random.seed(7)
        self.parent = parent
        self.planetes = []
        self.joueurs = {}
        self.initJoueurs()
        self.listeEtoiles = []
        self.listeAsteroides = []
        self.genererAstres()
        self.monstre = MonstreIntersideral(self, random.randint(0,1000),500,500)
        self.threadRecursif()
        
    def genererAstres(self):
        for i in range(10):
            self.planetes.append(PlaneteMonstre(random.randint(0,1000), random.randint(0,1000))) 
            self.listeEtoiles.append(EtoileMonstre(random.randint(0,1000), random.randint(0,1000))) 
            self.listeAsteroides.append(AsteroideMonstre(random.randint(0,1000), random.randint(0,1000))) 
            for key in self.joueurs:
                self.joueurs[key].flotte.append(Mineur(self,random.randint(0,1000), random.randint(0,1000)))
                self.joueurs[key].flotte.append(Frigate(self,random.randint(0,1000), random.randint(0,1000)))
        #test vaisseau à côté monstre      
        #self.listeVaisseaux.append(VaisseauMonstre(self,550,550))     
    
    def initJoueurs(self):
        joueur1 = JoueurMonstre()
        joueur2 = JoueurMonstre()
        self.joueurs = {"joueur1": joueur1,
                        "joueur2": joueur2 }
    
    def threadRecursif(self):
        time.sleep(1)
        #print("***** thread principal continue *****")
        for key in self.joueurs:
            for vaisseau in self.joueurs[key].flotte:
                vaisseau.choixCible()
                vaisseau.attaquer()
        self.threadRecursif()
        
class PlaneteMonstre():
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.estOccupee = False
        self.estInfectee = False
        
class EtoileMonstre():
    def __init__(self,x,y):
        self.x = x
        self.y = y
        
class AsteroideMonstre():
    def __init__(self,x,y):
        self.x = x
        self.y = y

class JoueurMonstre():
    def __init__(self):
        self.flotte = []
        
class Mineur():
    def __init__(self,pointeurModele,x,y):
        self.pointeurModele = pointeurModele
        self.x = x
        self.y = y
        self.hp = 150
        self.puissance = 10
        self.cible =None
        self.vitesse = 25
    
    def choixCible(self):
            if self.cible == None and self.pointeurModele.monstre.listeProgenitures:
                self.cible = random.choice(self.pointeurModele.monstre.listeProgenitures)
                #print("vaisseau", self, "trouver cible", self.cible)
                
    def deplacement(self):
            #print("deplacement de ", self.x, self.y, "vers", self.cible.x, self.cible.y)
        if self.x > self.cible.x:
            self.x -= self.vitesse
        if self.x < self.cible.x:
            self.x += self.vitesse
            
        if self.y > self.cible.y:
            self.y -= self.vitesse
        if self.y < self.cible.y:
            self.y += self.vitesse
            
    def attaquer(self):
        #print("progéniture à",self.x,self.y, "attaque", self.cible.x, self.cible.y, "vie cible:", self.cible.hp)
        if self.cible is not None and self.cible.hp > 0:
            self.cible.hp -= self.puissance
            print("vie cible après attaque", self.cible.hp)
        else:
            self.cible = None
            #print("cible détruite")
class Explorateur():
    def __init__(self,pointeurModele,x,y):
        self.pointeurModele = pointeurModele
        self.x = x
        self.y = y
        self.hp = 150
        self.puissance = 10
        self.cible =None
        self.vitesse = 25
    
    def choixCible(self):
            if self.cible == None and self.pointeurModele.monstre.listeProgenitures:
                self.cible = random.choice(self.pointeurModele.monstre.listeProgenitures)
                #print("vaisseau", self, "trouver cible", self.cible)
                
    def deplacement(self):
            #print("deplacement de ", self.x, self.y, "vers", self.cible.x, self.cible.y)
        if self.x > self.cible.x:
            self.x -= self.vitesse
        if self.x < self.cible.x:
            self.x += self.vitesse
            
        if self.y > self.cible.y:
            self.y -= self.vitesse
        if self.y < self.cible.y:
            self.y += self.vitesse
            
    def attaquer(self):
        #print("progéniture à",self.x,self.y, "attaque", self.cible.x, self.cible.y, "vie cible:", self.cible.hp)
        if self.cible is not None and self.cible.hp > 0:
            self.cible.hp -= self.puissance
            print("vie cible après attaque", self.cible.hp)
        else:
            self.cible = None
            #print("cible détruite")
class Frigate():
    def __init__(self,pointeurModele,x,y):
        self.pointeurModele = pointeurModele
        self.x = x
        self.y = y
        self.hp = 150
        self.puissance = 10
        self.cible =None
        self.vitesse = 25
    
    def choixCible(self):
            if self.cible == None and self.pointeurModele.monstre.listeProgenitures:
                self.cible = random.choice(self.pointeurModele.monstre.listeProgenitures)
                #print("vaisseau", self, "trouver cible", self.cible)
                
    def deplacement(self):
            #print("deplacement de ", self.x, self.y, "vers", self.cible.x, self.cible.y)
        if self.x > self.cible.x:
            self.x -= self.vitesse
        if self.x < self.cible.x:
            self.x += self.vitesse
            
        if self.y > self.cible.y:
            self.y -= self.vitesse
        if self.y < self.cible.y:
            self.y += self.vitesse
            
    def attaquer(self):
        #print("progéniture à",self.x,self.y, "attaque", self.cible.x, self.cible.y, "vie cible:", self.cible.hp)
        if self.cible is not None and self.cible.hp > 0:
            self.cible.hp -= self.puissance
            print("vie cible après attaque", self.cible.hp)
        else:
            self.cible = None
            #print("cible détruite")

if __name__ == '__main__':
   control = ControleurMonstre()
  
