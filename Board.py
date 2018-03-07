#!/usr/bin/env python
# -*- coding: utf-8 -*-

from random import randint
from copy import deepcopy
from math import sqrt


class Board(object):

    OBSTACLE = -1
    FREE_SPACE = 1
    GOAL = 2
    PLAYER_POINT = 0

    def __init__(self, height, width, move_pattern=None, obstacle_chance=50):
        """

        :param height: Hauteur du plateau
        :param width: Largeur du plateau
        :param move_pattern: Patterne de movement possible du joueur:
                            Dois êtres sous la forme [{"y": action 1 en y, "x" action 1 en x, "cost": coue du move},
                                                      ...
                                                      {"y": action n en y, "x" action n en x, "cost": coue du move}
        :param obstacle_chance: Chance d'obtenir un obstacle si égale a 0 il n'y aura pas d'obstacle
        """

        self.height = height
        self.width = width
        #           Bord haut +2 car il y a le bord gauche puis droit
        self.mat = [[Board.OBSTACLE] * (width + 2)] + \
                   [[Board.OBSTACLE] + [Board.FREE_SPACE] * width + [Board.OBSTACLE] for _ in range(height)] + \
                   [[Board.OBSTACLE] * (width + 2)]

        # creation des obstacles
        for y in range(1, height + 1):
            for x in range(1, width + 1):
                if obstacle_chance > randint(1, 99):
                    self.mat[y][x] = Board.OBSTACLE
                else:
                    self.mat[y][x] = Board.FREE_SPACE

        # Position du joueur
        self.player_pos = {"y": randint(1, height), "x": randint(1, width)}
        self.mat[self.player_pos["y"]][self.player_pos["x"]] = Board.PLAYER_POINT

        # position du goal
        self.goal_pos = {"y": randint(1, height), "x": randint(1, width)}
        self.mat[self.goal_pos["y"]][self.goal_pos["x"]] = Board.GOAL

        # Goal atteint
        self.reach_goal = False

        # Patterne de mouvement possible pour le joueur
        if move_pattern is not None:
            self.move_pattern = deepcopy(move_pattern)
        else:
            self.move_pattern = list()
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if not (i == 0 and j == 0):
                        cost = sqrt(2) if abs(i) == abs(j) else 1
                        self.move_pattern.append({"y": i, "x": j, "cost": cost})

    def get_possible_move(self):
        """
        Fonction qui renvoie la liste de coordonée possible
        :return: liste sous le forme [{"y": position y, "x": position x, "coue": coue du move},
                                        ...
                                      {"y": position y, "x": position x, "coue": coue du move}]
        """
        move_possible = list()
        for move in self.move_pattern:
            if self.mat[self.player_pos["y"] + move["y"]][self.player_pos["x"] + move["x"]] != Board.OBSTACLE:
                move_possible.append(self.__get_move_coord(move))
        return move_possible

    def __get_move_coord(self, move):
        """
        Fonction qui renvoie la nouvelle position en fonction du move donnée
        :param move: Move qui est dans le move patterner
        :return: un dico sous la forme: {"y": position y, "x": position x, "cost": coue du mouvement
        """
        return {"y": move["y"] + self.player_pos["y"], "x": move["x"] + self.player_pos["x"], "cost": move["cost"]}

    def move_player(self, coordo):
        """
        Fonction qui deplasse le joueur a la coordoner donnée si on le deplasse a l'objectif on mais a jours
        l'attribut reach_goal
        :param coordo: Sous le forme {"y": position y, "x": position x}
        :return: True le joueur c'est deplasser sinon False
        """

        if self.mat[coordo["y"]][coordo["x"]] == Board.OBSTACLE:
            return False
        elif self.mat[coordo["y"]][coordo["x"]] == Board.GOAL:
            self.reach_goal = True
            self.mat[coordo["y"]][coordo["x"]] = Board.PLAYER_POINT
        else:
            self.mat[coordo["y"]][coordo["x"]] = Board.PLAYER_POINT
            self.mat[self.player_pos["y"]][self.player_pos["x"]] = Board.FREE_SPACE

        self.player_pos = deepcopy(coordo)
        return True


if __name__ == "__main__":

    b = Board(10, 10, 0)
