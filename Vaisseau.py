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
        self.monstre = None
        self.hp = 100
        self.atk = 10
        self.cout = 100
        self.pop = 1
        self.combat = False
        self.rangeAtk = 12
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
        if self.cible:
            if self.cible == self.monstre:
                return True
            else:
                return False
    
    def attaquer(self):
        print("vaisseau �",self.x,self.y, "attaque", self.cible.x, self.cible.y, "vie cible:", self.cible.hp)
        if self.cible.hp > 0:
            self.cible.hp -= self.atk
            print("vie cible apr�s attaque", self.cible.hp)
        else:
            self.cible = None
            print("cible d�truite")
        
class Mineur(Vaisseau):
    def __init__(self, nom, x, y):
        Vaisseau.__init__(self, nom, x, y)
        self.type = "Mineur"                # Sert � certain tests
        self.hp = self.hp * 1
        self.atk = self.atk * 0
        self.vitesse = self.vitesse * 1
        self.cout = self.cout * 1.5
        self.pop = self.pop * 3
        
    def minevalide(self):
        if self.cible:
            if self.cible.mine:     # � r�viser; n'entre pas dans le if...
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
        self.type = "Exploreur"             # Sert � certains tests
        self.hp = self.hp * 1
        self.atk = self.atk * 0
        self.vitesse = self.vitesse * 1
        self.cout = self.cout * 1.5
        self.pop = self.pop * 1
        
    def explovalide(self):
        if self.cible:
            if self.cible.exploration:
                return True
            else:
                return False
    
    def decouvrir(self):
        pass
    
class Fregate(Vaisseau):
    def __init__(self, nom, x, y):
        Vaisseau.__init__(self, nom, x, y)
        self.combat = True
        self.type = "Fregate"               # Sert � certains tests
        self.hp = self.hp * 1
        self.atk = self.atk * 1
        self.vitesse = self.vitesse * 1
        self.cout = self.cout * 0.5
        self.pop = self.pop * 1
                
class Chasseur(Vaisseau):
    def __init__(self, nom, x, y):
        Vaisseau.__init__(self, nom, x, y)
        self.type = "Chasseur"              # Sert � certains tests
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
        self.type = "Bombarde"              # Sert � certains tests
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
        
    # -------------DM--------------- #    
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
        print("CIBLER FLOTTE")
        for i in self.flotte:
            if i.id== int(idori):
                for j in self.parent.planetes:
                    if j.id== int(iddesti):
                        i.cible=j
                        print("GOT TARGET")
                        return
                    
                # -------------DM------------- #    
                if self.parent.monstre.id == int(iddesti):
                    i.cible = self.parent.monstre
                    i.monstre = self.parent.monstre
                    print("GOT MONSTRE")
                # ---------------------------- #
                    
    def prochaineaction1(self):
        for i in self.flotte:
            if i.cible:
                i.avancer()
            else:
                pass
            
    def prochaineaction(self):
        for i in self.flotte:
            if i.cible and isinstance(i, Mineur):
                i.avancer()
            
            elif i.cible and isinstance(i, Exploreur):
                i.avancer()
                
            elif i.cible and isinstance(i, Vaisseau):       # Pour les vaisseaux offensifs; Mineur et Exploreur d�j� v�rifi�s
                if i.attaquevalide():
                    if math.sqrt(((i.cible.x - i.x) ** 2 + (i.cible.y - i.y) ** 2 )) > i.rangeAtk:
                        i.avancer()
                    else:
                        i.attaquer()
                
                else:
                    i.avancer()
                    
            
            else:
                pass
            
    # --------------DM-------------- #
            
"""
Dans Controleur: 

    def creermineur(self):
        self.actions.append([self.monnom, "creermineur", ""])
        
    def creerexploreur(self):
        self.actions.append([self.monnom, "creerexploreur", ""])
        
    def creerfregate(self):
        self.actions.append([self.monnom, "creerfregate", ""])
        
    def creerchasseur(self):
        self.actions.append([self.monnom, "creerchasseur", ""])

"""