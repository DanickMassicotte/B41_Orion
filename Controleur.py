## -*- coding: UTF-8 -*-
from tkinter import *
import os,os.path
import sys
import xmlrpc.client
import socket
import random
import time
from subprocess import Popen 
from helper import Helper as hlp
from Vue import *
from Modele import *
from ObjetsJeu import *

class Controleur():
    def __init__(self):

        print("IN CONTROLEUR")
        self.attente=0
        self.cadre=0 # le no de cadre pour assurer la syncronisation avec les autres participants
        self.tempo=0 # insert a reconnaitre qu'on a lance le serveur et qu'on peut s'inscrire automatiquement sans cliquer sur inscription dans l'interface
                     # ne peut pas etre remplace par egoserveur car si cette variable test a vrai (1), l'inscription est effectuee et tempo remis a 0 pour ne pas reinscrire deux fois...
                     # NOTE le nom de variable est ici epouvantable, j'en conviens - devrait quelquechose comme 'autoInscription'
        self.egoserveur=0 # est-ce que je suis celui qui a demarre le serveur, a priori, non (0)
        self.actions=[]    # la liste de mes actions a envoyer au serveur pour qu'il les redistribue a tous les participants
        self.statut=0 # etat dans le quel je me trouve : 0 -> rien, 1 -> inscrit, 2 -> demarre, 3-> joue
        self.monip=self.trouverIP() # la fonction pour retourner mon ip
        self.monnom=self.generernom() # un generateur de nom pour faciliter le deboggage (comme il genere un nom quasi aleatoire et on peut demarrer plusieurs 'participants' sur une même machine pour tester)
        self.modele=None
        self.serveur=None
        self.vue=Vue(self,self.monip,self.monnom)
        self.vue.root.mainloop()
        
    def trouverIP(self): # fonction pour trouver le IP en 'pignant' gmail
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # on cree un socket
        s.connect(("gmail.com",80))    # on envoie le ping
        monip=s.getsockname()[0] # on analyse la reponse qui contient l'IP en position 0 
        s.close() # ferme le socket
        return monip
    
    def generernom(self):  # generateur de nouveau nom - accelere l'entree de nom pour les tests - parfois � peut generer le meme nom mais c'est rare
        monnom="jmd_"+str(random.randrange(1000))
        return monnom

    def creerpartie(self):
        if self.egoserveur==0:
            pid=Popen([sys.executable,"./2018_orion_mini_serveur.py"],shell=1).pid # on lance l'application serveur
            self.egoserveur=1 # on note que c'est soi qui, ayant demarre le serveur, aura le privilege de lancer la simulation
            self.tempo=1 # on change d'etat pour s'inscrire automatiquement 
                         # (parce que dans ce type de programme on prend pour acquis que celui qui prepare la simulation veut aussi y participer)

    # NOTE si on demarre le serveur, cette fonction est appellee pour nous (voir timer et variable tempo)
    #      ou par un clique sur le bouton 'Creerunclient' du layout
    def inscrirejoueur(self):
        ipserveur=self.vue.ipSplash.get() # lire le IP dans le champ du layout
        nom=self.vue.nomSplash.get() # noter notre nom
        if ipserveur and nom:
            ad="http://"+ipserveur+":9999"
            self.serveur=xmlrpc.client.ServerProxy(ad)
            self.monnom=nom
            rep=self.serveur.inscrireclient(self.monnom)    # on averti le serveur de nous inscrire
            #tester retour pour erreur de nom
            self.statut=1 # statut 1 == attente de lancement de partie
            random.seed(rep[2])
            
    ## ----------- FONCTION POUR CELUI QUI A CREE LA PARTIE SEULEMENT
    def lancerpartie(self): # reponse du bouton de lancement de simulation (pour celui qui a parti le serveur seulement)
        rep=self.serveur.lancerpartie() 
        print("REP DU LANCER",rep)
        if rep==1:
            self.statut=3 # il change son statut pour lui permettre d'initer la simulation, les autres sont en 1 (attente) - voir timer.py
    ## ----------- FIN --
    
    def initierpartie(self,rep):  # initalisation locale de la simulation, creation du modele, generation des assets et suppression du layout de lobby
        if rep[1][0][0]=="lancerpartie":
            self.modele=Modele(self,rep[1][0][1]) # on cree le modele
        #-----------------------------------------------------------#
            #synchronisation de genese et seed
            self.modele.monstre.genese = round(time.time())
            self.modele.monstre.seed = self.modele.monstre.genese
        #-----------------------------------------------------------#  
            self.vue.creeraffichercadrepartie(self.modele)
            print(self.monnom,"LANCE PROCHAINTOUR")
            self.prochaintour()

    def boucleattente(self):
        print("IN BOUCLEATTENTE")
        rep=self.serveur.faireaction([self.monnom,0,0])
        print("RETOUR DU faire action  SERVEUR",rep)
        if rep[0]:
            print("Recu ORDRE de DEMARRER")
            # PATCH pour dico in xmlrpc qui requiert des chaines comme cles
            # On a recu un cle str qu'on retransforme en int (pour compter les cadres de jeu, servant a distribuer les taches)
            cle=list(rep[2].keys())[0]
            rep[2]={int(cle):rep[2][cle]}  # on transforme la cle de str à int avant le transfert - voir aussi prochaintour (plus bas)
            # fin de patch
            self.initierpartie(rep[2])
        elif rep[0]==0:
            self.vue.affichelisteparticipants(rep[2])
            self.vue.root.after(1000,self.boucleattente)
        
    def prochaintour(self): # la boucle de jeu principale, qui sera appelle par la fonction bouclejeu du timer
        if self.serveur: # s'il existe un serveur
            self.cadre=self.cadre+1 # increment du compteur de cadre
            if self.attente==0:
                self.modele.prochaineaction(self.cadre)    # mise a jour du modele
                self.vue.afficherpartie(self.modele) # mise a jour de la vue
            if self.actions: # si on a des actions a partager 
                rep=self.serveur.faireaction([self.monnom,self.cadre,self.actions]) # on les envoie 
            else:
                rep=self.serveur.faireaction([self.monnom,self.cadre,0]) # sinon on envoie rien au serveur on ne fait que le pigner 
                                                                        # (HTTP requiert une requete du client pour envoyer une reponse)
            self.actions=[] # on s'assure que les actions a`envoyer sont maintenant supprimer (on ne veut pas les envoyer 2 fois)
            if rep[0]: # si le premier element de reponse n'est pas vide
                
                # PATCH de dico in xmlrpc (vs Pyro utilise avant)
                cle=list(rep[2].keys())[0]
                #print("AVANT",rep[2])
                rep[2]={int(cle):rep[2][cle]}
                #print("APRES",rep[2])
                # FIN DE PATCH
                
                for i in rep[2]:   # pour chaque action a faire (rep[2] est dictionnaire d'actions en provenance des participants
                                   # dont les cles sont les cadres durant lesquels ses actions devront etre effectuees
                    if i not in self.modele.actionsafaire.keys(): # si la cle i n'existe pas
                        self.modele.actionsafaire[i]=[] #faire une entree dans le dictonnaire
                    for k in rep[2][i]: # pour toutes les actions lies a une cle du dictionnaire d'actions recu
                        self.modele.actionsafaire[i].append(k) # ajouter cet action au dictionnaire sous l'entree dont la cle correspond a i
            if rep[1]=="attend": # si jamais rep[0] est vide MAIS que rep[1] == 'attend', on veut alors patienter
                self.cadre=self.cadre-1  # donc on revient au cadre initial
                self.attente=1
                #print("ALERTE EN ATTENTE",self.monnom)
            else:
                self.attente=0
            self.vue.root.after(20,self.prochaintour)
        else:
            print("Aucun serveur connu")
            
    def fermefenetre(self):
        if self.serveur:
            self.serveur.jequitte(self.monnom)
        self.vue.root.destroy()
        
    # -------------DM---------------- #    
    def creermineur(self):
        self.actions.append([self.monnom, "creermineur", ""])
        
    def creerexploreur(self):
        self.actions.append([self.monnom, "creerexploreur", ""])
        
    def creerfregate(self):
        self.actions.append([self.monnom, "creerfregate", ""])
        
    def creerchasseur(self):
        self.actions.append([self.monnom, "creerchasseur", ""])
    # -------------DM---------------- #
        
    def ciblerflotte(self,idorigine,iddestination):
        self.actions.append([self.monnom,"ciblerflotte",[idorigine,iddestination]])
        
    # DEBUT AJOUTS BATIMENTS JCB !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!         
    def creerPod(self):
        self.actions.append([self.monnom, "creerPod",""])
        
    def creerFerme(self):
        self.actions.append([self.monnom, "creerFerme",""])
    
    def creerHangar(self):
        self.actions.append([self.monnom, "creerHangar",""])
    
    def creerMineArgent(self):
        self.actions.append([self.monnom, "creerMineArgent",""])
        
    def creerMineMateriaux(self):
        self.actions.append([self.monnom, "creerMineMateriaux",""])
        
    def creerMineEnergie(self):
        self.actions.append([self.monnom, "creerMineEnergie",""])
        
    def creerReacteurNucleaire(self):
        self.actions.append([self.monnom, "creerReacteurNucleaire",""])
# FIN AJOUTS BATIMENTS JCB !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!  
    
    def gameOver(self):
        print("jeu fini")
        #ajouter procédure de fin de jeu