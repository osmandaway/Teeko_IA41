import random
import copy

from grid import *
from check_victory import*
from structures import*
from functions import*

#from statistics import Statistics
from game_statistics import Stats

class Bot:
    def __init__(self, team_number, depth):
        self.team_number = team_number
        self.depth = depth

        # For each version of bot, initialise a class to retrieve some data
        self.statsEarlyGame = Stats()
        self.statsMinimax = Stats()


    #--------------------------------------------------------------------------------------------------------------------------------------------------
    #                                                             BOT / RANDOM / EARLY GAME
    #--------------------------------------------------------------------------------------------------------------------------------------------------

    def firstMove(self, gridC):

        coordinates = []

        #randomly choose a place to put the first piece

        coordinates.append(random.randint(0, 4))
        coordinates.append(random.randint(0, 4))

        while gridC.grid[coordinates[0]][coordinates[1]] != 0:
            coordinates[0] = random.randint(0, 4)
            coordinates[1] = random.randint(0, 4)
    
        return coordinates


    #--------------------------------------------------------------------------------------------------------------------------------------------------
    #                                           BOT / MINIMAX V2 / HEURISTIQUE / ALPHA PRUNING / MIDDLE GAME 
    #--------------------------------------------------------------------------------------------------------------------------------------------------

    def minMax(self, gridC, listState): 

        self.statsMinimax.startTimer()
        #list all possible moves
        list = list_all_possibles_moves(gridC, self.team_number)
        move_evaluation = []


        for move in list:
            move_evaluation.append((move, self.minValue(gridC, move, self.depth, listState, -1000, 1000)))

        best_move = max(move_evaluation, key=lambda x: x[1])
        self.statsMinimax.endTimer()
        self.statsMinimax.resetIter()
        
        return best_move[0]

    def eval(self, gridC, depth, listState, player): 

        if check_victory(gridC, self.team_number):
            return 100 + depth

        elif check_victory(gridC, self.team_number % 2 + 1):
            return -100 - depth

        elif is_redundance(listState, gridC, player):
            return -50 - depth

        else:

            #find all pions for each player
            list_own_pions = find_all_pions(gridC, self.team_number)
            list_adv_pions = find_all_pions(gridC, self.team_number % 2 + 1)

            # evaluate the spacing between the pions 
            # the higher the value, the better it is
            # value between -21 and 21
            
            spacing_value = 0

            # spacing between other pions
            min_i = min(list_adv_pions, key=lambda x: x[0])[0]
            min_j = min(list_adv_pions, key=lambda x: x[1])[1]

            max_i = max(list_adv_pions, key=lambda x: x[0])[0] + 1
            max_j = max(list_adv_pions, key=lambda x: x[1])[1] + 1

            area = (max_i - min_i) * (max_j - min_j)

            spacing_value += area

            # spacing between own pions
            min_i = min(list_own_pions, key=lambda x: x[0])[0]
            min_j = min(list_own_pions, key=lambda x: x[1])[1]

            max_i = max(list_own_pions, key=lambda x: x[0])[0] + 1
            max_j = max(list_own_pions, key=lambda x: x[1])[1] + 1

            area = (max_i - min_i) * (max_j - min_j)

            spacing_value -= area


            # evaluate the position of the pions (control of the center)
            # the higher the value, the better it is
            # value between -13 and 13 

            center_value = 0

            for pion in list_adv_pions:
                center_value += abs(2 - pion[0]) + abs(2 - pion[1])

            for pion in list_own_pions:
                center_value -= abs(2 - pion[0]) + abs(2 - pion[1])


            # evaluate the chance of having a diagonal victory
            # the higher the value, the better it is
            # value between -7 and 7

            delta = 0


            if len(list_own_pions) == 4:
                
                delta_i = []
                delta_j = []

                for i in range(3):
                    delta_i.append(list_own_pions[i][0] - list_own_pions[i+1][0])
                    delta_j.append(list_own_pions[i][1] - list_own_pions[i+1][1])

                # we look if space between pions is the same
                if delta_i[0] == delta_i[1]:
                    delta += 1
                else:
                    delta -= 1

                if delta_j[0] == delta_j[1]:
                    delta += 1
                else:
                    delta -= 1

                if delta_i[1] == delta_i[2]:
                    delta += 1
                else:
                    delta -= 1

                if delta_j[1] == delta_j[2]:
                    delta += 1
                else:
                    delta -= 1

                # we look if the pions are on diagonal between them
                for i in range(3):
                    if delta_i[i] == delta_j[i]:
                        delta += 1
                    else:
                        delta -= 1

            # compute the final score 

            score = spacing_value + center_value + delta

        return score # higher is the score better is the situation

    def maxValue(self, gridC, move, depth, listState, alpha, beta):
        
        self.statsMinimax.iterAdd1()
        #copy grid in order to not modify the original grid
        gridC_copy = copy.deepcopy(gridC)

        #move the piece
        gridC_copy = modify_grid(gridC_copy, move, 0, self.team_number % 2 + 1)
     
        if check_victory(gridC_copy, self.team_number % 2 + 1) or is_redundance(listState, gridC_copy, self.team_number % 2 + 1) or depth == 0:
            return self.eval(gridC_copy, depth, listState, self.team_number % 2 + 1)
        
        v = -100000

        #list all possible moves
        list = list_all_possibles_moves(gridC_copy, self.team_number)

        for move in list:
            v = max(v, self.minValue(gridC_copy, move, depth-1, listState, alpha, beta))
            if v >= beta: 
                return v
            alpha = max(alpha, v)
        
        return v


    def minValue(self, gridC, move, depth, listState, alpha, beta):

        self.statsMinimax.iterAdd1()
        #copy grid in order to not modify the original grid
        gridC_copy = copy.deepcopy(gridC)

        #move the piece
        gridC_copy = modify_grid(gridC_copy, move, 0, self.team_number)


        if check_victory(gridC_copy, self.team_number) or is_redundance(listState, gridC_copy, self.team_number) or depth == 0:
            return self.eval(gridC_copy, depth, listState, self.team_number)

        v = 100000
        
        #list all possible moves
        list = list_all_possibles_moves(gridC_copy, self.team_number % 2 + 1)

        for move in list:
            v = min(v, self.maxValue(gridC_copy, move, depth-1, listState, alpha, beta))
            if v <= alpha: 
                return v
            beta = min(beta, v)

        return v
   
    
