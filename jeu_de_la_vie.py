from tkinter import *
from random import *
import numpy

# C'est une fonction permettant de calculer le nombre de voisin autour d'un élément dans la matrice
def voisin(matrice, nligne, ncolonne):
    nb_voisin = 0
    for i in range(nligne - 1, nligne + 2):
        if (matrice[(i + len(matrice)) % len(matrice)][(ncolonne - 1 + len(matrice)) % len(matrice)] != 0):
            nb_voisin += 1
        if (matrice[(i + len(matrice)) % len(matrice)][(ncolonne + 1 + len(matrice)) % len(matrice)] != 0 ):
            nb_voisin += 1
        if (i + len(matrice)) % len(matrice) != nligne:
            if matrice[(i + len(matrice)) % len(matrice)][ncolonne] != 0:
                nb_voisin += 1
    return nb_voisin

# C'est une fonction permettant de générer une nouvelle génération suivante à partir de la génération courante
def mise_a_jour(matrice):
    nb_voisin = 0
    nouvelle_matrice = numpy.zeros((len(matrice), len(matrice))) # initialiser une nouvelle matrice vide en utilisant la fonction numpy.zeros()
    # On parcourt toutes les cases dans la matrice
    for i in range(0, len(matrice)):
        for j in range(0, len(matrice)):
            nb_voisin = voisin(matrice, i, j) # Obtenir le nombre de voisins survivants de l'élément actuelle
            if nb_voisin == 2:
                nouvelle_matrice[i][j] = matrice[i][j]
            elif nb_voisin == 3:
                nouvelle_matrice[i][j] = 1
            else:
                nouvelle_matrice[i][j] = 0
    return nouvelle_matrice # retourner la nouvelle matrice
    
# C'est une fonction permettant d’initialiser une matrice de la taille récupérée par le scale « taille de la grille » 
# et d’un pourcentage d’élément de la matrice égale à 1 également récupérée par le scale « % de vie»  de l’interface graphique.
def init_matrice(taille, pourcentage_vie):
    pourcentage_vie = pourcentage_vie / 100 # Convertir la valeur de pourcentage_vie en une valeur entre 0 et 1
    values = [0, 1] # C'est une liste de valeur propable pour initialiser une matrice
    weights = [1 - pourcentage_vie, pourcentage_vie] # C'est la probabilité de 0 et 1, 1-pourcentage_vie est la probabilité pour 0 et pourcentage_vie est la probabilité pour 1
    matrice = numpy.zeros((taille, taille)) # initialiser une matrice vide
    # On utilise la fonction choices de la module "random" pour obetenir 0 ou 1 par la probabilité conrrespondante
    for i in range(0, taille):
        for j in range(0, taille):
            matrice[i][j] = choices(values, weights, k=1)[0] # Ce que la fonction retourne, c'est une liste, donc on prend le premier élément de la liste
    return matrice

# C'est une fonction permettant de dessiner des grilles
def draw_grid(width, taille):
    for widget in Frame2.winfo_children(): # Avant de dessiner des nouvelles grilles, on détruit des grilles existantes dans Frame2
        widget.destroy()
    grid = Canvas(Frame2, width=width, height=width, background="white") # Création d'un objet de type Canvas dans le Frame2
    sizePerCellule = width / taille # la longeur de chaque cellules
    x, y = 0, 0
    for i in range(taille):
        x += sizePerCellule
        y += sizePerCellule
        grid.create_line(x,0,x,width, fill="black") # lignes verticales
        grid.create_line(0,y,width,y, fill="black") # lignes horizontales
    grid.pack()
    return grid

# C'est une fonction permettant de dessiner une grille en différenciant les cellules vivantes et mortes
# les cellules vivantes: rouge
# les cellules mortes: blanc 
def fill_grid(matrice, grid):
    grid.delete("rectangles") # Avant de mettre les cellules vivantes en rouge, on efface les cellules précédantes  
    sizePerCellule = 600 / len(matrice) # la longeur de chaque cellules
    for i in range(len(matrice)):
        for j in range(len(matrice)):
            if matrice[i][j] == 1: # Si la valeur d'une cellule = 1, on dessine un carré rouge dans cette cellule 
                grid.create_rectangle(j*sizePerCellule, i*sizePerCellule, (j+1)*sizePerCellule, (i+1)*sizePerCellule, fill="red", tag="rectangles")

# C'est une fonction permettant de continuer le déroulement du jeu de la vie
def run():
    global stop
    if stop == FALSE: # Si stop = FALSE, on continue le déroulement du jeu de la vie
        global matrice
        new_matrice = mise_a_jour(matrice) # mise a jour de la matrice
        fill_grid(new_matrice, grid) # remplissage de la grille avec la matrice
        matrice = new_matrice
        delay = int(1 * 1000 / vitesse.get()) # C'est le temps entre deux affichages, plus la vitesse est grande, plus le temps entre deux affichages est court
        window.after(delay, run) # lancement de la fonction run après delay s

# C'est une fonction permettant d’initialiser une grille et de l’afficher dans l’interface
def initialiser():
    arreter() # arrêter le jeu avant d'initialiser
    global matrice
    matrice = init_matrice(taille.get(), pourcentage_vie.get()) # Générer une matrice d'initialisation
    global grid
    grid = draw_grid(600, taille.get()) # Dessiner la grille
    fill_grid(matrice, grid) # remplissage de la grille avec la matrice d'initialisation

# C'est une fonction permettant de lancer le déroulement du jeu de la vie
def lancer():
    global stop
    stop = FALSE
    run()

# C'est une fonction permettant d'arrêter le déroulement du jeu de la vie
def arreter():
    global stop
    stop = TRUE

# C'est une fonction permettant de de stopper le programme et quitter l’interface graphique.
def quitter():
    window.destroy()

# L'interface graphique
window = Tk()
window.title("SR01 Jeu de la vie")
window.geometry("800x600")

# Frame de la grille
Frame2 = Frame(window, width=600, height=600, bg="#ffffff")
Frame2.pack(side=LEFT)

# Frame des boutons
Frame1 = Frame(window, width=200, height=600, bg="#f0eeec")
Frame1.pack_propagate(FALSE)
Frame1.pack(side=RIGHT)

# Buttons dans Frame1
Button1 = Button(Frame1, text="Quitter", bg="#d5d3d2", fg="#1d4699", command=quitter).pack(side=BOTTOM, fill=X)

Button2 = Button(Frame1, text="Lancer", bg="#d5d3d2", fg="#1d4699", command=lancer).pack(side=TOP, fill=X)

Button3 = Button(Frame1, text="Arreter", bg="#d5d3d2", fg="#1d4699", command=arreter).pack(side=TOP, fill=X)

Button4 = Button(Frame1, text="Initialiser", bg="#d5d3d2", fg="#1d4699", command=initialiser).pack(side=TOP, fill=X)

# variable pour récupérer la vitesse dans le scale 'Vitesse'
vitesse = IntVar()
Scale1 = Scale(Frame1, variable=vitesse, from_=1, to=15, orient=HORIZONTAL,  label = 'Vitesse', fg='#1d4699')
Scale1.pack(side=BOTTOM)
Scale1.set(1) # la vitesse par défaut est 1

# variable pour récupérer le pourcentage_vie dans le scale '% de vie'
pourcentage_vie = IntVar()
Scale2 = Scale( Frame1, variable=pourcentage_vie ,from_=10, to=90, orient = HORIZONTAL, label = '% de vie', fg='#1d4699' )
Scale2.pack(side=BOTTOM)
Scale2.set(20) # le pourcentage_vie par défaut est 20

# variable pour récupérer la taille dans le scale 'Taille de la grille'
taille = IntVar()
Scale3 = Scale( Frame1, variable=taille ,from_=10, to=100, resolution=5, orient = HORIZONTAL,  label = 'Taille de la grille', fg='#1d4699' )
Scale3.pack(side=BOTTOM)
Scale3.set(30) # la taille par défaut est 30

window.mainloop()