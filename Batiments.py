## -*- coding: utf-8 -*-

class Batiment:                                     # Super-classe pour la creation de batiments
    def __init__(self):
        self.coutEnArgent=0
        self.coutEnMateriaux=0
        self.niveau=0
        self.consommationEnergie=0
    

class Pod(Batiment):                                # Logement (Augmente la population maximale)
    def __init__(self):
        Batiment.__init__(self)
        self.capaciteOccupants=10
        self.nbOccupants=10
        self.coutEnArgent = 25
        self.coutEnMateriaux = 25
        self.niveau=1
        self.consommationEnergie=5

       
class Ferme(Batiment):                              # (Augmente la quantite de nourriture produite) 
    def __init__(self):
        Batiment.__init__(self)
        self.capaciteProduction
        self.vitesse = 1
        self.nourritureAccumule = 0
        self.coutEnArgent = 25
        self.coutEnMateriaux = 25
        self.niveau=1
        self.consommationEnergie=5


class MineArgent(Batiment):                         # (Accumule de l'argent)
    def __init__(self):
        Batiment.__init__(self)
        self.capaciteProduction = 10
        self.vitesse = 1 
        self.materiauxAccumule = 0
        
    def miner(self):
        self.materiauxAccumule += self.capaciteProduction * self.vitesse
        

class MineMateriaux(Batiment):                      # (Accumule des materiaux de construction)
    def __init__(self):
        Batiment.__init__(self)
        self.capaciteProduction = 10
        self.vitesse = 1 
        self.materiauxAccumule = 0
        
    def miner(self):
        self.materiauxAccumule += self.capaciteProduction * self.vitesse
        

class MineEnergie(Batiment):                        # (Accumule de la matiere transformable en energie)
    def __init__(self):
        Batiment.__init__(self)
        self.capaciteProduction = 10
        self.vitesse = 1 
        self.materiauxAccumule = 0
        
    def miner(self):
        self.materiauxAccumule += self.capaciteProduction * self.vitesse
  
  
class Hangar(Batiment):                                # Permet de créer des vaisseaux
    def __init__(self):
        Batiment.__init__(self)
        self.coutEnArgent = 25
        self.coutEnMateriaux = 25
        self.niveau=1
        self.consommationEnergie=5
  