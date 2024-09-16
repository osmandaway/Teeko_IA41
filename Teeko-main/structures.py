# Structure definitions for the game. I didn't know nametuple so I created structures
class MoveAndAvScore:

    def __init__(self, round, player, move):
        self.round = round
        self.player = player
        self.move = move

class Node:
    
    def __init__(self,state,father,path):
        self.state=state
        self.father=father
        self.path = path