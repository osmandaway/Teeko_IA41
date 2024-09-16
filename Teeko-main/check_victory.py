#check if the team win
def check_victory(game, team_number): 

    position_first = find_first_pion(game, team_number)

    if check_horizontal(game, team_number, position_first):
        return True
    
    elif check_vertical(game, team_number, position_first):
        return True
    
    elif check_diagonal_right(game, team_number, position_first):
        return True

    elif check_diagonal_left(game, team_number, position_first):
        return True

    elif check_square(game, team_number, position_first):
        return True

    else:
        return False

#find first pion of the team in the grid and return it's position
def find_first_pion(game, team_number): 
    for i in range(5):
        for j in range(5):
            if game.grid[i][j] == team_number:
                return [i,j]


#check if there is a horizontal victory from the first pion
def check_horizontal(game, team_number, position_first):

    if position_first[1] < 2:
        for i in range(4):
            if game.grid[position_first[0]][position_first[1]+i] != team_number:
                return False
        return True

    else :
        return False

#check if there is a vertical victory from the first pion
def check_vertical(game, team_number, position_first):
    
        if position_first[0] < 2:
            for i in range(4):
                if game.grid[position_first[0]+i][position_first[1]] != team_number:
                    return False
            return True
    
        else :
            return False

#check if there is a diagonal victory from the first pion on the right
def check_diagonal_right(game, team_number, position_first):
    if position_first[0] < 2 and position_first[1] < 2:
        for i in range(4):
            if game.grid[position_first[0]+i][position_first[1]+i] != team_number:
                return False
        return True

    else :
        return False

#check if there is a diagonal victory from the first pion on the left
def check_diagonal_left(game, team_number, position_first):
    if position_first[0] < 2 and position_first[1] > 2:
        for i in range(4):
            if game.grid[position_first[0]+i][position_first[1]-i] != team_number:
                return False
        return True

    else :
        return False

#check if there is a square victory from the first pion
def check_square(game, team_number, position_first):
    if position_first[0] < 4 and position_first[1] < 4:
        for i in range(2):
            for j in range(2):
                if game.grid[position_first[0]+i][position_first[1]+j] != team_number:
                    return False
        return True

    else :
        return False
    