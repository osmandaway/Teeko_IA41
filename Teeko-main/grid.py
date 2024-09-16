#Plusieurs fonctions relative à la grille
class Grid:
    def __init__(self,nb_pionsX,nb_pionsO):
        self.grid = [[0 for i in range(5)] for j in range(5)]
        self.nb_pionsX = nb_pionsX
        self.nb_pionsO = nb_pionsO

    def init_grid(self):
        for i in range(5):
            for j in range(5):
                self.grid[i][j] = 0

    #Affiche la grille
    def print_grid(self): 

        from colorama import Fore, Back, Style

        for i in range(self.nb_pionsX):
            print(Back.RED + Fore.WHITE + "1",end = " ")
        print(Style.RESET_ALL)

        #afficher toute la grille ligne par ligne 
        print(Back.GREEN + "--------------------------" + Style.RESET_ALL)
        print(Back.GREEN + "|X\Y|| 0 | 1 | 2 | 3 | 4 |" + Style.RESET_ALL)
        print(Back.GREEN + "--------------------------" + Style.RESET_ALL)
        for i in range(5):
            print(Back.GREEN + "| " + str(i), end = " |")
            for j in range(5):
                if self.grid[i][j] == 1:
                    print(Back.YELLOW + "|" + Back.RED + Fore.WHITE + " " + str(self.grid[i][j]), end=" ")
                elif self.grid[i][j] == 2:
                    print(Back.YELLOW + "|" + Back.BLUE + Fore.WHITE + " " + str(self.grid[i][j]), end=" ")
                else:
                    print(Back.YELLOW + "| " + str(self.grid[i][j]), end=" ")
                
            print(Back.YELLOW + "|" + Style.RESET_ALL)
            print(Back.GREEN + "-----" + Back.YELLOW + "---------------------" + Style.RESET_ALL)

        for i in range(self.nb_pionsO):
            print(Back.BLUE + Fore.WHITE + "2",end = " ")
        print(Style.RESET_ALL)