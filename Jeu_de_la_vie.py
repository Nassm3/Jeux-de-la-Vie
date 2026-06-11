#!/usr/bin/python3

import random
import tkinter as tk
from tkinter import ttk

class controleur:
    def __init__(self,interface,grille):
        self.interface = interface
        self.grille = grille
        self.en_cour = False
        self.compteur = 0
        self.speed = 125
        self.interface.bouton_start.config(command = self.clicstart)
        self.interface.speedbox.bind("<<ComboboxSelected>>", self.selectspeed)
        self.interface.combobox.bind("<<ComboboxSelected>>", self.select)
        self.interface.bouton_clean.config(command = self.clean)

    def simulation(self):
        if not self.en_cour:
            print("Simulation terminée")
        else:
#            self.interface.canvas.unbind("<ButtonRelease-1>")
            changement = self.grille.maj()
            self.interface.maj(self.grille.grid)
            if changement and self.en_cour:
                self.compteur += 1
                self.interface.nb_gen.set(str(self.compteur))
                self.interface.master.after(self.speed, self.simulation)
            else:
                print("Simulation terminée")

    def clicstart(self):
        if self.interface.etat_jeu.get() == "Start":
            self.interface.etat_jeu.set("Stop")
            self.en_cour = True
            self.simulation()
        elif self.interface.etat_jeu.get() == "Stop":
            self.interface.etat_jeu.set("Start")
            self.en_cour = False
            self.simulation()

    def selectspeed(self,event):
        widget=event.widget
        selection =  widget.get()
        match selection:
            case "Lent":
                self.speed = 125
            case "Normal":
                self.speed = 62
            case "Rapide":
                self.speed = 31
            case "Très Rapide":
                self.speed = 16

    def select(self,event):
        widget = event.widget
        selection = widget.get()
        self.interface.canvas.unbind("<Button-1>")
        self.interface.canvas.unbind("<Motion>")
        match selection:
            case "Aléatoire":
                self.grille.initialisation_random()

            case "Manuel":
                self.grille.initialisation_user()
                self.interface.canvas.bind("<Button-1>",self.cliccell)

            case motif if motif in self.grille.dico_motif.keys():
                self.interface.motif = self.grille.dico_motif[motif]
                self.interface.canvas.bind("<Motion>", lambda event:self.interface.fantome_motif(event,self.grille.grid))
                self.interface.canvas.bind("<Button-1>", self.place_motif)
        self.compteur = 0
        self.interface.nb_gen.set("0")
        self.interface.maj(self.grille.grid)

    def cliccell(self,event):
        col = int((event.x - self.interface.x_decalage) // self.interface.taille_cell)
        li = int((event.y - self.interface.y_decalage) // self.interface.taille_cell)
        if 0 <= li < self.grille.nb and 0 <= col < self.grille.nb:
            if self.grille.grid[li][col] > 0:
                self.grille.grid[li][col] = 0
            elif self.grille.grid[li][col] == 0:
                self.grille.grid[li][col] = 1
        self.interface.maj(self.grille.grid)

    def place_motif(self,event):
        col = int((event.x - self.interface.x_decalage) // self.interface.taille_cell)
        li = int((event.y - self.interface.y_decalage) // self.interface.taille_cell)
        if 0 <= li < self.grille.nb and 0 <= col < self.grille.nb:
            self.interface.fantome=[]
            self.grille.initialisation_motif(self.interface.motif,li,col)
            self.interface.maj(self.grille.grid)

    def clean(self):
        self.grille.initialisation_user()
        self.interface.maj(self.grille.grid)

class Interface:
    def __init__(self,master,nb_cell):
        self.nb_cell = nb_cell
        self.x_decalage = 0
        self.y_decalage = 0
        self.master = master
        self.jeu = tk.Frame(self.master)
        self.menu = tk.Frame(self.master,bg="lightgrey", padx=20, pady=20)
        self.initialisation = tk.StringVar()
        self.etat_jeu = tk.StringVar(value="Start")
        self.bouton_start = tk.Button(self.menu, textvariable=self.etat_jeu)
        self.vitesse = tk.StringVar()
        self.speed_frame = tk.Frame(self.menu, bg="lightgrey", padx=20, pady=20)
        self.speedbox = ttk.Combobox(self.speed_frame, textvariable=self.vitesse)
        self.taille_cell = 10
        self.taille_canvas = self.nb_cell * self.taille_cell
        self.canvas = tk.Canvas(self.jeu, width=self.taille_canvas, height=self.taille_canvas, highlightthickness=0)
        self.combobox = ttk.Combobox(self.menu, textvariable=self.initialisation)
        self.last_x = 0
        self.last_y = 0
        self.nb_gen = tk.StringVar()
        self.ligne = 'Black'
        self.bouton_clean = tk.Button(self.menu, text="Clean")
        self.motif=[]
        self.fantome=[]
        self.couleur = {0:'white',1:'lawn green',2:'spring green',3:'light sea green',4:'DeepSkyBlue3',5:'DeepSkyBlue4',6:'SteelBlue4',7:'DodgerBlue4',8:'blue4'}
        self.create_Interface()

    def create_Interface(self):

        self.jeu.grid(row=0, column=0, sticky="nsew")
        self.menu.grid(row=0, column=1, sticky="nsew")

        tk.Label(self.menu, text="Configuration:").pack(pady=1)

        self.combobox['values'] = ('Aléatoire', 'Manuel','Planeur','Canon','Vaisseau','Papillon')
        self.combobox['state'] = 'readonly'
        self.combobox.pack(padx=5, pady=5)
        self.combobox.current(0)

        gen_frame = tk.Frame(self.menu, bg="lightgrey", padx=20, pady=20)
        gen_frame.pack()
        tk.Label(gen_frame, text="Génération :").grid(row=0, column=0)
        tk.Label(gen_frame, textvariable=self.nb_gen).grid(row=0, column=1)

        self.speed_frame.pack()
        tk.Label(self.speed_frame, text="Vitesse:").grid(row=0, column=0)

        self.speedbox['values'] = ('Lent','Normal','Rapide', 'Très Rapide')
        self.speedbox['state'] = 'readonly'
        self.speedbox.set('Normal')

        self.speedbox.grid(row=0, column=1)
        self.showgri = tk.IntVar()
        tk.Checkbutton(self.menu, text="Afficher la Grille", variable=self.showgri,
                             onvalue=1, offvalue=0, command=self.affichage_grille).pack(side="left")
        self.showgri.set(1)

        self.bouton_clean.pack(side="bottom",pady=50)

        self.bouton_start.pack(side="bottom")

        self.canvas.pack(expand=True, fill="both")
        self.rectangles = [[None for _ in range(self.nb_cell)] for _ in range(self.nb_cell)]

        for li in range(self.nb_cell):
            for col in range(self.nb_cell):
                x1 = col * self.taille_cell
                y1 = li * self.taille_cell
                x2 = x1 + self.taille_cell
                y2 = y1 + self.taille_cell

                cell = self.canvas.create_rectangle(x1,y1,x2,y2,fill='white')
                self.rectangles[li][col] = cell

        self.canvas.bind("<MouseWheel>", self.molette_zoom)
        self.canvas.bind("<ButtonPress-3>", self.clic_droit)
        self.canvas.bind("<B3-Motion>", self.deplacer)

    def fantome_motif(self,event,grille):
        for x_fant,y_fant in self.fantome:
            if grille[x_fant][y_fant] == 0:
                motif_fantome = self.rectangles[x_fant][y_fant]
                self.canvas.itemconfig(motif_fantome, fill='White')
        col = int((event.x - self.x_decalage) // self.taille_cell)
        li = int((event.y - self.y_decalage) // self.taille_cell)
        x, y = zip(*self.motif)
        centre_x = int((max(x) + min(x)) / 2)
        centre_y = int((max(y) + min(y)) / 2)
        if centre_x <= li < ((self.nb_cell-max(x))+centre_x) and centre_y <= col < ((self.nb_cell-max(y))+centre_y):
            for dli,dcol in self.motif:
                dcol = int(dcol + col - centre_y)
                dli = int(dli + li - centre_x)
                self.fantome.append([dli,dcol])
                if grille[dli][dcol] == 0:
                    cell_fantome = self.rectangles[dli][dcol]
                    self.canvas.itemconfig(cell_fantome, fill='SkyBlue3')

    def molette_zoom(self,event):
        if event.delta > 0 and self.taille_cell < 50:
            self.taille_cell=self.taille_cell+5
        elif event.delta < 0 and self.taille_cell > 10:
            self.taille_cell=self.taille_cell-5
        self.maj_rectangles()

    def clic_droit(self,event):
        self.last_x = event.x
        self.last_y = event.y

    def maj_rectangles(self):
        for li in range(self.nb_cell):
            for col in range(self.nb_cell):
                x1 = col * self.taille_cell + self.x_decalage
                y1 = li * self.taille_cell + self.y_decalage
                x2 = x1 + self.taille_cell
                y2 = y1 + self.taille_cell
                id = self.rectangles[li][col]
                self.canvas.coords(id, x1, y1, x2, y2)

    def deplacer(self, event):
        self.x_decalage += event.x - self.last_x
        self.y_decalage += event.y - self.last_y
        self.last_x = event.x
        self.last_y = event.y
        self.maj_rectangles()

    def affichage_grille(self):
        if self.showgri.get() == 1:
            self.ligne = 'Black'
        else:
            self.ligne = 'White'
        for li in range(self.nb_cell):
            for col in range(self.nb_cell):
                cell = self.rectangles[li][col]
                self.canvas.itemconfig(cell,outline=self.ligne)

    def maj(self,grille):
        for li in range(self.nb_cell):
            for col in range(self.nb_cell):
                generation = grille[li][col]
                color = self.couleur[generation] if generation < 9 else 'blue4'
                cell = self.rectangles[li][col]
                self.canvas.itemconfig(cell,fill=color)

class Grille:
    def __init__(self, nb): #nb = nombre de lignes/colonnes
        self.nb = nb
        self.grid = [[0 for _ in range(self.nb)] for _ in range(self.nb)]
        self.dico_motif = {
            'Planeur':[(0,1),(1,2),(2,0),(2,1),(2,2)],
            'Canon':[(0,24),(1,22),(1,24),(2,20),(2,21),(2,12),(2,13),(2,34),(2,35),(3,11),(3,15),(3,20),(3,21),(3,34),(3,35),(4,0),(4,1),(4,10),(4,16),(4,20),(4,21),(5,0),(5,1),(5,10),(5,14),(5,16),(5,17),(5,22),(5,24),(6,10),(6,16),(6,24),(7,11),(7,15),(8,12),(8,13)],
            'Vaisseau':[(0,1),(0,2),(0,3),(0,4),(0,5),(0,6),(1,0),(1,6),(2,6),(3,0),(3,5),(4,2),(4,3)],
            'Papillon':[(0,4),(0,5),(0,6),(0,7),(1,3),(1,4),(1,5),(1,6),(1,7),(1,8),(2,2),(2,3),(2,5),(2,6),(2,7),(2,8),(3,3),(3,4),(5,11),(5,12),(6,1),(6,14),(7,0),(8,0),(8,14),(9,0),(9,1),(9,2),(9,3),(9,4),(9,5),(9,6),(9,7),(9,8),(9,9),(9,10),(9,11),(9,12),(9,13),(12,4),(12,5),(12,6),(12,7),(13,3),(13,4),(13,5),(13,6),(13,7),(13,8),(14,2),(14,3),(14,5),(14,6),(14,7),(14,8),(15,3),(15,4)]
        }

    def initialisation_random(self):
        for li in range(self.nb):
            for col in range(self.nb):
                self.grid[li][col] = random.choice([0,1])

    def initialisation_user(self):
       self.grid = [[0 for _ in range(self.nb)] for _ in range(self.nb)]

    def initialisation_motif(self,motif,pos_li,pos_col):
        x, y = zip(*motif)
        centre_x = int((max(x) + min(x)) / 2)
        centre_y = int((max(y) + min(y)) / 2)
        for li,col in motif:
            col = int(col + pos_col - centre_y)
            li = int(li + pos_li - centre_x)
            self.grid[li][col] = 1

    def compter_voisins_vivants(self,li,col):
        compteur=0
        direction = [(1, -1), (1, 0), (1, 1), (0, -1),(-1,-1),(-1,0),(-1,1),(0,1)]
        for x,y in direction: # x = ligne et y = colonne
            x_voisin = li + x
            y_voisin = col + y
            if self.nb > x_voisin >= 0 and self.nb > y_voisin >= 0 and self.grid[x_voisin][y_voisin] != 0:
                compteur += 1
        return(compteur)

    def maj(self):
        etat_suivant = [[0 for _ in range(self.nb)] for _ in range(self.nb)]
        changement = False
        for li in range(self.nb):
            for col in range(self.nb):
                nb_voisin = self.compter_voisins_vivants(li,col)
                if nb_voisin == 3 and self.grid[li][col] == 0:
                    etat_suivant[li][col] = 1
                    changement = True
                elif (nb_voisin == 3 or nb_voisin == 2) and self.grid[li][col] > 0:
                    etat_suivant[li][col] = self.grid[li][col] + 1
                elif (2 > nb_voisin or nb_voisin > 3) and self.grid[li][col] > 0:
                    etat_suivant[li][col] = 0
                    changement = True
        self.grid = etat_suivant
        return changement # true si changement


if __name__ == '__main__':
    g = Grille(60)
    fenetre = tk.Tk()
    fenetre.grid_rowconfigure(0, weight=1)
    fenetre.grid_columnconfigure(1, weight=1)
    inter = Interface(fenetre,g.nb)
    jeux = controleur(inter,g)
    fenetre.mainloop()
