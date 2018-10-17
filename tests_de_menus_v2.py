
from tkinter import *

frame = Tk()

frame.config(bg = "steelblue")
frame.geometry("300x350")
frame.grid_columnconfigure(0, weight = 5)

saut_de_ligne_x1 = "\n"

#---------------------------------------
def afficher_menu_ma_planete():

    vider_le_cadre()

    label_du_menu_ma_planete.grid(column = 3, row =0)
    bouton_afficher_menu_pr_batir_une_amelioration.grid(column = 3, row =1)
    bouton_afficher_menu_pr_batir_un_vaisseau.grid(column = 3, row =2)

#---------------------------------------
def afficher_menu_pr_batir_une_amelioration():

    vider_le_cadre()

    label_du_menu_pr_batir_une_amelioration.grid(column = 3, row =0)
    bouton_hangar.grid(column = 3, row =1)
    bouton_ferme.grid(column = 3, row =2)
    bouton_pod.grid(column = 3, row =3)
    bouton_afficher_menu_pr_batir_une_mine.grid(column = 3, row =4)

    label_saut_de_ligne.grid(column = 3, row =6)
    bouton_retour_au_menu_ma_planete.grid(column = 3, row =7)
 
#---------------------------------------
def afficher_menu_pr_batir_une_mine():

    vider_le_cadre()

    label_du_menu_pr_batir_une_mine.grid(column = 3, row =0)
    bouton_mine_argent.grid(column = 3, row =1)
    bouton_mine_materiau.grid(column = 3, row =2)
    bouton_mine_energie.grid(column = 3, row =3)

    label_saut_de_ligne.grid(column = 3, row =4)
    bouton_retour_au_menu_pr_batir_une_amelioration.grid(column = 3, row =6)
    bouton_retour_au_menu_ma_planete.grid(column = 3, row =7)

#---------------------------------------
def afficher_menu_pr_batir_un_vaisseau():

    vider_le_cadre()

    label_du_menu_pr_batir_un_vaisseau.grid(column = 3, row =0)
    bouton_exploreur.grid(column = 3, row =1)
    bouton_mineur.grid(column = 3, row =2)
    bouton_fregate.grid(column = 3, row =3)
    #bouton_bombarde.grid(column = 0, row =0)
    bouton_chasseur.grid(column = 3, row =4)
    #bouton_dreadnought.grid(column = 0, row =0)
    #bouton_destructeur.grid(column = 0, row =0)

    label_saut_de_ligne.grid(column = 3, row =5)
    bouton_retour_au_menu_ma_planete.grid(column = 3, row =6)
 
#---------------------------------------
def vider_le_cadre():

    label_du_menu_ma_planete.grid_forget()
    label_du_menu_pr_batir_une_amelioration.grid_forget()
    label_du_menu_pr_batir_une_mine.grid_forget()
    label_du_menu_pr_batir_un_vaisseau.grid_forget()
    label_saut_de_ligne.grid_forget()
    
    bouton_retour_au_menu_ma_planete.grid_forget()
    bouton_retour_au_menu_pr_batir_une_amelioration.grid_forget()

    bouton_afficher_menu_pr_batir_une_amelioration.grid_forget()
    bouton_hangar.grid_forget()
    bouton_ferme.grid_forget()
    bouton_pod.grid_forget()

    bouton_afficher_menu_pr_batir_une_mine.grid_forget()
    bouton_mine_argent.grid_forget()
    bouton_mine_materiau.grid_forget()
    bouton_mine_energie.grid_forget()

    bouton_afficher_menu_pr_batir_un_vaisseau.grid_forget()
    bouton_exploreur.grid_forget()
    bouton_mineur.grid_forget()
    bouton_fregate.grid_forget()
    #bouton_bombarde.grid_forget()
    bouton_chasseur.grid_forget()
    #bouton_dreadnought.grid_forget()
    #bouton_destructeur.grid_forget()

#---------------------------------------
# Controle de la mise en page
#---------------------------------------
label_du_menu_ma_planete = Label (
    frame,
    text = saut_de_ligne_x1 + "Menu de ma planete" + saut_de_ligne_x1,
    font = ("Copperplate Gothic", 12, "bold"),
    bg = "steelblue",
    fg = "white",
    relief = "flat",
    width = 30)

#---------------------------------------
label_du_menu_pr_batir_une_amelioration = Label (
    frame,
    text = saut_de_ligne_x1 + "Menu pour batir une amelioration" + saut_de_ligne_x1,
    font = ("Copperplate Gothic", 12, "bold"),
    bg = "steelblue",
    fg = "white",
    relief = "flat",
    width = 30)

#---------------------------------------
label_du_menu_pr_batir_une_mine = Label (
    frame,
    text = saut_de_ligne_x1 + "Menu pour batir une mine" + saut_de_ligne_x1,
    font = ("Copperplate Gothic", 12, "bold"),
    bg = "steelblue",
    fg = "white",
    relief = "flat",
    width = 30)

#---------------------------------------
label_du_menu_pr_batir_un_vaisseau = Label (
    frame,
    text = saut_de_ligne_x1 + "Menu pour batir un vaisseau" + saut_de_ligne_x1,
    font = ("Copperplate Gothic", 12, "bold"),
    bg = "steelblue",
    fg = "white",
    relief = "flat",
    width = 30)

#---------------------------------------
label_saut_de_ligne = Label (
    frame,
    text = saut_de_ligne_x1,
    bg = "steelblue")

#---------------------------------------
# Menu de ma planete
#---------------------------------------
bouton_afficher_menu_pr_batir_une_amelioration = Button (
    frame,
    text = "Batir une amelioration",
    font = ("Copperplate Gothic", 12, "bold"),
    bg = "steelblue",
    fg = "white",
    relief = "raised",
    width = 20,
    command = afficher_menu_pr_batir_une_amelioration)

#---------------------------------------
bouton_afficher_menu_pr_batir_un_vaisseau = Button (
    frame,
    text = "Batir un vaisseau",
    font = ("Copperplate Gothic", 12, "bold"),
    bg = "steelblue",
    fg = "white",
    relief = "raised",
    width = 20,
    command = afficher_menu_pr_batir_un_vaisseau)

#---------------------------------------
# Menu pour batir des ameliorations
#---------------------------------------
bouton_hangar = Button (
    frame,
    text = "Batir un hangar",
    font = ("Copperplate Gothic", 12, "bold"),
    bg = "steelblue",
    fg = "white",
    relief = "raised",
    width = 20,
    command = None)

#---------------------------------------
bouton_ferme = Button (
    frame,
    text = "Batir une ferme",
    font = ("Copperplate Gothic", 12, "bold"),
    bg = "steelblue",
    fg = "white",
    relief = "raised",
    width = 20,
    command = None)

#---------------------------------------
bouton_pod = Button (
    frame,
    text = "Batir un pod",
    font = ("Copperplate Gothic", 12, "bold"),
    bg = "steelblue",
    fg = "white",
    relief = "raised",
    width = 20,
    command = None)

#---------------------------------------
bouton_afficher_menu_pr_batir_une_mine = Button (
    frame,
    text = "Batir une mine",
    font = ("Copperplate Gothic", 12, "bold"),
    bg = "steelblue",
    fg = "white",
    relief = "raised",
    width = 20,
    command = afficher_menu_pr_batir_une_mine)

#---------------------------------------
# Menu pour batir une mine
#---------------------------------------
bouton_mine_argent = Button (
    frame,
    text = "Batir une mine d'argent",
    font = ("Copperplate Gothic", 12, "bold"),
    bg = "steelblue",
    fg = "white",
    relief = "raised",
    width = 20,
    command = None)

#---------------------------------------
bouton_mine_materiau = Button (
    frame,
    text = "Batir une mine de materiau",
    font = ("Copperplate Gothic", 12, "bold"),
    bg = "steelblue",
    fg = "white",
    relief = "raised",
    width = 20,
    command = None)

#---------------------------------------
bouton_mine_energie = Button (
    frame,
    text = "Batir une mine d'energie",
    font = ("Copperplate Gothic", 12, "bold"),
    bg = "steelblue",
    fg = "white",
    relief = "raised",
    width = 20,
    command = None)

#---------------------------------------
# Menu pour batir un vaisseau
#---------------------------------------
bouton_exploreur = Button (
    frame,
    text = "Batir un exploreur",
    font = ("Copperplate Gothic", 12, "bold"),
    bg = "steelblue",
    fg = "white",
    relief = "raised",
    width = 20,
    command = None)

#---------------------------------------
bouton_mineur = Button (
    frame,
    text = "Batir un mineur",
    font = ("Copperplate Gothic", 12, "bold"),
    bg = "steelblue",
    fg = "white",
    relief = "raised",
    width = 20,
    command = None)

#---------------------------------------
bouton_fregate = Button (
    frame,
    text = "Batir une fregate",
    font = ("Copperplate Gothic", 12, "bold"),
    bg = "steelblue",
    fg = "white",
    relief = "raised",
    width = 20,
    command = None)

#---------------------------------------
'''bouton_bombarde = Button (
    frame,
    text = "Batir une bombarde",
    font = ("Copperplate Gothic", 12, "bold"),
    bg = "steelblue",
    fg = "white",
    relief = "raised",
    width = 20,
    command = None)
'''
#---------------------------------------
bouton_chasseur = Button (
    frame,
    text = "Batir un chasseur",
    font = ("Copperplate Gothic", 12, "bold"),
    bg = "steelblue",
    fg = "white",
    relief = "raised",
    width = 20,
    command = None)

#---------------------------------------
'''bouton_dreadnought = Button (
    frame,
    text = "Batir un dreadnought",
    font = ("Copperplate Gothic", 12, "bold"),
    bg = "steelblue",
    fg = "white",
    relief = "raised",
    width = 20,
    command = None)
'''
#---------------------------------------
'''bouton_destructeur = Button (
    frame,
    text = "Batir un destructeur",
    font = ("Copperplate Gothic", 12, "bold"),
    bg = "steelblue",
    fg = "white",
    relief = "raised",
    width = 20,
    command = None)
'''
#---------------------------------------
# Boutons de style "menu precedent"
#---------------------------------------
bouton_retour_au_menu_ma_planete = Button (
    frame,
    text = " -> Menu initial   ",
    font = ("Copperplate Gothic", 12, "bold"),
    bg = "steelblue",
    fg = "white",
    relief = "raised",
    width = 20,
    command = afficher_menu_ma_planete)

#---------------------------------------
bouton_retour_au_menu_pr_batir_une_amelioration = Button (
    frame,
    text = " -> Menu des ameliorations   ",
    font = ("Copperplate Gothic", 12, "bold"),
    bg = "steelblue",
    fg = "white",
    relief = "raised",
    width = 20,
    command = afficher_menu_pr_batir_une_amelioration)
 
#---------------------------------------



#---------------------------------------
# Lancement du menu principal
#---------------------------------------
afficher_menu_ma_planete()

frame.mainloop()


