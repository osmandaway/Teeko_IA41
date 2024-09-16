import pandas as pd

from datetime import date
from structures import *

def save_stats(listMoves, round, winnerP1,HP1, HP2, depthP1, depthP2, AvgTimeBEGP1, AvgIterBEGP1, AvgTimeBEGP2, AvgIterBEGP2, AvgTimeMBMGP1, AvgIterMBMGP1, AvgTimeMBMGP2, AvgIterMBMGP2):
    addstat = {
        'Date':[date.today().strftime("%d/%m/%Y")],
        'Round':[round],
        'Winner P1':[winnerP1],

        'Human P1':[HP1],
        'Human P2':[HP2],
        'Depth Minimax P1':[depthP1],
        'Depth Minimax P2':[depthP2],

        'Avg Time Bot Early Game P1':[AvgTimeBEGP1],
        'Avg Iter Bot Early Game P1':[AvgIterBEGP1],
        'Avg Time Bot Early Game P2':[AvgTimeBEGP2],
        'Avg Iter Bot Early Game P2':[AvgIterBEGP2],
        'Avg Time Main Bot Middle Game P1':[AvgTimeMBMGP1],
        'Avg Iter Main Bot Middle Game P1':[AvgIterMBMGP1],
        'Avg Time Main Bot Middle Game P2':[AvgTimeMBMGP2],
        'Avg Iter Main Bot Middle Game P2':[AvgIterMBMGP2],
    }
    df = pd.DataFrame(addstat)
    df.to_csv("resources/gameStats.csv", header=False, index=False, mode='a')

    df2 = pd.read_csv("resources/gameStats.csv")
    indexGame = df2.index[-1] + 2

    for element in listMoves:
        addstat2 = {
            'Index Game':[indexGame],
            'Round':[element.round],
            'Player':[element.player],
            'Move':[element.move],
        }
        df3 = pd.DataFrame(addstat2)
        df3.to_csv("resources/gameMoves.csv", header=False, index=False, mode='a')
    

    # Initialise dataframe in case of reset :
    # Date,Round,Winner P1,Human P1,Human P2,Depth P1,DepthP2,Avg Time Bot Early Game P1,Avg Iter Bot Early Game P1,Avg Time Bot Early Game P2,Avg Iter Bot Early Game P2,Avg Time Main Bot Middle Game P1,Avg Iter Main Bot Middle Game P1,Avg Time Main Bot Middle Game P2,Avg Iter Main Bot Middle Game P2
    # Date,round,winnerP1,HP1,HP2,Depth P1,DepthP2,AvgTimeBEGP1,AvgIterBEGP1,AvgTimeBEGP2,AvgIterBEGP2,AvgTimeMBMGP1,AvgIterMBMGP1,AvgTimeMBMGP2,AvgIterMBMGP2


def update_table(winnerP1, listMoves):
    df = pd.read_csv("resources/first_pion_stat.csv")

    if winnerP1:
        coordinate = listMoves[0].move[1]
    else:
        coordinate = listMoves[1].move[1]

    df.iloc[coordinate[0],coordinate[1]] +=1

    df.to_csv("resources/first_pion_stat.csv", index=False, mode='w')

    return df

def init_table():

    addheader = {
        'x0':[0,0,0,0,0],
        'x1':[0,0,0,0,0],
        'x2':[0,0,0,0,0],
        'x3':[0,0,0,0,0],
        'x4':[0,0,0,0,0],
    }
    df = pd.DataFrame(addheader)
    df.to_csv("resources/first_pion_stat.csv", index=False, mode='w')

# init_table()

def get_best_first_moves():
    df = pd.read_csv("resources/first_pion_stat.csv")
    max = df.max().max()
    second = 0
    for i in range(5):
        for j in range(5):
            if df.iloc[i,j] == max:
                best_move = (i,j)
    for i in range(5):
        for j in range(5):
            if df.iloc[i,j] > second and df.iloc[i,j] < max:
                second = df.iloc[i,j]
                second_best_move = (i,j)
    return (best_move, second_best_move)