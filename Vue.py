# -*- coding: utf-8 -*-
from tkinter import *
import os,os.path
import sys
import xmlrpc.client
import socket
import random
from subprocess import Popen 
from helper import Helper as hlp
from PIL import Image, ImageTk

class Vue():
    def __init__(self,parent,ip,nom):
        self.parent=parent
        self.root=Tk()
        self.largeur=640
        self.hauteur=480
        self.root.protocol("WM_DELETE_WINDOW", self.fermerfenetre)
        self.terrain=[]
        self.cadreactif=None
        self.maselection=None
        self.root.title("Orion")
        self.modele=None
        self.nom=""
        self.cadreapp=Frame(self.root,width=1920,height=950)
        self.cadreapp.grid(row = 0,column = 0)
        self.creercadresplash(ip,nom)
        self.creercadrelobby()
        
    def fermerfenetre(self):
        self.parent.fermefenetre()
        
    def changecadre(self,cadre):
        if self.cadreactif:
            self.cadreactif.grid_forget()
        self.cadreactif=cadre
        self.cadreactif.grid(row = 0,column = 0)
            
    def creercadresplash(self,ip,nom):
        
       self.frameSplash = Frame(self.cadreapp, width = 1920, height = 950)
       self.frameSplashTexte = Frame(self.frameSplash )
       
       self.frameSplash.grid(row = 0, column = 0, sticky = "nsew")
       self.frameSplashTexte.grid(row = 0, column = 0, sticky = "nsew")
       
       self.photoSplash = PhotoImage(file = "scifi_art.png")
       self.label = Label(self.frameSplash,image=self.photoSplash,bg = "black")
       self.label.grid(row = 0, column = 0)
       
       self.canevasSplash = Canvas(self.frameSplashTexte,width=1920,height=950)
       self.canevasSplash.grid(row = 0, column = 0)
       
       self.nomSplash = Entry(bg = "steelblue")
       self.nomSplash.insert(0, nom)
       self.ipSplash = Entry(bg = "steelblue")
       self.ipSplash.insert(0, ip)
       
       labip=Label(text=ip,bg="steelblue",borderwidth=0,relief=RIDGE)
       btncreerpartie=Button(text="Creer partie",bg="steelblue",command=self.creerpartie)
       btnconnecterpartie=Button(text="Connecter partie",bg="steelblue",command=self.connecterpartie)
       
       self.canevasSplash.create_window(1750,200,window=self.nomSplash,width=200,height=40)
       self.canevasSplash.create_window(1750,250,window=self.ipSplash,width=200,height=40)
       self.canevasSplash.create_window(1750,300,window=labip,width=200,height=40)
       self.canevasSplash.create_window(1750,350,window=btncreerpartie,width=200,height=40)
       self.canevasSplash.create_window(1750,400,window=btnconnecterpartie,width=200,height=40)
            
    def creercadrelobby(self):
        
        self.frameLobby=Frame(self.cadreapp, width = 1920, height = 950)
        self.frameLobbyTexte = Frame(self.frameLobby)
        
        self.frameLobby.grid(row = 0, column = 0, sticky = "nsew")
        self.frameLobbyTexte.grid(row = 0, column = 0, sticky = "nsew")
        
        self.photoSplash = PhotoImage(file = "scifi_art.png")
        self.label = Label(self.frameLobby,image=self.photoSplash,bg = "black")
        self.label.grid(row = 0, column = 0)
        
        self.canevaslobby=Canvas(self.frameLobbyTexte,width=1920,height=950)
        
        self.listelobby=Listbox(bg="steelblue", relief = "sunken", font=("Copperplate Gothic", 10, "bold"), bd = 1, highlightbackground= "steelblue")
        self.nbetoile=Entry(bg="steelblue", font=("Copperplate Gothic", 10))
        self.nbetoile.insert(0, 100)
        self.largeespace=Entry(bg="steelblue", font=("Copperplate Gothic", 10))
        self.largeespace.insert(0, 1000)
        self.hautespace=Entry(bg="steelblue", font=("Copperplate Gothic", 10))
        self.hautespace.insert(0, 800)
        
        self.case1 = Label(text = "Nombre d'étoile",bg = "steelblue", relief = "groove", font=("Copperplate Gothic", 10, "bold"))
        self.case2 = Label(text = "Largeur",bg = "steelblue", relief = "groove", font=("Copperplate Gothic", 10, "bold"))
        self.case3 = Label(text = "Hauteur",bg = "steelblue", relief = "groove", font=("Copperplate Gothic", 10, "bold"))
        self.configuration = Button(text = "Configuration", bg = "steelblue", relief = "raised", font=("Copperplate Gothic", 10, "bold"), command=self.lancerconfig)
        
        btnlancerpartie=Button(text="Lancer partie", font=("Copperplate Gothic", 15, "bold"),bg="steelblue",relief = "raised",command=self.lancerpartie)
        
        self.canevaslobby.create_window(1700,150, window=self.configuration, width =300, height =40)
        self.canevaslobby.create_window(1700,530,window=self.listelobby,width=300,height=400)
        self.canevaslobby.create_window(1700,800,window=btnlancerpartie,width=300,height=80)
        
    def connecterpartie(self):
        self.frameSplashTexte.grid_forget()
        self.canevaslobby.grid(row = 0,column = 0)
        nom=self.nomSplash.get()
        ip=self.ipSplash.get()
        if nom and ip:
            self.parent.inscrirejoueur()
            self.changecadre(self.frameLobby)
            print("BOUCLEATTENTE de CONNECTER")
            self.parent.boucleattente()
        
    def creerpartie(self):
        self.frameSplashTexte.grid_forget()
        self.canevaslobby.grid(row = 0,column = 0)
        nom=self.nomSplash.get()
        ip=self.ipSplash.get()
        if nom and ip:
            self.parent.creerpartie()
            self.parent.inscrirejoueur()
            self.changecadre(self.frameLobby)
            print("BOUCLEATTENTE de CREER")
            self.parent.boucleattente()
        
    def lancerpartie(self):
        self.parent.lancerpartie()
        
    def lancerconfig(self):
        self.canevaslobby.create_window(1600,200, window=self.case1,width = 100,height = 40)
        self.canevaslobby.create_window(1600,250, window=self.case2,width = 100,height = 40)
        self.canevaslobby.create_window(1600,300, window=self.case3,width = 100,height = 40)
        self.canevaslobby.create_window(1750,200,window=self.largeespace,width=200,height=40)
        self.canevaslobby.create_window(1750,250,window=self.hautespace,width=200,height=40)
        self.canevaslobby.create_window(1750,300,window=self.nbetoile,width=200,height=40)
        
    def affichelisteparticipants(self,lj):
        self.listelobby.delete(0,END)
        self.listelobby.insert(0,lj)
        
    def creeraffichercadrepartie(self,mod):
        self.nom=self.parent.monnom
        self.mod=mod
        # DEBUT AJOUT JCB !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        self.varNourriture=StringVar()
        self.varNourriture.set(str(self.mod.joueurs[self.parent.monnom].nourriture))
        self.varEnergie=StringVar()
        self.varEnergie.set(str(self.mod.joueurs[self.parent.monnom].energie))
        self.varArgent=StringVar()
        self.varArgent.set(str(self.mod.joueurs[self.parent.monnom].argent))
        self.varMateriaux=StringVar()
        self.varMateriaux.set(str(self.mod.joueurs[self.parent.monnom].materiaux))
        self.varMatiereNucleaire=StringVar()
        self.varMatiereNucleaire.set(str(self.mod.joueurs[self.parent.monnom].matiereNucleaire))
        self.varPopulation=StringVar()
        self.varPopulation.set(str(self.mod.joueurs[self.parent.monnom].population))
        self.varPopulationMax=StringVar()
        self.varPopulationMax.set(str(self.mod.joueurs[self.parent.monnom].populationMaximale))
#         self.varConnaissance=StringVar()
#         self.varConnaissance.set(str(self.mod.joueurs[self.parent.monnom].connaissance))
        # FIN AJOUT JCB !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        
        self.frameJeu=Frame(self.cadreapp)  
        self.frameRessource = Frame(self.frameJeu,bg='black', highlightbackground="deep sky blue", highlightthickness=2, width=1920,height = 50)
        self.frameAireJeu = Frame(self.frameJeu,bg='steelblue', width=1920,height = 500, highlightbackground="deep sky blue", highlightthickness=2)
        self.frameZoneUsager = Frame(self.frameJeu,bg='black', highlightbackground="deep sky blue", highlightthickness=2, width = 1920, height = 230 )
        self.frameMessage = Frame(self.frameZoneUsager,bg='steelblue', highlightbackground="deep sky blue", highlightthickness=2, width = 1090, height = 280)
        self.frameMenu = Frame(self.frameZoneUsager,bg='steelblue', highlightbackground="deep sky blue", highlightthickness=2, width = 500, height = 280)
        self.frameMap = Frame(self.frameZoneUsager,bg='steelblue', highlightbackground="deep sky blue", highlightthickness=2, width = 330, height = 280)
        
        self.frameJeu.grid(row = 0, sticky = "nsew")
        self.frameRessource.grid(column = 16 , sticky = "new", columnspan=16)
        self.frameAireJeu.grid(column = 16, sticky = "ew")
        self.frameZoneUsager.grid(column = 16, sticky = "nsew")
        self.frameMenu.grid(row = 0, column = 2, sticky = "nsew")
        self.frameMap.grid(row = 0, column = 0,  sticky = "nsew")
        self.frameMessage.grid(row = 0, column = 1,  sticky = "nsew")

        self.canevas=Canvas(self.frameAireJeu,width=mod.largeur,height=mod.hauteur,bg="grey11")  
        self.canevas.grid(row = 0, column = 0)                                                            
        self.canevas.bind("<Button>",self.cliquecosmos)
        self.labid=Label(self.frameMessage,text=self.nom,fg=mod.joueurs[self.nom].couleur)
        self.labid.bind("<Button>",self.afficherplanemetemere)                                  
        self.labid.grid(row = 0, column = 0 )                                                                                                                                    #.grid
        self.btncreervaisseau=Button( self.frameMenu,text="Vaisseau",
                                      command=self.creermineur, 
                                      relief=RAISED,
                                      bg = "deep sky blue",
                                      fg="black", 
                                      width=20, 
                                      activebackground='sky blue',
                                      font=("Castellar",10, "bold"))
        self.btncreerHangar=Button( self.frameMenu,text="Hangar",
                                      command=self.creerHangar, 
                                      relief=RAISED,
                                      bg = "deep sky blue",
                                      fg="black", 
                                      width=20, 
                                      activebackground='sky blue',
                                      font=("Castellar",10, "bold"))
        self.btncreerPod=Button( self.frameMenu,text="Pod",
                                      command=self.creerPod, 
                                      relief=RAISED,
                                      bg = "deep sky blue",
                                      fg="black", 
                                      width=20, 
                                      activebackground='sky blue',
                                      font=("Castellar",10, "bold"))
        self.btncreerMineArgent=Button( self.frameMenu,text="Gold Mine",
                                      command=self.creerMineArgent, 
                                      relief=RAISED,
                                      bg = "deep sky blue",
                                      fg="black", 
                                      width=20, 
                                      activebackground='sky blue',
                                      font=("Castellar",10, "bold"))
        self.btncreerMineMateriaux=Button( self.frameMenu,text="Steel Mine",
                                      command=self.creerMineMateriaux, 
                                      relief=RAISED,
                                      bg = "deep sky blue",
                                      fg="black", 
                                      width=20, 
                                      activebackground='sky blue',
                                      font=("Castellar",10, "bold"))
        self.btncreerMineEnergie=Button( self.frameMenu,text="Nuclear Mine",
                                      command=self.creerMineEnergie, 
                                      relief=RAISED,
                                      bg = "deep sky blue",
                                      fg="black", 
                                      width=20, 
                                      activebackground='sky blue',
                                      font=("Castellar",10, "bold"))
        
        self.lbselectecible=Label(self.frameMenu,text="Choisir cible",bg="darkgrey")
        
        #Creation des widgets dans le frame ressource
        
        self.boutonXchange = Button(    self.frameRessource, 
                                      relief=RAISED,
                                      bg = "deep sky blue", 
                                      text = "Xchange",
                                      fg="black", 
                                      width=20, 
                                      activebackground='sky blue',
                                      font=("Castellar",10, "bold"))
        
        self.Alerte = Label(self.frameRessource, 
                               text='Alerte', 
                               font = ("Castellar",10, "bold"),
                               bg = 'black', 
                               fg = "deep sky blue",
                               padx = 450)
       
        self.ressource = Label(self.frameRessource, 
                               text='Ressource :', 
                               font = ("Castellar",10, "bold"),
                               bg = 'black', 
                               fg = "deep sky blue",
                               padx = 10)
        
        #Matiere nucleaire
        self.nucleaire = Label(self.frameRessource, 
                               text='nuclear', 
                               font = ("Castellar",10, "bold"),
                               bg = 'black', 
                               fg = "deep sky blue",
                               padx = 20)
        
        self.nucleaireAmount = Label(self.frameRessource, 
                               text=self.varMatiereNucleaire.get(),
                               font = ("Castellar",10, "bold"),
                               bg = 'black', 
                               fg = "deep sky blue")
        #Food
        self.food = Label(self.frameRessource, 
                               text='Food', 
                               font = ("Castellar",10, "bold"),
                               bg = 'black', 
                               fg = "deep sky blue",
                               padx = 20)
        
        self.foodAmount = Label(self.frameRessource, 
                               text=self.varNourriture.get(), 
                               font = ("Castellar",10, "bold"),
                               bg = 'black', 
                               fg = "deep sky blue")
        #Energy
        self.energy = Label(self.frameRessource,
                               text='Energy:',  
                               font = ("Castellar",10, "bold"),
                               bg = 'black', 
                               fg = "deep sky blue",
                               padx = 20)
        
        self.energyAmount = Label(self.frameRessource, 
                               text=self.varEnergie.get(),  
                               font = ("Castellar",10, "bold"),
                               bg = 'black', 
                               fg = "deep sky blue")
        
        # DEBUT AJOUT JCB !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        
        #Argent
        self.argent = Label(self.frameRessource, 
                               text='Money', 
                               font = ("Castellar",10, "bold"),
                               bg = 'black', 
                               fg = "deep sky blue",
                               padx = 20)
         
        self.argentAmount = Label(self.frameRessource, 
                               text=self.varArgent.get(), 
                               font = ("Castellar",10, "bold"),
                               bg = 'black', 
                               fg = "deep sky blue")
        
        #Population
        self.population = Label(self.frameRessource, 
                               text='Population', 
                               font = ("Castellar",10, "bold"),
                               bg = 'black', 
                               fg = "deep sky blue",
                               padx = 20)
         
        self.populationAmount = Label(self.frameRessource, 
                               text=self.varPopulation.get() + " / " + self.varPopulationMax.get(), 
                               font = ("Castellar",10, "bold"),
                               bg = 'black', 
                               fg = "deep sky blue")
         
        #Materiaux
        self.materiaux = Label(self.frameRessource, 
                               text='Materials', 
                               font = ("Castellar",10, "bold"),
                               bg = 'black', 
                               fg = "deep sky blue",
                               padx = 20)
         
        self.materiauxAmount = Label(self.frameRessource, 
                               text=self.varMateriaux.get(), 
                               font = ("Castellar",10, "bold"),
                               bg = 'black', 
                               fg = "deep sky blue")

#         #Connaissance
#         self.connaissance = Label(self.frameRessource, 
#                                text='connaissance', 
#                                font = ("Castellar",10, "bold"),
#                                bg = 'black', 
#                                fg = "deep sky blue",
#                                padx = 20)
#          
#         self.connaissanceAmount = Label(self.frameRessource, 
#                                text=self.varConnaissance.get(), 
#                                font = ("Castellar",10, "bold"),
#                                bg = 'black', 
#                                fg = "deep sky blue")

        # FIN AJOUT JCB !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        
        #Creation des widgets dans le frame Zone Usager
        self.boutonTest1 = Button(    self.frameMenu, 
                                      relief=RAISED,
                                      bg = "deep sky blue", 
                                      text = "Test1",
                                      fg="black", 
                                      width=20, 
                                      activebackground='sky blue',
                                      font=("Castellar",10, "bold"))
        self.boutonTest2 = Button(    self.frameMenu, 
                                      relief=RAISED,
                                      bg = "deep sky blue", 
                                      text = "Test2",
                                      fg="black", 
                                      width=20, 
                                      activebackground='sky blue',
                                      font=("Castellar",10, "bold"))
        self.boutonTest3 = Button(    self.frameMenu, 
                                      relief=RAISED,
                                      bg = "deep sky blue", 
                                      text = "Test3",
                                      fg="black", 
                                      width=20, 
                                      activebackground='sky blue',
                                      font=("Castellar",10, "bold"))
        self.boutonTest4 = Button(    self.frameMenu, 
                                      relief=RAISED,
                                      bg = "deep sky blue", 
                                      text = "Test4",
                                      fg="black", 
                                      width=20, 
                                      activebackground='sky blue',
                                      font=("Castellar",10, "bold"))
        self.boutonTest5 = Button(    self.frameMenu, 
                                      relief=RAISED,
                                      bg = "deep sky blue", 
                                      text = "Test5",
                                      fg="black", 
                                      width=20, 
                                      activebackground='sky blue',
                                      font=("Castellar",10, "bold"))
        self.boutonTest6 = Button(    self.frameMenu, 
                                      relief=RAISED,
                                      bg = "deep sky blue", 
                                      text = "Test5",
                                      fg="black", 
                                      width=20, 
                                      activebackground='sky blue',
                                      font=("Castellar",10, "bold"))
        self.boutonTest7 = Button(    self.frameMenu, 
                                      relief=RAISED,
                                      bg = "deep sky blue", 
                                      text = "Test5",
                                      fg="black", 
                                      width=20, 
                                      activebackground='sky blue',
                                      font=("Castellar",10, "bold"))
        self.boutonTest8 = Button(    self.frameMenu, 
                                      relief=RAISED,
                                      bg = "deep sky blue", 
                                      text = "Test5",
                                      fg="black", 
                                      width=20, 
                                      activebackground='sky blue',
                                      font=("Castellar",10, "bold"))
        self.boutonTest9 = Button(    self.frameMenu, 
                                      relief=RAISED,
                                      bg = "deep sky blue", 
                                      text = "Test5",
                                      fg="black", 
                                      width=20, 
                                      activebackground='sky blue',
                                      font=("Castellar",10, "bold"))
        self.boutonTest10 = Button(    self.frameMenu, 
                                      relief=RAISED,
                                      bg = "deep sky blue", 
                                      text = "Test5",
                                      fg="black", 
                                      width=20, 
                                      activebackground='sky blue',
                                      font=("Castellar",10, "bold"))
        
        self.frameJeu.grid_rowconfigure(0, weight = 0)
        self.frameJeu.grid_columnconfigure(1, weight = 1)
        
        self.frameRessource.grid_rowconfigure(0, weight = 0)
        self.frameRessource.grid_columnconfigure(16, weight = 1)
        
        self.frameAireJeu.grid_rowconfigure(0, weight = 0)
        self.frameAireJeu.grid_columnconfigure(1, weight = 1)
        
        self.frameZoneUsager.grid_rowconfigure(0, weight = 0)
        self.frameZoneUsager.grid_columnconfigure(1, weight = 1)
        
        self.ressource.grid(row = 0, column =2)
        self.population.grid(row = 0, column = 3)
        self.populationAmount.grid(row = 0, column = 4)
        self.food.grid(row = 0, column = 5)
        self.foodAmount.grid(row = 0, column = 6)
        self.energy.grid(row = 0, column = 7)
        self.energyAmount.grid(row = 0, column = 8)
        self.argent.grid(row = 1, column = 3)
        self.argentAmount.grid(row = 1, column = 4)
        self.materiaux.grid(row = 1, column = 5)
        self.materiauxAmount.grid(row = 1, column = 6)
        self.nucleaire.grid(row = 1, column = 7)
        self.nucleaireAmount.grid(row = 1, column = 8)
        self.boutonXchange.grid(row = 0, column = 0)
        self.Alerte.grid(row = 0, column = 1)
        
        #self.btncreervaisseau.grid(row =0, column =0)
        #self.boutonTest2.grid(row = 1, column =0)
        #self.boutonTest3.grid(row = 2, column =0)
        #self.boutonTest4.grid(row = 3, column =0)
        #self.boutonTest5.grid(row = 4, column =0)
        #self.boutonTest6.grid(row = 5, column =0)
        #self.boutonTest7.grid(row = 6, column =0)
        #self.boutonTest8.grid(row = 7, column =0)
        #self.boutonTest9.grid(row = 8, column =0)
        #self.boutonTest10.grid(row = 9, column =0)
        
        self.afficherdecor(mod)
        
        self.changecadre(self.frameJeu)
        
    # AFFICHAGE INITIAL SEULEMENT
    def afficherdecor(self,mod):
        
        # afficher etoiles decoratives
        for i in range(len(mod.planetes)*3):
            x=random.randrange(mod.largeur)
            y=random.randrange(mod.hauteur)
            self.canevas.create_oval (x, y, x+1, y+1, fill = "white", tags = ("fond"))

        # afficher planetes vierges
        self.imgplanete = PhotoImage (file = "img_planeteVierge_02.png")
        for i in mod.planetes:
            self.canevas.create_image (
                i.x, i.y, image = self.imgplanete, tags = (i.proprietaire,"planete",str(i.id)))

        # afficher monstre        
        self.img_monstre = PhotoImage (file = "img_monstre_02.png")
        x = mod.monstre.x # hardcode pour l'instant
        y = mod.monstre.y # hardcode pour l'instant
        self.canevas.create_image (x, y, image = self.img_monstre)

        # afficher une planete infectee
        self.img_planeteInfectee = PhotoImage (file = "img_planeteInfectee_01.png")
        x = 220 # hardcode pour l'instant
        y = 60 # hardcode pour l'instant
        self.canevas.create_image (x, y, image = self.img_planeteInfectee)

        # afficher planetes joueurs
        self.img_planeteJoueur = PhotoImage (file = "img_planeteJoueur_02.png")
        for i in mod.joueurs.keys():
            for j in mod.joueurs[i].planetescontrolees:
                self.canevas.create_image (
                    j.x, j.y, image = self.img_planeteJoueur,
                    tags = (j.proprietaire,"planete", str(j.id), "possession"))
                
        self.afficherpartie(mod)
                
    def afficherplanemetemere(self,evt):
        j=self.mod.joueurs[self.nom]
        couleur=j.couleur
        x=j.planetemere.x
        y=j.planetemere.y
        t=10
        self.canevas.create_oval (
            x-t, y-t, x+t, y+t, dash=(3,3), width=2, outline=couleur,
            tags = ("planetemere","marqueur"))
        
    def creervaisseau(self):
        print("Creer vaisseau")
        self.parent.creervaisseau()
        self.maselection=None
        self.canevas.delete("marqueur")
        self.btncreervaisseau.pack_forget()
        
    # -----------------DM---------------------- #
    def creermineur(self):
        print("Creer mineur")
        self.parent.creermineur()
        self.maselection=None
        self.canevas.delete("marqueur")
        self.btncreervaisseau.pack_forget()     # À vérifier
        
    def creerexploreur(self):
        print("Creer exploreur")
        self.parent.creerexploreur()
        self.maselection=None
        self.canevas.delete("marqueur")
        self.btncreervaisseau.pack_forget()     # À vérifier
        
    def creerfregate(self):
        print("Creer fregate")
        self.parent.creerfregate()
        self.maselection=None
        self.canevas.delete("marqueur")
        self.btncreervaisseau.pack_forget()     # À vérifier
    # ------------------------------------------#
    
    # DEBUT Ajout JCB !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!    
    def creerPod(self):
        #print("Creer un Pod")
        self.parent.creerPod()
        #self.maselection=None
        self.canevas.delete("marqueur")
        #self.btncreerPod.pack_forget()
        
    def creerFerme(self):
        #print("Creer une Ferme")
        self.parent.creerFerme()
        #self.maselection=None
        self.canevas.delete("marqueur")
        #self.btncreerFerme.pack_forget()
        
    def creerMineArgent(self):
        #print("Creer une mine d'argent")
        self.parent.creerMineArgent()
        #self.maselection=None
        self.canevas.delete("marqueur")
        #self.btncreerMineArgent.pack_forget()
        
    def creerMineMateriaux(self):
        #print("Creer une mine de materiaux")
        self.parent.creerMineMateriaux()
        #self.maselection=None
        self.canevas.delete("marqueur")
        #self.btncreerMineMateriaux.pack_forget()
        
    def creerMineEnergie(self):
        #print("Creer une mine d'energie")
        self.parent.creerMineEnergie()
        #self.maselection=None
        self.canevas.delete("marqueur")
        #self.btncreerMineEnergie.pack_forget()
        
    def creerHangar(self):
        #print("Creer un hangar")
        self.parent.creerHangar()
        #self.maselection=None
        self.canevas.delete("marqueur")
        #self.btncreerHangar.pack_forget()
        
    def creerReacteurNucleaire(self):
        #print("Creer un reacteur nucleaire")
        self.parent.creerReacteurNucleaire()
        #self.maselection=None
        self.canevas.delete("marqueur")
        #self.btncreerReacteurNucleaire.pack_forget()
    # FIN Ajout JCB !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        
    def afficherpartie(self,mod):
        self.canevas.delete("artefact")
        
        # afficher progenitures du monstre
        if mod.monstre.listeProgenitures:
            self.img_progenitures = PhotoImage (file = "img_progenitures_02.png")
            for progeniture in mod.monstre.listeProgenitures:
                self.canevas.create_image (progeniture.x, progeniture.y, image = self.img_progenitures)

#                 x = progeniture.x
#                 y = progeniture.y
                #print(x, y)
        
        
        if self.maselection!=None:
            joueur=mod.joueurs[self.maselection[0]]
            if self.maselection[1]=="planete":
                for i in joueur.planetescontrolees:
                    if i.id == int(self.maselection[2]):
                        x=i.x
                        y=i.y
                        t = 40
                        self.canevas.create_oval (
                            x-t, y-t, x+t, y+t, dash = (2,2),
                            outline = mod.joueurs[self.nom].couleur,
                            tags=("select","marqueur"))
            elif self.maselection[1]=="flotte":
                for i in joueur.flotte:
                    if i.id == int(self.maselection[2]):
                        x=i.x
                        y=i.y
                        t = 60
                        self.canevas.create_rectangle (
                            x-t, y-t, x+t, y+t, dash = (2,2),
                            outline = mod.joueurs[self.nom].couleur,
                            tags=("select","marqueur"))
        
        for i in mod.joueurs.keys():
            i=mod.joueurs[i]
            for j in i.flotte:
                t = 40
                self.canevas.create_rectangle (
                    j.x-t, j.y-t, j.x+t, j.y+t, fill = i.couleur,
                    tags = (j.proprietaire,"flotte",str(j.id),"artefact"))
                
    # Mise à jour des variables d'affichage des statistiques du joueur    
    # DEBUT AJOUT JCB !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        self.varPopulation.set(str(self.mod.joueurs[self.parent.monnom].population))
        self.varPopulationMax.set(str(self.mod.joueurs[self.parent.monnom].populationMaximale))
        self.varNourriture.set(str(self.mod.joueurs[self.parent.monnom].nourriture))
        self.varArgent.set(str(self.mod.joueurs[self.parent.monnom].argent))
        self.varEnergie.set(str(self.mod.joueurs[self.parent.monnom].energie))                
        self.varMateriaux.set(str(self.mod.joueurs[self.parent.monnom].materiaux))
        self.varMatiereNucleaire.set(str(self.mod.joueurs[self.parent.monnom].matiereNucleaire))
        #self.varConnaissance.set(str(self.mod.joueurs[self.parent.monnom].connaissance))
    # FIN AJOUT JCB !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    def cliquecosmos(self,evt):
        self.btncreervaisseau.pack_forget()
        self.btncreerHangar.pack_forget()
        self.btncreerPod.pack_forget()
        self.btncreerMineArgent.pack_forget()
        self.btncreerMineMateriaux.pack_forget()
        self.btncreerMineEnergie.pack_forget()
        t=self.canevas.gettags(CURRENT)
        if t and t[0]==self.nom:
            #self.maselection=self.canevas.find_withtag(CURRENT)#[0]
            self.maselection=[self.nom,t[1],t[2]]  #self.canevas.find_withtag(CURRENT)#[0]
            print(self.maselection)
            if t[1] == "planete":
                self.montreplaneteselection()
            elif t[1] == "flotte":
                self.montreflotteselection()
        elif "planete" in t and t[0]!=self.nom:
            if self.maselection:
                pass # attribuer cette planete a la cible de la flotte selectionne
                self.parent.ciblerflotte(self.maselection[2],t[2])
            print("Cette planete ne vous appartient pas - elle est a ",t[0])
            self.maselection=None
            self.lbselectecible.pack_forget()
            self.canevas.delete("marqueur")
        else:
            print("Region inconnue")
            self.maselection=None
            self.lbselectecible.pack_forget()
            self.canevas.delete("marqueur")
            
    def montreplaneteselection(self):
        self.btncreervaisseau.pack()
        self.btncreerHangar.pack()
        self.btncreerPod.pack()
        self.btncreerMineArgent.pack()
        self.btncreerMineMateriaux.pack()
        self.btncreerMineEnergie.pack()
    def montreflotteselection(self):
        self.lbselectecible.pack()
    
    def afficherartefacts(self,joueurs):
        pass #print("ARTEFACTS de ",self.nom)
    
    
    