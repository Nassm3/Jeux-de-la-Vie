#!/usr/bin/python3

import random
import tkinter as tk
from idlelib.query import Query
from tkinter import ttk, IntVar


class Interface:
    def __init__(self,grille,master):
        self.x_decalage = 0
        self.y_decalage = 0
        self.grille = grille
        self.master = master
        self.en_cour = False
        self.taille_cell = 10
        self.compteur = 0
        self.speed = 125
        self.last_x = 0
        self.last_y = 0
        self.ligne = 'Black'
        self.dico_motif = {
            'Planeur':[(0,1),(1,2),(2,0),(2,1),(2,2)],
            'Canon':[(0,24),(1,22),(1,24),(2,20),(2,21),(2,12),(2,13),(2,34),(2,35),(3,11),(3,15),(3,20),(3,21),(3,34),(3,35),(4,0),(4,1),(4,10),(4,16),(4,20),(4,21),(5,0),(5,1),(5,10),(5,14),(5,16),(5,17),(5,22),(5,24),(6,10),(6,16),(6,24),(7,11),(7,15),(8,12),(8,13)]
        }
        self.couleur = {0:'white',1:'lawn green',2:'spring green',3:'light sea green',4:'DeepSkyBlue3',5:'DeepSkyBlue4',6:'SteelBlue4',7:'DodgerBlue4',8:'blue4'}
        self.afficher()


    def clicstart(self,etat_jeu):
        if etat_jeu.get() == "Start":
            etat_jeu.set("Stop")
            self.en_cour = True
            self.simulation()
        elif etat_jeu.get() == "Stop":
            etat_jeu.set("Start")
            self.en_cour = False
            self.simulation()

    def cliccell(self,event):
        col = int((event.x - self.x_decalage) // self.taille_cell)
        li = int((event.y - self.y_decalage) // self.taille_cell)
        if 0 <= li < self.grille.nb and 0 <= col < self.grille.nb:
            if self.grille.grid[li][col] > 0:
                self.grille.grid[li][col] = 0
            elif self.grille.grid[li][col] == 0:
                self.grille.grid[li][col] = 1
        self.maj()

    def select(self,event):
        widget = event.widget
        selection = widget.get()
        self.canvas.unbind("<Button-1>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas.unbind("<Motion>")
        match selection:
            case "Aléatoire":
                self.compteur = 0
                self.g.set("0")
                self.grille.initialisation_random()
                self.canvas.unbind("<Button-1>")

            case "Manuel":
                self.grille.initialisation_user()
                self.canvas.bind("<Button-1>",self.cliccell)

            case motif if motif in self.dico_motif.keys():
                self.motif = self.dico_motif[motif]
                self.canvas.bind("<Motion>", self.fantome_motif)
                self.canvas.bind("<ButtonRelease-1>", self.place_motif)
        self.compteur = 0
        self.g.set("0")
        self.maj()

    def fantome_motif(self,event):
        self.maj()
        col = int((event.x - self.x_decalage) // self.taille_cell)
        li = int((event.y - self.y_decalage) // self.taille_cell)
        x, y = zip(*self.motif)
        centre_x = int((max(x) + min(x)) / 2)
        centre_y = int((max(y) + min(y)) / 2)
        if centre_x <= li < ((self.grille.nb-max(x))+centre_x) and centre_y <= col < ((self.grille.nb-max(y))+centre_y):
            for dli,dcol in self.motif:
                dcol = int(dcol + col - centre_y)
                dli = int(dli + li - centre_x)
                cell_fantome = self.rectangles[dli][dcol]
                self.canvas.itemconfig(cell_fantome, fill='SkyBlue3')

    def selectspeed(self,event):
        widget = event.widget
        selection = widget.get()
        match selection:
            case "Lent":
                self.speed = 125
            case "Normal":
                self.speed = 62
            case "Rapide":
                self.speed = 31
            case "Très Rapide":
                self.speed = 16

    def place_motif(self,event):
        col = int((event.x - self.x_decalage) // self.taille_cell)
        li = int((event.y - self.y_decalage) // self.taille_cell)
        if 0 <= li < self.grille.nb and 0 <= col < self.grille.nb:
            self.grille.initialisation_motif(self.motif, li,col)
            self.maj()

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
        for li in range(self.grille.nb):
            for col in range(self.grille.nb):
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

    def clean(self):
        self.grille.initialisation_user()
        self.maj()

    def afficher(self):
        jeu = tk.Frame(self.master)
        menu = tk.Frame(self.master,bg="lightgrey", padx=20, pady=20)

        jeu.grid(row=0, column=0, sticky="nsew")
        menu.grid(row=0, column=1, sticky="nsew")

        tk.Label(menu, text="Configuration:").pack(pady=1)

        initialisation = tk.StringVar()
        self.combobox = ttk.Combobox(menu, textvariable=initialisation)
        self.combobox['values'] = ('Aléatoire', 'Manuel','Planeur','Canon')

        self.combobox['state'] = 'readonly'
        self.combobox.pack(padx=5, pady=5)
        self.combobox.current(0)
        self.combobox.bind("<<ComboboxSelected>>", self.select)


        gen_frame = tk.Frame(menu, bg="lightgrey", padx=20, pady=20)
        gen_frame.pack()
        gen = tk.Label(gen_frame, text="Génération :")
        self.g = tk.StringVar()
        show_gen = tk.Label(gen_frame, textvariable=self.g)
        self.g.set(str(self.compteur))

        gen.grid(row=0, column=0)
        show_gen.grid(row=0, column=1)

        speed_frame = tk.Frame(menu, bg="lightgrey", padx=20, pady=20)
        speed_frame.pack()
        vitesse_label = tk.Label(speed_frame, text="Vitesse:")

        vitesse = tk.StringVar()
        speedbox = ttk.Combobox(speed_frame, textvariable=vitesse)
        speedbox['values'] = ('Lent','Normal','Rapide', 'Très Rapide')
        speedbox['state'] = 'readonly'
        speedbox.set('x1')
        speedbox.bind("<<ComboboxSelected>>", self.selectspeed)

        vitesse_label.grid(row=0, column=0)
        speedbox.grid(row=0, column=1)
        self.showgri = tk.IntVar()
        tk.Checkbutton(menu, text="Afficher la Grille", variable=self.showgri,
                             onvalue=1, offvalue=0, command=self.affichage_grille).pack(side="left")
        self.showgri.set(1)

        tk.Button(menu, text="Clean", command= self.clean).pack(side="bottom",pady=50)

        etat_jeu = tk.StringVar(value="Start")
        tk.Button(menu, textvariable=etat_jeu, command=lambda:self.clicstart(etat_jeu)).pack(side="bottom")

        taille_canvas = self.grille.nb * self.taille_cell
        self.canvas = tk.Canvas(jeu, width=taille_canvas, height=taille_canvas, highlightthickness=0)
        self.canvas.pack(expand=True, fill="both")
        self.rectangles = [[None for _ in range(self.grille.nb)] for _ in range(self.grille.nb)]

        for li in range(self.grille.nb):
            for col in range(self.grille.nb):
                x1 = col * self.taille_cell
                y1 = li * self.taille_cell
                x2 = x1 + self.taille_cell
                y2 = y1 + self.taille_cell

                cell = self.canvas.create_rectangle(x1,y1,x2,y2,fill='white')
                self.rectangles[li][col] = cell

        self.canvas.bind("<MouseWheel>", self.molette_zoom)
        self.canvas.bind("<ButtonPress-3>", self.clic_droit)
        self.canvas.bind("<B3-Motion>", self.deplacer)

    def affichage_grille(self):
        if self.showgri.get() == 1:
            self.ligne = 'Black'
            self.maj()
        else:
            self.ligne = 'White'
            self.maj()

    def maj(self):
        for li in range(self.grille.nb):
            for col in range(self.grille.nb):
                color = self.couleur[self.grille.grid[li][col]] if self.grille.grid[li][col] < 9 else 'blue4'
                cell = self.rectangles[li][col]
                self.canvas.itemconfig(cell,fill=color,outline=self.ligne)

    def simulation(self):
        if not self.en_cour:
            print("Simulation terminée")
        else:
            self.canvas.unbind("<ButtonRelease-1>")
            changement = self.grille.maj()
            self.maj()
            if changement and self.en_cour:
                self.compteur += 1
                self.g.set(str(self.compteur))
                self.master.after(self.speed, self.simulation)
            else:
                print("Simulation terminée")

class Grille:
    def __init__(self, nb): #nb = nombre de lignes/colonnes
        self.nb = nb
        self.grid = [[0 for _ in range(self.nb)] for _ in range(self.nb)]

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

    g = Grille(50)
    fenetre = tk.Tk()
    fenetre.grid_rowconfigure(0, weight=1)
    fenetre.grid_columnconfigure(1, weight=1)
    inter = Interface(g,fenetre)
    fenetre.mainloop()

