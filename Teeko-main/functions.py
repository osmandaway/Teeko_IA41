from structures import *
from grid import *

#List of all the moves possible for a player
def list_all_possibles_moves(gridC, team_number): 
    list = []

    pions = find_all_pions(gridC, team_number)

    if len(pions) >= 4:
        for pion in pions: 
            i = pion[0]
            j = pion[1]
            for k in range(i-1,i+2):
                for l in range(j-1,j+2):
                    if k>-1 and k<5 and l<5 and l>-1:
                        if gridC.grid[k][l] == 0:
                            list.append([[i,j],[k,l]])
    else: 
        for k in range(5):
            for l in range(5):
                if gridC.grid[k][l] == 0:
                    list.append([0,[k,l]])
    
    return list
    

#find all the pions of a team
def find_all_pions(gridC, team_number):
    list = []
    for i in range(5):
        for j in range(5):
            if gridC.grid[i][j] == team_number:
                list.append([i,j])
    return list


#modify the grid with a move
def modify_grid(gridC, move_coordinates, number_first_coordinate, number_second_coordinate):

    if move_coordinates[0] == 0:
        gridC.grid[move_coordinates[1][0]][move_coordinates[1][1]] = number_second_coordinate

    else:
        gridC.grid[move_coordinates[0][0]][move_coordinates[0][1]] = number_first_coordinate
        gridC.grid[move_coordinates[1][0]][move_coordinates[1][1]] = number_second_coordinate
    
    return gridC

#place a pion on the grid
def place_pion(gridC, coordinate, number):
    gridC.grid[coordinate[0]][coordinate[1]] = number
    return gridC

def addListMoves(listMoves, round, player, move):
    listMoves.append(MoveAndAvScore(round, player, move))
    #for element in listMoves:
    #    print("Round : " + str(element.round) + ", player : " + str(element.player) + ", move : " + str(element.move))
    return listMoves

def is_redundance(listState, grid, player):
    
    red_pions = find_all_pions(grid, 1)
    blue_pions = find_all_pions(grid, 2)
    
    state = [player, red_pions, blue_pions]

    if state in listState:
        return True
    else:
        return False