import numpy as np

from bot import *
from check_victory import *
from functions import *
from graphics import *
from Imp_Exp_Data import *


#Déroulement et fonction relative à la game
class Game:
    def __init__(self):

        self.gridC = Grid(4,4) # Initialise une grille dans la game
        self.graphics = Graphics(self.gridC)
        
        #----------------------------------------
        # Define player 1 and player 2 :
        #----------------------------------------
        self.player1 = True # False:IA / True:human
        self.player2 = True # False:IA / True:human

        #----------------------------------------
        # State of the game
        #----------------------------------------

        self.earlygame = False
        self.middlegame = False
        self.gameover = False

        #----------------------------------------
        # Different variables
        #----------------------------------------

        self.round = 1
        self.listMoves = []
        self.listState = []
        self.depth1 = 2
        self.depth2 = 2
        self.turnPlayer1 = True
        self.done = False

        #----------------------------------------
        # Endless mode
        #----------------------------------------

        self.endless = False
        self.random_first_move = False
    
    #--------------------------------------------------------------------------------------------------------------------------------------------------
    #                                                                   COURSE OF THE GAME
    #--------------------------------------------------------------------------------------------------------------------------------------------------

    def run(self):
        running = True #Variable qui permet de quitter la partie / le jeu
        
        while running:
            
            # Check for user input
            running = self.graphics.checkInput()

            # Call appropriate game function based on game state
            if self.earlygame:
                self.earlyGame()

            elif self.middlegame:
                self.play()

            elif self.gameover:
                self.gameOver()
                
            else:
                self.mainMenu()
            
            # Update the screen
            self.graphics.updateScreen()

    #--------------------------------------------------------------------------------------------------------------------------------------------------
    #                                                                       MAIN MENU
    #--------------------------------------------------------------------------------------------------------------------------------------------------

    # Function to handle the main menu of the game
    def mainMenu(self):
        # Variables to track button presses
        up1 = False
        down1 = False
        up2 = False
        down2 = False

        # Draw the main menu
        self.graphics.mainMenuScript()
        self.player1 = self.graphics.bot_button1.draw(self.player1, self.graphics.mousePosition)
        self.player1 = self.graphics.human_button1.draw(self.player1, self.graphics.mousePosition)

        self.player2 = self.graphics.bot_button2.draw(self.player2, self.graphics.mousePosition)
        self.player2 = self.graphics.human_button2.draw(self.player2, self.graphics.mousePosition)

        # If player 1 is an AI, allow depth to be adjusted
        if not self.player1:
            # Hide the up and down buttons if the depth is at the maximum or minimum
            if self.depth1 < 5:
                # Draw the up button
                up1 = self.graphics.up_button1.draw(up1, self.graphics.mousePosition)
                # Check if up button is pressed and increment depth if it is
                if up1:
                    self.depth1 +=1

            
            if self.depth1 > 1:
                # Draw the down button
                down1 = self.graphics.down_button1.draw(down1, self.graphics.mousePosition)
                # Check if down button is pressed and decrement depth if it is
                if down1:
                    self.depth1 -=1

            # Print the current depth of player 1
            self.graphics.printValue(self.depth1, 30, 50, 493)

        # If player 2 is an AI, allow depth to be adjusted
        if not self.player2:
            # Hide the up and down buttons if the depth is at the maximum or minimum
            if self.depth2 < 5:
                # Draw the up button
                up2 = self.graphics.up_button2.draw(up2, self.graphics.mousePosition)
                # Check if up button is pressed and increment depth if it is
                if up2:
                    self.depth2 +=1

            if self.depth2 > 1:
                # Draw the down button
                down2 = self.graphics.down_button2.draw(down2, self.graphics.mousePosition)
                # Check if down button is pressed and decrement depth if it is
                if down2:
                    self.depth2 -=1

            # Print the current depth of player 2
            self.graphics.printValue(self.depth2, 30, 350, 493)

        # Draw cross if the buttons Endless and Random FM are activated
        if not self.player1 and not self.player2:
            self.graphics.printValue("Endless Loop", 20, 95, 570)
            if self.endless:
                self.endless = self.graphics.square_button2.draw(self.endless, self.graphics.mousePosition)
                self.graphics.drawCross(RED, [64,579], 17)
                self.graphics.printValue("Random FM", 20, 395, 570)
                if self.random_first_move:
                    self.random_first_move = self.graphics.square_button3.draw(self.random_first_move, self.graphics.mousePosition)
                    self.graphics.drawCross(RED, [364,579], 17)
                else:
                    self.random_first_move = self.graphics.square_button4.draw(self.random_first_move, self.graphics.mousePosition)
            else:
                self.endless = self.graphics.square_button.draw(self.endless, self.graphics.mousePosition)

        self.earlygame = self.graphics.startButton_button.draw(self.earlygame, self.graphics.mousePosition)
        # If the start button is pressed, start the early game and initialize the bots
        if self.earlygame:
            self.botRed = Bot(1,self.depth1)
            self.botBlue = Bot(2,self.depth2)

    #--------------------------------------------------------------------------------------------------------------------------------------------------
    #                                                                      EARLY GAME
    #--------------------------------------------------------------------------------------------------------------------------------------------------

    def earlyGame(self):
        if self.turnPlayer1:
            # Get the move from the bot
            if self.player1:
                coordinate = self.graphics.detectCercle(0)
            else:
                if self.round == 1:
                    if self.random_first_move:
                        coordinate = self.botRed.firstMove(self.gridC)
                    else:
                        coordinate = get_best_first_moves()[0]
                else:
                    move = self.botRed.minMax(self.gridC, self.listState)
                    coordinate = move[1]

            # Place the pion on the grid
            if coordinate is not None:
                self.turnPlayer1 = False
                self.gridC = place_pion(self.gridC, coordinate, 1)
                self.listMoves = addListMoves(self.listMoves ,self.round, 1, [[-1,-1],coordinate])
                self.addlistState(1)
                self.gridC.nb_pionsX -=1

                # Check if the player/bot has won
                if check_victory(self.gridC,1):
                    self.earlygame = False
                    self.gameover = True
            
            # Display the grid
            self.graphics.displayGrid()
        else:
            # Get the move from the player/bot
            if self.player2:
                coordinate = self.graphics.detectCercle(0)
            else:
                if self.round == 1:
                    if self.random_first_move:
                        coordinate = self.botBlue.firstMove(self.gridC)
                        print("random")
                    else:
                        coordinate = get_best_first_moves()[1]
                        print("best second move", coordinate)
                    
                else:
                    move = self.botBlue.minMax(self.gridC, self.listState)
                    coordinate = move[1]

            # Place the pion on the grid
            if coordinate is not None:
                self.turnPlayer1 = True
                self.listMoves = addListMoves(self.listMoves ,self.round, 2, [[-1,-1],coordinate])
                self.gridC = place_pion(self.gridC, coordinate, 2)
                self.addlistState(2)
                self.round+=1
                self.gridC.nb_pionsO -=1
                
                # If the round is greater than 4, start the middle game
                if self.round > 4:
                    self.earlygame = False
                    self.middlegame = True

                # Check if the player/bot has won
                if check_victory(self.gridC,2):
                    self.earlygame = False
                    self.middlegame = False
                    self.gameover = True

            # Display the grid
            self.graphics.displayGrid()

        # Save the mouse position
        self.graphics.mousePosition = (0,0)


    #--------------------------------------------------------------------------------------------------------------------------------------------------
    #                                                                      GAME
    #--------------------------------------------------------------------------------------------------------------------------------------------------

    def play(self):

        if self.turnPlayer1:
            # Display the grid
            self.graphics.displayGrid()
            # Get the move of the player or bot
            if self.player1:
                move = self.move_pion(1)
            else:
                move = self.botRed.minMax(self.gridC, self.listState)

            # play the move if it is not None
            if move is not None:
                self.turnPlayer1 = False
                self.round+=1
                self.gridC = modify_grid(self.gridC, move, 0, 1)
                self.listMoves = addListMoves(self.listMoves ,self.round-1, 1, move)
                self.addlistState(1)

                # Check if the player won
                if check_victory(self.gridC,1):
                    self.middlegame = False
                    self.gameover = True
            if not self.player1 and not self.player2:
                self.graphics.displayGrid()
        else:
            # Display the grid
            self.graphics.displayGrid()
            # Get the move of the player or bot
            if self.player2:
                move = self.move_pion(2)
            else:
                move = self.botBlue.minMax(self.gridC, self.listState)

            # play the move if it is not None
            if move is not None:
                self.turnPlayer1 = True
                self.round+=1
                self.gridC = modify_grid(self.gridC, move, 0, 2)
                self.listMoves = addListMoves(self.listMoves ,self.round-1, 2, move)
                self.addlistState(2)

                # Check if the player won
                if check_victory(self.gridC,2):
                    self.middlegame = False
                    self.gameover = True
            if not self.player1 and not self.player2:
                self.graphics.displayGrid()            

        # save the mouse position
        self.graphics.mousePosition = (0,0)

    #--------------------------------------------------------------------------------------------------------------------------------------------------
    #                                                                      GAME OVER
    #--------------------------------------------------------------------------------------------------------------------------------------------------

    def gameOver(self):
        # Display the grid and the game over script
        self.graphics.displayGrid()
        self.graphics.gameOverScript(not self.turnPlayer1)

        if not self.done:
            self.resultAndStats()
            update_table(not self.turnPlayer1, self.listMoves)
            self.done = True

        # Check if the player wants to restart the game
        self.earlygame = self.graphics.restartButton_button.draw(self.earlygame, self.graphics.mousePosition)

        # If the player wants to restart the game or he activated the endless mode, reset the game
        if self.earlygame or self.endless:
            self.earlygame = True
            self.reset()

    # reset the game
    def reset(self):
        # reset the list of moves and states
        self.listMoves = []
        self.listState = []
        # reset variables
        self.round = 1
        self.done = False
        self.gameover = False
        self.turnPlayer1 = True
        self.gridC.nb_pionsX = 4
        self.gridC.nb_pionsO = 4
        # reset the grid
        self.gridC.init_grid()
        # reset the stats
        self.botBlue.statsEarlyGame.resetAll()
        self.botBlue.statsMinimax.resetAll()
        self.botRed.statsEarlyGame.resetAll()
        self.botRed.statsMinimax.resetAll()

    #add a move to the list of moves
    def addlistState(self, player):

        red_pions = find_all_pions(self.gridC, 1)
        blue_pions = find_all_pions(self.gridC, 2)

        self.listState.append([player, red_pions, blue_pions])

    def resultAndStats(self):

        AvgTimeBEGP1 = AvgIterBEGP1 = AvgTimeBEGP2 = AvgIterBEGP2 = np.nan
        AvgTimeMBMGP1 = AvgIterMBMGP1 = AvgTimeMBMGP2 = AvgIterMBMGP2 = np.nan

        # Display stats of the bot 1
        if not self.player1:
            print("Stats player 1 :")
            print("Minimax stats :")
            self.botRed.statsMinimax.printStats()
            AvgTimeMBMGP1 = self.botRed.statsMinimax.getAvgTime()
            AvgIterMBMGP1 = self.botRed.statsMinimax.getAvgIter()
                
        # Display stats of the bot 2
        if not self.player2:
            print("Stats player 2 :")
            print("Minimax stats :")
            self.botBlue.statsMinimax.printStats()
            AvgTimeMBMGP2 = self.botBlue.statsMinimax.getAvgTime()
            AvgIterMBMGP2 = self.botBlue.statsMinimax.getAvgIter()
                
        # Save stats to a file
        save_stats(
            self.listMoves, self.round, not self.turnPlayer1, self.player1, self.player2, self.depth1, self.depth2,
            AvgTimeBEGP1, AvgIterBEGP1, AvgTimeBEGP2, AvgIterBEGP2,
            AvgTimeMBMGP1, AvgIterMBMGP1, AvgTimeMBMGP2, AvgIterMBMGP2
            )

    #--------------------------------------------------------------------------------------------------------------------------------------------------
    #                                                                   HUMAN MOVE A PION
    #--------------------------------------------------------------------------------------------------------------------------------------------------

    def move_pion(self,team_number):
        cancel = None
        newCoordinate = None

        # detect if the player clicked on a pion
        if self.graphics.firstCoordinate:
            self.graphics.oldCoordinate = self.graphics.detectCercle(team_number)   
        else:
            newCoordinate = self.graphics.detectCercle(0)
            if newCoordinate == None:
                cancel = self.graphics.detectCercle(team_number)

        # if the player clicked on a pion, draw a circle around it
        if self.graphics.oldCoordinate is not None:
            self.graphics.firstCoordinate = False
            self.graphics.draw_circle(team_number, (abscisse[self.graphics.oldCoordinate[1]], ordonnee[self.graphics.oldCoordinate[0]]), 5)
            list = list_all_possibles_moves(self.gridC,team_number)
            for move in list:
                if move[0] == self.graphics.oldCoordinate:
                    self.graphics.draw_empty_circle(team_number, (abscisse[move[1][1]], ordonnee[move[1][0]]), -10)

        # if the player clicked on a new coordinate, check if the move is possible
        if newCoordinate is not None:
            list = list_all_possibles_moves(self.gridC,team_number)
            move = [self.graphics.oldCoordinate,newCoordinate]
            self.graphics.firstCoordinate = True
            self.graphics.oldCoordinate = None
            if move in list:
                return move

        # if the player clicked on the same pion, cancel the move
        if cancel is not None and cancel == self.graphics.oldCoordinate:
            self.graphics.firstCoordinate = True
            self.graphics.oldCoordinate = None