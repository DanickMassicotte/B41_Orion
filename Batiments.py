## -*- coding: utf-8 -*-

class Pod():                                # Logement (Augmente la population maximale)
    coutEnArgent=100
    coutEnMateriaux=100
    capaciteOccupants=10
    nbOccupants=10
    
    def __init__(self):
        self.niveau=1
        self.consommationEnergie=0.1
        self.nbOccupants=10
       
class Ferme():                              # (Augmente la quantite de nourriture produite)
    coutEnArgent=100
    coutEnMateriaux=100
         
    def __init__(self):
        self.niveau=1
        self.consommationEnergie=0.1
        self.capaciteProduction = 0.1
        self.vitesse = 1
        
    def produire(self):
        return self.capaciteProduction * self.vitesse


class MineArgent():                         # (Accumule de l'argent)
    coutEnArgent=100
    coutEnMateriaux=100
    
    def __init__(self):
        self.niveau=1
        self.consommationEnergie=0.1
        self.capaciteProduction = 0.1
        self.vitesse = 1 
        
    def miner(self):
        return self.capaciteProduction * self.vitesse
        

class MineMateriaux():                      # (Accumule des materiaux de construction)
    coutEnArgent=100
    coutEnMateriaux=100
    
    def __init__(self):
        self.niveau=1
        self.consommationEnergie=0.1
        self.capaciteProduction = 0.1
        self.vitesse = 1 
        
    def miner(self):
        return self.capaciteProduction * self.vitesse
        

class MineEnergie():                        # (Accumule de la matiere transformable en energie)
    coutEnArgent=100
    coutEnMateriaux=100
    
    def __init__(self):
        self.niveau=1
        self.consommationEnergie=0.1
        self.capaciteProduction = 0.1
        self.vitesse = 1 
        
    def miner(self):
        return self.capaciteProduction * self.vitesse
  
  
class Hangar():                                # Permet de créer des vaisseaux
    coutEnArgent=100
    coutEnMateriaux=100
    
    def __init__(self):
        self.niveau=1
        self.consommationEnergie=0.1
        
class ReacteurNucleaire():                      # Transforme le minerai nucleaire en energie
    coutEnArgent=100
    coutEnMateriaux=100
    
    def __init__(self):
        self.niveau=1
        self.consommationEnergie=0.1
        self.capaciteProduction = 0.05
        self.vitesse = 1
        
    def produire(self):
        return self.capaciteProduction * self.vitesse

  