import numpy as np
from timeit import default_timer as timer

class Stats:

    # Class to store statistics about the game
    def __init__(self):
        self.average_time = []
        self.average_iter = []
        self.nbr_iter = 0
        self.time = 0

    # Reset all the statistics
    def resetAll(self):
        self.average_time = []
        self.average_iter = []
        self.nbr_iter = 0
        self.time = 0

    # Start a timer
    def startTimer(self):
        self.time = timer()

    # Stop the timer and add the time to the list of average time
    def endTimer(self):
        deltaTime = timer() - self.time
        self.average_time.append(deltaTime)

    # Add 1 to the number of iteration
    def iterAdd1(self):
        self.nbr_iter+=1

    # Add a number to the number of iteration
    def resetIter(self):
        self.average_iter.append(self.nbr_iter)
        self.nbr_iter = 0

    # Get the average time of all the moves
    def getAvgTime(self):
        if self.time != 0:
            return np.mean(self.average_time)
        else:
            return np.nan

    # Get the average number of iteration of all the moves
    def getAvgIter(self):
        if self.time != 0:
            return np.mean(self.average_iter)
        else:
            return np.nan

    # Print the statistics in the terminal
    def printStats(self):
        if self.time != 0:
            print("Average time per move was : " + str(np.mean(self.average_time)))
            print("Average iter per move was : " + str(round(np.mean(self.average_iter))))