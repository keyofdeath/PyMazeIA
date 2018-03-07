#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tkinter import *
from tkinter.ttk import *
from time import sleep, time
from Board import *


class BoardGui(object):
    """
    Class qui va soccuper de crée l'interface graphique est de soccuper de l'éxacution des différents algorithme
    """

    def __init__(self, board):
        """

        :param board: Objet de type Board pour les information sur le plateau
        """

        self.board = board

        #                                        _________
        # ______________________________________/PARTIE UI\______________________________________

        font9 = "-family {Segoe UI} -size 9 -weight normal -slant roman -underline 0 -overstrike 0"

        # Liste des algos disponible a la selection
        algo = ["Recherche profondeur", "Recherche largeur", "A*"]

        self.player_shape = None
        self.goal_shape = None

        self.top = Tk()
        self.select_set = IntVar()

        # Fenêtres principale
        self.top.geometry("923x771+500+167")
        self.top.title("IA Maze")
        self.top.configure(background="#d9d9d9")
        self.top.configure(highlightbackground="#d9d9d9")
        self.top.configure(highlightcolor="black")
        self.top.resizable(width=False, height=False)

        # Canvas pour le dessin
        self.canvas = Canvas(self.top)
        self.canvas.place(relx=0.01, rely=0.01, relheight=0.79, relwidth=0.98)
        self.canvas.configure(background="white")
        self.canvas.configure(borderwidth="2")
        self.canvas.configure(highlightbackground="#d9d9d9")
        self.canvas.configure(highlightcolor="black")
        self.canvas.configure(insertbackground="black")
        self.canvas.configure(relief=RIDGE)
        self.canvas.configure(selectbackground="#c4c4c4")
        self.canvas.configure(selectforeground="black")
        self.canvas.configure(width=906)
        self.canvas.bind("<Button-1>", lambda event: self.__click_event(event))

        # Input pour la largeur du plateau
        self.largeur = Spinbox(self.top, from_=1.0, to=100.0)
        self.largeur.place(relx=0.07, rely=0.86, relheight=0.03, relwidth=0.15)
        self.largeur.configure(activebackground="#f9f9f9")
        self.largeur.configure(background="white")
        self.largeur.configure(buttonbackground="#d9d9d9")
        self.largeur.configure(disabledforeground="#a3a3a3")
        self.largeur.configure(font=font9)
        self.largeur.configure(foreground="black")
        self.largeur.configure(from_="10")
        self.largeur.configure(highlightbackground="black")
        self.largeur.configure(highlightcolor="black")
        self.largeur.configure(insertbackground="black")
        self.largeur.configure(selectbackground="#c4c4c4")
        self.largeur.configure(selectforeground="black")
        self.largeur.configure(to="100.0")

        # Input pour la hauteur du plateau
        self.hauteur = Spinbox(self.top, from_=1.0, to=100.0)
        self.hauteur.place(relx=0.22, rely=0.86, relheight=0.03, relwidth=0.15)
        self.hauteur.configure(activebackground="#f9f9f9")
        self.hauteur.configure(background="white")
        self.hauteur.configure(buttonbackground="#d9d9d9")
        self.hauteur.configure(disabledforeground="#a3a3a3")
        self.hauteur.configure(font=font9)
        self.hauteur.configure(foreground="black")
        self.hauteur.configure(from_="10")
        self.hauteur.configure(highlightbackground="black")
        self.hauteur.configure(highlightcolor="black")
        self.hauteur.configure(insertbackground="black")
        self.hauteur.configure(selectbackground="#c4c4c4")
        self.hauteur.configure(selectforeground="black")
        self.hauteur.configure(to="100.0")

        # Input pour la selection de l'algo a éxécuter
        self.ia_select = Combobox(self.top, values=algo, state='readonly')
        self.ia_select.place(relx=0.74, rely=0.86, relheight=0.03, relwidth=0.24)
        self.ia_select.configure(takefocus="")

        # Botton pour générer le plateau
        self.generate = Button(self.top)
        self.generate.place(relx=0.07, rely=0.9, height=44, width=417)
        self.generate.configure(command=self.__new_board)
        self.generate.configure(text='''Generate''')
        self.generate.configure(width=417)

        # Boutton pour start l'algo
        self.start = Button(self.top)
        self.start.place(relx=0.74, rely=0.9, height=44, width=227)
        self.start.configure(command=self.__start)
        self.start.configure(text='''Start''')

        self.Label1 = Label(self.top)
        self.Label1.place(relx=0.07, rely=0.82, height=21, width=46)
        self.Label1.configure(text='''Largeur''')

        self.Label2 = Label(self.top)
        self.Label2.place(relx=0.22, rely=0.82, height=21, width=49)
        self.Label2.configure(text='''Hauteur''')

        self.Label3 = Label(self.top)
        self.Label3.place(relx=0.74, rely=0.82, height=21, width=64)
        self.Label3.configure(text='''Algo select''')

        # Input pour entree le taux d'obstacle générer
        self.obstacle_pourcent = Spinbox(self.top, from_=1.0, to=100.0)
        self.obstacle_pourcent.place(relx=0.37, rely=0.86, relheight=0.03, relwidth=0.15)
        self.obstacle_pourcent.configure(activebackground="#f9f9f9")
        self.obstacle_pourcent.configure(background="white")
        self.obstacle_pourcent.configure(buttonbackground="#d9d9d9")
        self.obstacle_pourcent.configure(disabledforeground="#a3a3a3")
        self.obstacle_pourcent.configure(font=font9)
        self.obstacle_pourcent.configure(foreground="black")
        self.obstacle_pourcent.configure(from_="50")
        self.obstacle_pourcent.configure(highlightbackground="black")
        self.obstacle_pourcent.configure(highlightcolor="black")
        self.obstacle_pourcent.configure(insertbackground="black")
        self.obstacle_pourcent.configure(selectbackground="#c4c4c4")
        self.obstacle_pourcent.configure(selectforeground="black")
        self.obstacle_pourcent.configure(to="100.0")

        self.Label4 = Label(self.top)
        self.Label4.place(relx=0.37, rely=0.82, height=21, width=65)
        self.Label4.configure(text='''Obstacle %''')

        self.Labelframe1 = LabelFrame(self.top)
        self.Labelframe1.place(relx=0.53, rely=0.82, relheight=0.14, relwidth=0.2)
        self.Labelframe1.configure(relief=GROOVE)
        self.Labelframe1.configure(text='''Placer élément''')
        self.Labelframe1.configure(width=180)

        # Radio pour choisire si on veut replacer le joueur dans le canvas
        self.joueur = Radiobutton(self.Labelframe1, variable=self.select_set, value=1)
        self.joueur.place(relx=0.06, rely=0.29, relheight=0.24, relwidth=0.35)
        self.joueur.configure(text='''Joueur''')

        # Radio pour choisire si on veut replacer l'objectif dans le canvas
        self.objectif = Radiobutton(self.Labelframe1, variable=self.select_set, value=2)
        self.objectif.place(relx=0.06, rely=0.57, relheight=0.24, relwidth=0.39)
        self.objectif.configure(text='''Objectif''')

        self.select_set.set(1)

        # Vitesse d'éxécution
        self.speed = Spinbox(self.top, from_=1.0, to=100.0)
        self.speed.place(relx=0.07, rely=0.96, relheight=0.03, relwidth=0.15)
        self.speed.configure(activebackground="#f9f9f9")
        self.speed.configure(background="white")
        self.speed.configure(buttonbackground="#d9d9d9")
        self.speed.configure(disabledforeground="#a3a3a3")
        self.speed.configure(font=font9)
        self.speed.configure(foreground="black")
        self.speed.configure(from_="0.3")
        self.speed.configure(highlightbackground="black")
        self.speed.configure(highlightcolor="black")
        self.speed.configure(insertbackground="black")
        self.speed.configure(selectbackground="#c4c4c4")
        self.speed.configure(selectforeground="black")
        self.speed.configure(to="100.0")
        self.speed.configure(width=265)

        self.Label5 = Label(self.top)
        self.Label5.place(relx=0.25, rely=0.96, height=21, width=74)
        self.Label5.configure(text='''Vitesse (en s)''')

        self.top.mainloop()

    def draw_player(self, y, x):
        """
        Fonction qui supprime le dessin du joueur est le re dessine a la position donnée
        :param y:
        :param x:
        :return:
        """

        if self.player_shape is not None:
            self.canvas.delete(self.player_shape)

        can_largeur = self.canvas.winfo_width()
        can_hauteur = self.canvas.winfo_height()

        #  + 2 car il y a les bords
        colomne_space = can_largeur // (self.board.width + 2)
        ligne_space = can_hauteur // (self.board.height + 2)

        self.player_shape = self.canvas.create_rectangle(colomne_space * x, ligne_space * y,
                                                         (colomne_space * x) + colomne_space,
                                                         (ligne_space * y) + ligne_space,
                                                         fill="#FF0002")
        self.canvas.update_idletasks()

    def draw_target(self, y, x):
        """
        Fonction qui supprime le dessin de l'objectif est le re dessine a la position donnée
        :param y:
        :param x:
        :return:
        """

        if self.goal_shape is not None:
            self.canvas.delete(self.goal_shape)

        can_largeur = self.canvas.winfo_width()
        can_hauteur = self.canvas.winfo_height()

        #  + 2 car il y a les bords
        colomne_space = can_largeur // (self.board.width + 2)
        ligne_space = can_hauteur // (self.board.height + 2)

        self.goal_shape = self.canvas.create_rectangle(colomne_space * x, ligne_space * y,
                                                       (colomne_space * x) + colomne_space,
                                                       (ligne_space * y) + ligne_space,
                                                       fill="#00FF00")
        self.canvas.update_idletasks()

    def draw_obstacle(self, y, x):
        """
        Fonction qui dessine un obstacle a la position donnée
        :param y:
        :param x:
        :return:
        """
        can_largeur = self.canvas.winfo_width()
        can_hauteur = self.canvas.winfo_height()

        #  + 2 car il y a les bords
        colomne_space = can_largeur // (self.board.width + 2)
        ligne_space = can_hauteur // (self.board.height + 2)

        self.canvas.create_rectangle(colomne_space * x, ligne_space * y,
                                     (colomne_space * x) + colomne_space, (ligne_space * y) + ligne_space,
                                     fill="#006F79")

    def __click_event(self, event):
        """
        Fonction appeler quand on click sur la canvas
        :param event:
        :return:
        """

        if self.board is None:
            return

        largeur = self.canvas.winfo_width()
        hauteur = self.canvas.winfo_height()

        colomne_space = largeur / self.board.width
        ligne_space = hauteur / self.board.height

        # on recupaire le position dans la grille
        grid_pos_x = round(event.x / colomne_space)
        grid_pos_y = round(event.y / ligne_space)

        # Si on a fait un click gauche et que on a choisi de placer un joueur
        if self.select_set.get() == 1 and self.board.mat[grid_pos_y][grid_pos_x] == self.board.FREE_SPACE:
            print("player")
            self.board.mat[self.board.player_pos["y"]][self.board.player_pos["x"]] = Board.FREE_SPACE
            self.board.mat[grid_pos_y][grid_pos_x] = Board.PLAYER_POINT
            self.board.player_pos["y"] = grid_pos_y
            self.board.player_pos["x"] = grid_pos_x
            self.draw_player(grid_pos_y, grid_pos_x)

        # Si on a fait un click gauche et que on a choisi de placer la cible
        elif self.select_set.get() == 2 and self.board.mat[grid_pos_y][grid_pos_x] == self.board.FREE_SPACE:
            print("target")
            self.board.mat[self.board.goal_pos["y"]][self.board.goal_pos["x"]] = Board.FREE_SPACE
            self.board.mat[grid_pos_y][grid_pos_x] = Board.GOAL
            self.board.goal_pos["y"] = grid_pos_y
            self.board.goal_pos["x"] = grid_pos_x
            self.draw_target(grid_pos_y, grid_pos_x)

    #                                        __________
    # ______________________________________/ALGO DU TP\______________________________________

    def __bfs(self, speed):
        """
        Algo recherche en largeur
        :param speed: vitesse execution
        :return:
        """
        start = time()
        # On ajoute tout les move possibles
        open_task = [move for move in self.board.get_possible_move()]
        # On ajoute la position du joueur
        close = [deepcopy(self.board.player_pos)]
        while not self.board.reach_goal and len(open_task) > 0:
            # on recupaire le move en tête de liste
            move = open_task.pop(0)
            if move in close:
                continue
            # on deplase le joueur
            self.board.move_player(move)
            close.append(move)
            # on ajoute tout les move possible
            possible_move = list()
            # on retir tout les move qui on déja été fait
            for coord in self.board.get_possible_move():
                if coord not in close:
                    possible_move.append(coord)
            # Si on a des posibliter on les ajoutes
            if len(possible_move) != 0:
                open_task.extend(possible_move)
            self.draw_player(self.board.player_pos["y"], self.board.player_pos["x"])
            if speed != 0:
                sleep(speed)

        print("Fin du depth first search temps mie: {} sec".format(round(time() - start)))

    def __a_star(self, speed):
        """

        :param speed:
        :return:
        """

        def h(pos, goal):
            """
            Fonction heuristique distance de manathane
            :param pos:
            :param goal:
            :return:
            """
            return abs(goal["y"] - pos["y"]) + abs(goal["x"] - pos["x"])

        start = time()
        # on recupaire les move possibles
        open_task = [move for move in self.board.get_possible_move()]
        close = [deepcopy(self.board.player_pos)]

        while not self.board.reach_goal and len(open_task) > 0:

            # on tri nos chemin possible par ordre de coue le moin cher g + h
            open_task = sorted(open_task, key=lambda node: node["cost"] + h(node, self.board.goal_pos))
            # on recupaire le move le plus intérésent
            move = open_task.pop(0)
            # on regarde si le noeud est déja dans close
            # pour cela on filtre les noeud avec les maime coordoner (La fonction 'in' ne marche pas car les
            # noeud peuve avoire la maime position mais pas le maime coue)
            if len(list(filter(lambda node: node["y"] == move["y"] and node["x"] == move["x"], close))) != 0:
                continue
            self.board.move_player(move)
            close.append(move)
            # on ajoute tout les move possible
            possible_move = list()
            # on retir tout les move qui on déja été fait
            for coord in self.board.get_possible_move():
                # on regarde si le move n'est pas déja dans close
                node_in_close = list(filter(lambda node: node["y"] == coord["y"] and node["x"] == coord["x"], close))
                if len(node_in_close) == 0:
                    # Si c'est un noeud déja ouvert on regarde si son coue est plus petit si oui on le remplace
                    node_in_open = list(filter(lambda node: node["y"] == coord["y"] and node["x"] == coord["x"],
                                               open_task))
                    # Si le noeud est déja dans open
                    if len(node_in_open) != 0:
                        if coord["cost"] + move["cost"] < node_in_open[0]["cost"]:
                            # On modifie le cost au moin cherche
                            node_in_open[0]["cost"] = coord["cost"] + move["cost"]
                    else:
                        # on augmente le cost par raport au noeud d'avent
                        coord["cost"] += move["cost"]
                        possible_move.append(coord)
            # Si on a des posibliter on les ajoutes
            if len(possible_move) != 0:
                open_task.extend(possible_move)

            self.draw_player(self.board.player_pos["y"], self.board.player_pos["x"])
            sleep(speed)
        print("Fin du A* temps mie: {} sec".format(round(time() - start)))

    def __dfs(self, speed):
        """
        Algo recherche en profondeur
        :param speed:
        :return:
        """

        start = time()
        open_task = [move for move in self.board.get_possible_move()]
        close = [deepcopy(self.board.player_pos)]
        while not self.board.reach_goal and len(open_task) > 0:

            move = open_task.pop()
            if move in close:
                continue
            self.board.move_player(move)
            close.append(move)
            # on ajoute tout les move possible
            possible_move = list()
            # on retir tout les move qui on déja été fait
            for coord in self.board.get_possible_move():
                if coord not in close:
                    possible_move.append(coord)
            # Si on a des posibliter on les ajoutes
            if len(possible_move) != 0:
                open_task.extend(possible_move)
            self.draw_player(self.board.player_pos["y"], self.board.player_pos["x"])
            sleep(speed)

        print("Fin du depth first search temps mie: {} sec".format(round(time() - start)))

    # ______________________________________FIN ALGO DU TP______________________________________

    def __start(self):
        """
        Fonction appeler quand on apuiy sur start
        :return:
        """
        if self.board is None:
            self.__new_board()
        try:
            speed = float(self.speed.get())
        except ValueError:
            print("Error get speed")
            return

        # on fait un dico event pour faciliter l'apelle au differente fonction
        func = {"Recherche profondeur": self.__dfs, "Recherche largeur": self.__bfs, "A*": self.__a_star}
        try:
            # on appele l'algo
            func[self.ia_select.get()](speed)
        except KeyError:
            print("Error exe algorithm")

    def __new_board(self):
        """
        Fonction qui cree un nouveaux plateau et le dessine
        :return:
        """
        # on supprime tout les dessine du canvas
        self.canvas.delete("all")
        try:
            hauteur = int(self.hauteur.get())
            largeur = int(self.largeur.get())
            self.board = Board(hauteur, largeur, None, int(self.obstacle_pourcent.get()))
        except ValueError as e:
            print("Error get dimention: ", e)
            return

        can_largeur = self.canvas.winfo_width()
        can_hauteur = self.canvas.winfo_height()

        #  + 2 car il y a les bords
        colomne_space = can_largeur // (largeur + 2)
        ligne_space = can_hauteur // (hauteur + 2)

        # dessine les colomne
        for i in range(1, largeur + 2):
            x = colomne_space * i
            self.canvas.create_line(x, 0, x, can_hauteur)

        # dessine les ligne
        for i in range(1, hauteur + 2):
            y = ligne_space * i
            self.canvas.create_line(0, y, can_largeur, y)

        # On dessine le plateau
        for y in range(len(self.board.mat)):
            for x in range(len(self.board.mat[y])):
                if self.board.mat[y][x] == self.board.OBSTACLE:
                    self.draw_obstacle(y, x)
                elif self.board.mat[y][x] == self.board.GOAL:
                    self.draw_target(y, x)
                elif self.board.mat[y][x] == self.board.PLAYER_POINT:
                    self.draw_player(y, x)


if __name__ == "__main__":

    n = BoardGui(None)
