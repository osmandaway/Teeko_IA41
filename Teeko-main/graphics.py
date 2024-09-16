
import pygame
from math import sqrt

SIZE = 30 #Rayon cercle pion
DELAY = 0.3 #Delais (en s) pour relancer le prog
SIZE_SCREEN = (600,780)

#Différentes couleurs
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
MARRON = (182, 106, 25)
GREY = (121,121,121)
BACKGROUND = (81,49,49)
#(81,49,49)(0,0,102)

# Dictionary to convert coordinates in pixels to coordinates in the grid
abscisse = {
    0 : 80,
    1 : 190,
    2 : 300,
    3 : 410,
    4 : 520,
    80 : 0,
    190 : 1,
    300 : 2,
    410 : 3,
    520 : 4
}

ordonnee = {
    0 : 180,
    1 : 290,
    2 : 400,
    3 : 510,
    4 : 620,
    180 : 0,
    290 : 1,
    400 : 2,
    510 : 3,
    620 : 4
}

class Graphics:
    def __init__(self, gridC):
        #Initialise Pygame
        pygame.init()

        #Initialise variable
        self.surface = pygame.display.set_mode(SIZE_SCREEN)
        pygame.display.set_caption("Teeko")

        self.bot_img = pygame.image.load('resources/botAI.png').convert_alpha()
        self.human_img = pygame.image.load('resources/human.png').convert_alpha()
        self.startButton_img = pygame.image.load('resources/startButton.png').convert_alpha()
        self.up_img = pygame.image.load('resources/up.png').convert_alpha()
        self.down_img = pygame.image.load('resources/down.png').convert_alpha()
        self.restart_img = pygame.image.load('resources/restartButton.png').convert_alpha()
        self.square_img = pygame.image.load('resources/square.png').convert_alpha()

        self.bot_button1 = Button(10,360, self.bot_img, 0.23, False, self.surface)
        self.human_button1 = Button(140,360, self.human_img, 0.23, True, self.surface)
        self.bot_button2 = Button(310,360, self.bot_img, 0.23, False, self.surface)
        self.human_button2 = Button(440,360, self.human_img, 0.23, True, self.surface)

        self.up_button1 = Button(10,470, self.up_img, 0.06, True, self.surface)
        self.down_button1 = Button(10,510, self.down_img, 0.06, True, self.surface)
        self.up_button2 = Button(310,470, self.up_img, 0.06, True, self.surface)
        self.down_button2 = Button(310,510, self.down_img, 0.06, True, self.surface)

        self.startButton_button = Button((SIZE_SCREEN[0]-0.3*self.startButton_img.get_rect().width)/2,620, self.startButton_img, 0.3, True, self.surface)
        self.restartButton_button = Button((SIZE_SCREEN[0]-0.3*self.restart_img.get_rect().width)/2,650, self.restart_img, 0.3, True, self.surface)
        self.square_button = Button(35,558, self.square_img, 0.1, True, self.surface)
        self.square_button2 = Button(35,558, self.square_img, 0.1, False, self.surface)
        self.square_button3 = Button(335,558, self.square_img, 0.1, False, self.surface)
        self.square_button4 = Button(335,558, self.square_img, 0.1, True, self.surface)

        self.mousePosition = (0,0)
        self.oldCoordinate = None
        self.firstCoordinate = True

        self.gridC = gridC

    def mainMenuScript(self):
        self.render_background()

        font = pygame.font.SysFont('lucidaconsole',50)
        font1 = pygame.font.SysFont('lucidaconsole',30)

        line0 = font.render(f"TEEKO", True, WHITE)
        self.surface.blit(line0, ((SIZE_SCREEN[0]-line0.get_rect().width)/2,100))

        line1 = font.render(f"MAIN MENU", True, WHITE)
        self.surface.blit(line1, ((SIZE_SCREEN[0]-line1.get_rect().width)/2,200))

        line2 = font1.render(f"Joueur 1 :", True, WHITE)
        self.surface.blit(line2, ((SIZE_SCREEN[0]-300-line2.get_rect().width)/2,300))

        line3 = font1.render(f"Joueur 2 :", True, WHITE)
        self.surface.blit(line3, ((SIZE_SCREEN[0]-300-line3.get_rect().width)/2+300,300))

    def gameOverScript(self, winnerP1):

        font1 = pygame.font.SysFont('lucidaconsole',30)

        if winnerP1:
            line2 = font1.render(f"The player Red win!!!", True, WHITE)
            self.surface.blit(line2, ((SIZE_SCREEN[0]-line2.get_rect().width)/2,50))

            line3 = font1.render(f"Blue, you're a looser", True, WHITE)
            self.surface.blit(line3, ((SIZE_SCREEN[0]-line3.get_rect().width)/2,100))
        else:
            line2 = font1.render(f"The player Blue win!!!", True, WHITE)
            self.surface.blit(line2, ((SIZE_SCREEN[0]-line2.get_rect().width)/2,50))

            line3 = font1.render(f"Red, you're a looser", True, WHITE)
            self.surface.blit(line3, ((SIZE_SCREEN[0]-line3.get_rect().width)/2,100))

    def printValue(self, value, size, Xcoordinate, Ycoordinate):
        font = pygame.font.SysFont('lucidaconsole',size)
        line = font.render(str(value), True, WHITE)
        self.surface.blit(line, (Xcoordinate, Ycoordinate))
        

    # Vérifie les inputs du clavier et de la souris
    def checkInput(self):
        for event in pygame.event.get():
                
            if pygame.mouse.get_pressed()[0]:
                self.mousePosition = pygame.mouse.get_pos()

            #Récupère les inputs du clavier
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    return False

            elif event.type == pygame.QUIT:
                return False
        return True
                

    # Met à jour l'écran
    def updateScreen(self):
        pygame.display.update()
    
    # Display le background
    def render_background(self):
        self.surface.fill(BACKGROUND)

    # Initialise et affiche la grille
    def init_grid(self):
        self.render_background()
        for i in range(5):
            for j in range(5):
                pygame.draw.circle(self.surface, GREEN, [80+i*110, 180+j*110], 40, 2)

        for i in range(4):
            for j in range(5):
                pygame.draw.line(self.surface, GREEN,[120+i*110, 180+j*110],[150+i*110, 180+j*110], 2)
                pygame.draw.line(self.surface, GREEN,[80+j*110, 220+i*110],[80+j*110, 250+i*110], 2)

        for i in range(4):
            for j in range(4):
                pygame.draw.line(self.surface, GREEN,[80+40*sqrt(2)/2+i*110, 180+40*sqrt(2)/2+j*110],[80-40*sqrt(2)/2+(i+1)*110, 180-40*sqrt(2)/2+(j+1)*110], 2)
                pygame.draw.line(self.surface, GREEN,[80+40*sqrt(2)/2+i*110, 180-40*sqrt(2)/2+(j+1)*110],[80-40*sqrt(2)/2+(i+1)*110, 180+40*sqrt(2)/2+j*110], 2)
    
    # Affiche les grands cercles lorsqu'on clique sur une case
    def draw_circle(self, team_number, coordinate, scale):
        if team_number == 1:
            pygame.draw.circle(self.surface, RED , coordinate, SIZE+scale)
        else:
            pygame.draw.circle(self.surface, BLUE , coordinate, SIZE+scale)

    # Affiche les cercles vides des cases où on peut jouer
    def draw_empty_circle(self, team_number, coordinate, scale):
        if team_number == 1:
            pygame.draw.circle(self.surface, RED , coordinate, SIZE+scale, 2)
        else:
            pygame.draw.circle(self.surface, BLUE , coordinate, SIZE+scale,2)

    # Fonction pour détecter les cercle
    def detectCercle(self, team_number):
        for i in range(5):
            for j in range(5):

                sqx = ((80+i*110) - self.mousePosition[0])**2
                sqy = ((180+j*110) - self.mousePosition[1])**2
                if sqrt(sqx + sqy) < SIZE:
                    if self.gridC.grid[j][i] == team_number:
                        return [j,i]

    # Affiche le plateau de jeu
    def displayGrid(self):
        self.init_grid()

        for i in range(self.gridC.nb_pionsX):
            pygame.draw.circle(self.surface, RED , (135+i*110,120), SIZE)

        for i in range(5):
            for j in range(5):
                if self.gridC.grid[i][j] == 1:
                    pygame.draw.circle(self.surface, RED , (abscisse[j], ordonnee[i]), SIZE)
                elif self.gridC.grid[i][j] == 2:
                    pygame.draw.circle(self.surface, BLUE , (abscisse[j], ordonnee[i]), SIZE)

        for i in range(self.gridC.nb_pionsO):
            pygame.draw.circle(self.surface, BLUE , (135+i*110,680), SIZE)

    # Affiche les croix pour le menu
    def drawCross(self, color, pos, width):
        pygame.draw.line(self.surface, color, (pos[0]-width, pos[1]-width), (pos[0]+width, pos[1]+width), 3)
        pygame.draw.line(self.surface, color, (pos[0]+width, pos[1]-width), (pos[0]-width, pos[1]+width), 3)

class Button():
    def __init__(self,x,y,image, scale, result, parent_surface):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.parent_surface = parent_surface
        
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False
        self.result = result
    
    def draw(self, action, pos):

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] and self.clicked == False:
                self.clicked = True
                action = self.result

        if not pygame.mouse.get_pressed()[0]:
            self.clicked = False

        self.parent_surface.blit(self.image, (self.rect.x, self.rect.y))

        if action == self.result:
            pygame.draw.rect(self.parent_surface, RED, self.rect, 3)

        return action