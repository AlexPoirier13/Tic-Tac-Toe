import pygame
import sys
import time


class Button:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    
    def draw(self, screen, text) -> None:
        #création d'un button play

        ##création du rectangle

        

        button_rect = pygame.Rect(self.x, self.y, self.width, self.height)

        button_color = (60, 140, 255)

        pygame.draw.rect(screen, button_color, button_rect, border_radius=12)        



        ##création du texte "play"

        text_play = pygame.font.Font("font\PressStart2P-Regular.ttf", 24)
        text_play = text_play.render(text, True, (230, 230, 255))

        text_play_rect = text_play.get_rect(center=button_rect.center)
        screen.blit(text_play, text_play_rect)
        
    
    def click(self,x_click,y_click) -> bool:
        
        return self.x <= x_click <= self.x + self.width and self.y <= y_click <= self.y + self.height
            

class Game:

    def __init__(self, width = 800, height = 600):
        
        self.width = width
        self.height = height
        self.main_color = (4, 7, 56)
        self.line_size = 4
        self.state = ""
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.running = True
        
        self.min_side = min(self.width, self.height) - self.width // 4
        
        #print(self.min_side)

        self.cell_size = self.min_side // 3

        #offset
        self.offset_x = (self.width - self.min_side) // 2
        self.offset_y = (self.height - self.min_side) // 2

        self.turn = 0
        self.grid = [["","",""],["","",""],["","",""]] #la grille
        self.grid_coords = [[[],[],[]], 
                            [[],[],[]], 
                            [[],[],[]]]
        

        pygame.init()
        pygame.display.set_caption("Tic-tac-toe")


    def main_menu(self):
        self.screen.fill(self.main_color)

        #création titre tic tac toe en haut de l'écran

        police_title = pygame.font.Font("font\PressStart2P-Regular.ttf", 48)

        text = police_title.render("Tic-Tac-Toe", True, (230, 230, 255)) 
        shadow_text = police_title.render("Tic-Tac-Toe", True, (0, 0, 0))


        text_rect = text.get_rect(center=(self.width//2, self.height//10))
        shadow_rect = text_rect.copy()
        shadow_rect.x += 6
        shadow_rect.y += 6


        
        self.screen.blit(shadow_text, shadow_rect)
        self.screen.blit(text, text_rect)



        #création d'un button play

        ##création du rectangle

        button_width = self.width * 0.35
        button_height = self.height * 0.125
        button_x = (self.width - button_width) // 2
        button_y = (self.height - button_height) // 2

        button_play = Button(button_x, button_y, button_width, button_height)

        button_play.draw(self.screen, "Play")

        self.main_menu_buttons = button_play

        

    def end_menu(self):
        print("Game Over")

        self.screen.fill(self.main_color)

        self.update_display_state()

        #Play again button
        button_width = self.width * 0.35
        button_height = self.height * 0.125
        pg_button_x = (self.width - button_width) // 2
        pg_button_y = (self.height - button_height) // 2

        self.play_again_button = Button(pg_button_x, pg_button_y, button_width, button_height)

        self.play_again_button.draw(self.screen, "Play again")

        #Quit button

        quit_button_x = (self.width - button_width) // 2
        quit_button_y = (self.height - button_height) * 4/5

        self.quit_button = Button(quit_button_x, quit_button_y, button_width, button_height)

        self.quit_button.draw(self.screen, "Quit")

        


        
        

    """
    return 0 si c'est au tour du joueur X
    return 1 si c'est au tour du joueur O
    """  
    def player_turn(self) -> int:
        if self.turn%2 == 0:
            return 0
        return 1

    def update_display_state(self):
        police_title = pygame.font.Font("font\PressStart2P-Regular.ttf", 24)

        text = police_title.render(self.state, True, (230, 230, 255)) 
        shadow_text = police_title.render(self.state, True, (0, 0, 0))


        text_rect = text.get_rect(center=(self.width//2, self.height//12))
        shadow_rect = text_rect.copy()
        shadow_rect.x += 6
        shadow_rect.y += 6

        padding = 10
        clear_rect = text_rect.inflate(padding, padding)
        self.screen.fill(self.main_color, clear_rect)
        
        self.screen.blit(shadow_text, shadow_rect)
        self.screen.blit(text, text_rect)


    def draw_grid(self):
        for i in range(1, 3):
            x = self.offset_x + i * self.cell_size
            y = self.offset_y + i * self.cell_size

        
            pygame.draw.line(self.screen, (255, 255, 255), (x, self.offset_y), (x, self.min_side + self.offset_y), self.line_size)
            pygame.draw.line(self.screen, (255, 255, 255), (self.offset_x, y), (self.min_side + self.offset_x, y), self.line_size)

    def fill(self):
        for i in range(len(self.grid_coords)):
            for j in range(len(self.grid_coords[i])):
                self.grid_coords[i][j].append([(self.offset_x + self.line_size*2 + self.cell_size * i, self.offset_y + self.line_size*2 + self.cell_size * j), (self.offset_x + self.cell_size - self.line_size*2 + self.cell_size * i, self.offset_y + self.cell_size - self.line_size*2 + self.cell_size * j)])
        #print(self.grid_coords)

    

    def set(self):
        x, y = pygame.mouse.get_pos()
        
        col = (x - self.offset_x) // self.cell_size
        row = (y - self.offset_y) // self.cell_size
        
        legal_click = True

        if col < 0 or col > 2 or row < 0 or row > 2 or self.grid[col][row] != "":
            legal_click = False

        #print(row, col)
    

        if not legal_click:
            print("You can't play on this cell, please choose another one or you clicked outside the grid")
        
        else:

            if self.turn % 2 == 0: #si pair alors c'est au joueur 1 ("X") de jouer sinon au joueur 2 ("O"), ici col = x et row = y
                pos1 = self.grid_coords[col][row][0][0]
                pos4 = self.grid_coords[col][row][0][1]
                pos2 = (pos4[0], pos1[1])
                pos3 = (pos1[0], pos4[1])
                pygame.draw.line(self.screen, (0,0,255), pos1, pos4, 6)
                pygame.draw.line(self.screen, (0,0,255), pos2, pos3, 6)
                self.grid[col][row] = "X"
                
                
                
            else:
                center_x = (self.grid_coords[col][row][0][0][0] + self.grid_coords[col][row][0][1][0]) // 2
                center_y = (self.grid_coords[col][row][0][0][1] + self.grid_coords[col][row][0][1][1]) // 2

                pygame.draw.circle(self.screen, (255,0,0), (center_x, center_y), self.cell_size // 2 - self.line_size, 6)
                self.grid[col][row] = "O"
                

            self.turn += 1

            

    
    def grid_to_tuple(self):
        x,o = 0,0

        for l in range(len(self.grid)):
            for c in range(len(self.grid[l])):
                if self.grid[l][c] == "X":
                    x += 2**(3*l + c)
                elif self.grid[l][c] == "O":
                    o += 2**(3*l + c)
        
        return (x,o)
        

    #return 0 si joueur X gagne
    #return 1 si joueur O gagne
    #return 2 si égalité
    #return 3 si la partie n'est pas encore terminée
    def endgame(self): 
        x,o = self.grid_to_tuple()
        
        if x+o == 511:
            return 2


        a = 1+2+4 #ligne
        b = 1+8+64 #colonne
        c = 1+16+256 #diagonale 1
        d = 4+16+64 #diagonale 2

        for _ in range(3):
            if x & a == a or x & b == b:
                return 0
            elif o & a == a or o & b == b:
                return 1
            a = a * 8 #on passe à la ligne suivante
            b = b * 2 #on passe à la colonne suivante
        
        if x & c == c or x & d == d:
            return 0
        if o & c == c or o & d == d:
            return 1
        
        return 3
        
    """
    remet la grille à 0
    """
    def reset(self):
        self.turn = 0
        self.grid = [["","",""],["","",""],["","",""]]
        self.grid_coords = [[[],[],[]], 
                            [[],[],[]], 
                            [[],[],[]]]
        



    def run(self):
        
        etat = self.endgame()
    
        menu_active = True
        game_active = False
        end_menu_active = False

        while self.running:
            if menu_active:
                self.main_menu()

                for event in pygame.event.get():


                    if event.type == pygame.QUIT:
                        self.running = False
                    

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1: #si c'est un clique gauche
                            x,y = pygame.mouse.get_pos()
                            if self.main_menu_buttons.click(x,y):
                                print("Play button clicked")
                                menu_active = False
                                self.screen.fill(self.main_color)
                                self.draw_grid()
                                self.fill()
                                game_active = True
                                print("Au tour du joueur X de jouer")
            
                pygame.display.flip()

            elif game_active:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        self.set()
                        pygame.display.flip()   
                        etat = self.endgame()
                    
                    if etat == 0:
                        print("Joueur X a gagné la partie")
                        self.state = "Joueur X a gagné la partie"
                        game_active = False
                        end_menu_active = True
                        time.sleep(2)
                        
                    elif etat == 1:
                        print("Joueur O a gagné la partie")
                        game_active = False
                        self.state = "Joueur O a gagné la partie"
                        end_menu_active = True
                        time.sleep(2)
                        
                    elif etat == 2:
                        print("Partie nulle")
                        self.state = "Egalité"
                        game_active = False
                        end_menu_active = True
                        time.sleep(2)
                        


                        

                    else:
                        turn = self.player_turn()
                        if turn == 0:
                            self.state = "Au tour du joueur X de jouer"
                        else:
                            self.state = "Au tour du joueur O de jouer"
                    self.update_display_state()
                    
                pygame.display.flip() 

            elif end_menu_active:
                self.end_menu()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        x,y = pygame.mouse.get_pos()
                        if self.play_again_button.click(x,y):
                            print("Play again button clicked")
                            self.reset()
                            etat = self.endgame()
                            self.screen.fill(self.main_color)
                            self.draw_grid()
                            self.fill()
                            self.state = "Au tour du joueur X de jouer"
                            self.update_display_state()
                            game_active = True
                            end_menu_active = False
                            
                        
                        elif self.quit_button.click(x,y):
                            print("Quit button clicked")
                            self.running = False

                pygame.display.flip()    


        pygame.quit()
        sys.exit()


                
            



test = Game()

test.run()