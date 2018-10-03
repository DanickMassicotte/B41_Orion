# -*- coding: utf-8 -*-
import random
import time
import math
random.seed()


class MonstreIntersideral():
    def __init__(self,pointeurModele,x,y): #bcp de placeholders à ajuster au fur et à mesure
        self.pointeurModele = pointeurModele
        self.x = x
        self.y = y
        self.genese = time.time() 
        self.pointsDeVie = 1000
        self.puissance = 100
        self.grandeurInvasion = 0
        self.porteeMonstre = 0
        self.compteurHorsPortee = 0
        self.nbPlanetesInfectees = 0
        self.nbEtoilesDevorees = 0
        self.nbAsteroidesDevores = 0
        self.listeProgenitures = []
        self.listeMessages= []
        self.initMessages()
        
    def initMessages(self):
        self.listeMessages.append("Je vais dévorer votre monde!")
        self.listeMessages.append("Vos étoiles s'éteignent, une à une!")
        self.listeMessages.append("Votre futile résistance... nourrie ma haine!")
        self.listeMessages.append("Je suis éternel! JE SUIS INFINI!")
        self.listeMessages.append("J'ai éteint des trillons d'espèces, vous n'êtes que les plus récentes à subir mon étreinte mortelle!")
        self.listeMessages.append("ph'nglui mglw'nafh Cthulhu R'lyeh wgah'nagl fhtagn")
        self.listeMessages.append("Cahf ah nafl mglw'nafh hh' ahor syha'h ah'legeth, ng llll or'azath syha'hnahh n'ghftephai n'gha ahornah ah'mglw'nafh")
        self.listeMessages.append("Y'ephairemake ymg'nilgh'rishuggogg")
        self.listeMessages.append("The og mgn'ghftephai ot ya ymg'ephaich'nglui'ahog feeble lloigg")
        
    def updateGrandeurInvasion(self):
        nombreMinutesPassees = math.floor(( (time.time() - self.genese) / 60 ))
        self.grandeurInvasion = nombreMinutesPassees + self.nbAsteroidesDevores + ( 2 * self.nbPlanetesInfectees) + (3 * self.nbEtoilesDevorees)
        print("Grandeur invasion =", self.grandeurInvasion)
    
    #pas encore utilisée
    def updatePortee(self):
        self.porteeMonstre = 100 * ( self.nbPlanetesInfectees + self.compteurHorsPortee )
        print("JE M'ÉTEND MONSTRUEUSEMENT : (portée à:", self.porteeMonstre, ")")
        
    def determinerProiesAPortee(self, proie):
        if proie == "planete":
            random.shuffle(self.pointeurModele.planetes)
            for planete in self.pointeurModele.planetes:
                portee = math.sqrt( ( (planete.x -self.x) ** 2 + (planete.y - self.y) ** 2 ) )
                if portee <= self.porteeMonstre and not planete.estOccupee:
                   return planete
        
        elif proie == "vaisseau":
            random.shuffle(self.pointeurModele.listeVaisseaux)
            for vaisseau in self.pointeurModele.listeVaisseaux:
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
        
    def identifierProfilJoueur(self):
        pass
    
    def choixAction(self):
        probabilite = random.randint(0,100)
        print("probabilite=",probabilite)
        if 0 <= probabilite < 20:
            print(self.message())
        elif 20 <= probabilite < 35:
            self.invasion()
        elif 35 <= probabilite <= 100:
            choixAstre = random.randint(0,100) 
            print("choix astre=",choixAstre)
            if 0 <= choixAstre < 20:    #faire des branches selon ce qui est à portée
                self.devorerEtoile()
            elif 20 <= choixAstre < 70:
                self.devorerAsteroides()
            elif 70 <= choixAstre < 100:
                self.infecterPlanete()
            
    def message(self):
        message = random.choice(self.listeMessages) # *** faudrait que la vue affiche le message dans frame en haut ou en bas ***
        return message
    
    def invasion(self):
        self.updateGrandeurInvasion()
        for nbProgenitures in range(self.grandeurInvasion):
            progeniture = ProgenitureInfernale(self.x, self.y)
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
            print("Aucune étoile à portée...")
            self.compteurHorsPortee += 1
        
    def devorerAsteroides(self):
        self.updatePortee()
        asteroideCible = self.determinerProiesAPortee("asteroide")
        if asteroideCible != -1:
            print("je dévore astéroïde à:", asteroideCible.x, asteroideCible.y)
            del asteroideCible
            self.nbAsteroidesDevores += 1
        else:
            print("Aucun astéroïde à portée...")
            self.compteurHorsPortee += 1
    
    def infecterPlanete(self):
        self.updatePortee()
        planeteCible = self.determinerProiesAPortee("planete")
        if planeteCible != -1:
            planeteCible.estOccupee = True
            print("j'infecte planète à:", planeteCible.x, planeteCible.y, planeteCible.estOccupee)
            self.nbPlanetesInfectees += 1
        else:
            print("Aucune planète à portée...")
            self.compteurHorsPortee += 1
            
class ProgenitureInfernale():
    def __init__(self,x,y):
        self.x = x
        self.y = y
        #***print("Infernal Spawn")

# ----------------------------------------------------- #
#               section tests locaux
# ----------------------------------------------------- #

class ModeleMonstre():
    def __init__(self):
        self.monstre = MonstreIntersideral(self,500,500)
        self.planetes = []
        self.listeVaisseaux = ["Vaisseau1", "Vaisseau2", "Vaisseau3"]
        self.listeEtoiles = []
        self.listeAsteroides = []
        self.genererAstres()
        
    def genererAstres(self):
        for i in range(10):
            self.planetes.append(PlaneteMonstre(random.randint(0,1000), random.randint(0,1000))) 
            self.listeEtoiles.append(EtoileMonstre(random.randint(0,1000), random.randint(0,1000))) 
            self.listeAsteroides.append(AsteroideMonstre(random.randint(0,1000), random.randint(0,1000))) 

class PlaneteMonstre():
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.estOccupee = False
        
class EtoileMonstre():
    def __init__(self,x,y):
        self.x = x
        self.y = y
        
class AsteroideMonstre():
    def __init__(self,x,y):
        self.x = x
        self.y = y
       

if __name__ == '__main__':
   modele = ModeleMonstre()
   while 1:
       modele.monstre.choixAction()
       time.sleep(2)