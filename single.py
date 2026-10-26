import pygame
import random

pygame.init()

WIDTH = 500
HEIGHT = 500
mode = "x" if round(random.randint(0,1)) == 1 else "o"
turn = True if mode == "x" else False
win = 0 # 0 - NONE, 1 - X, 2 - O, 3 - tie
robots_choise = {
    "row": 0,
    "col": 0
    }

display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(f"Tic-Tac-Toe (Te vagy az [{mode.upper()}] !)")

# table[0][0] = 0,1,2 - 0 = semmi, 1 = X, 2 = O
table = [[0 for i in range(3)] for i in range(3)]
table_rect = [[pygame.Rect(0,i*169, WIDTH/3-4, HEIGHT/3-4), pygame.Rect(WIDTH/3+4, i*169, WIDTH/3-4, HEIGHT/3-4), pygame.Rect(WIDTH-WIDTH/3+5, i*169, WIDTH/3-4, HEIGHT/3-4)] for i in range(3)]

def draw(typein:str, x:int,y:int):
    if typein == "o":
        kor = pygame.font.Font(pygame.font.get_default_font(), 200).render(f"O", True, (255,0,0))
        kor_rect = kor.get_rect()
        kor_rect.centerx = x+80
        kor_rect.centery = y+90
        display.blit(kor, kor_rect)
    else:
        iksz = pygame.font.Font(pygame.font.get_default_font(), 200).render(f"X", True, (0,0,255))
        iksz_rect = iksz.get_rect()
        iksz_rect.centerx = x+80
        iksz_rect.centery = y+90
        display.blit(iksz, iksz_rect)

running = True

def check(row:bool, col:int):
    if table[row][col] != 0:
        if table[row].count(0) == 0:
            check(row=round(random.randint(0,2)), col=col)
        else:
            check(row=row, col=round(random.randint(0,2)))
    else:
        robots_choise["row"] = row
        robots_choise["col"] = col
        return

while running:
    xdb = {0: [0 for i in range(3)], 1: [0 for i in range(3)], 2: [0 for i in range(3)]}
    odb = {0: [0 for i in range(3)], 1: [0 for i in range(3)], 2: [0 for i in range(3)]}
    ndb = 0
    for row in range(len(table)):
        if table[row].count(1) == 3 or table[row].count(2) == 3:
            win = 1 if table[row].count(1) == 3 else 2
            break
        else:
            for col in range(len(table[row])):
                    if table[row][col] == 1:
                        xdb[row][col] += 1
                    elif table[row][col] == 2:
                        odb[row][col] += 1

            ndb += table[row].count(0)

    if win == 0:
        if ndb == 0:
            win = 3
        else:
            if ((xdb[0][0]>= 1 and xdb[1][0]>= 1 and xdb[2][0]>=1) or (xdb[0][1]>= 1 and xdb[1][1]>= 1 and xdb[2][1]>=1) or (xdb[0][2]>= 1 and xdb[1][2]>= 1 and xdb[2][2]>=1)) or (xdb[0][0]>= 1 and xdb[1][1]>= 1 and xdb[2][2]>=1) or (xdb[0][2]>= 1 and xdb[1][1]>= 1 and xdb[2][0]>=1):
                win = 1
            elif ((odb[0][0]>= 1 and odb[1][0]>= 1 and odb[2][0]>=1) or (odb[0][1]>= 1 and odb[1][1]>= 1 and odb[2][1]>=1) or (odb[0][2]>= 1 and odb[1][2]>= 1 and odb[2][2]>=1)) or (odb[0][0]>= 1 and odb[1][1]>= 1 and odb[2][2]>=1) or (odb[0][2]>= 1 and odb[1][1]>= 1 and odb[2][0]>=1):
                win = 2
            


    if win != 0:
        pause = True

        while pause:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pause = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    win = 0
                    table = [[0 for i in range(3)] for i in range(3)]
                    mode = "x" if round(random.randint(0,1)) == 1 else "o"
                    turn = True if mode == "x" else False
                    pygame.display.set_caption(f"Tic-Tac-Toe (Te vagy az [{mode.upper()}] !)")
                    pause = False

            if win == 3:
                win_title = pygame.font.Font(pygame.font.get_default_font(), 32).render(f"Döntetlen!", True, (0, 255, 0))
            else:
                win_title = pygame.font.Font(pygame.font.get_default_font(), 32).render(f"Az {'X' if win == 1 else 'O'} nyert!", True, (0, 255, 0))
            win_title_rect = win_title.get_rect()
            win_title_rect.centerx = WIDTH/2
            win_title_rect.centery = HEIGHT/2-32

            win_subtitle = pygame.font.Font(pygame.font.get_default_font(), 32).render(f"Te voltál a [{mode.upper()}]!", True, (0,255,0))
            win_subtitle_rect = win_subtitle.get_rect()
            win_subtitle_rect.centerx = WIDTH/2
            win_subtitle_rect.centery = HEIGHT/2

            ct = pygame.font.Font(pygame.font.get_default_font(), 26).render("Nyomj egy [szóköz]-t a folytatáshoz!", True, (0,255,0))
            ct_rect = ct.get_rect()
            ct_rect.centerx = WIDTH/2
            ct_rect.centery = HEIGHT/2+26

            display.blit(ct, ct_rect)
            display.blit(win_subtitle, win_subtitle_rect)
            display.blit(win_title, win_title_rect)
            pygame.display.update()

    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            for i in range(len(table_rect[0])):
                for i2 in range(len(table_rect)):
                    if table_rect[i][i2].collidepoint(event.pos):
                        if table[i][i2] == 0 and turn:
                            table[i][i2] = 1 if mode == "x" else 2
                            turn = False

    if turn == False:   
        check(row=round(random.randint(0,2)), col=round(random.randint(0,2)))
        table[robots_choise["row"]][robots_choise["col"]] = 1 if mode == "o" else 2
        turn = True

    display.fill((255,255,255))
    pygame.draw.line(display, (0,0,0), (WIDTH/3, 0), (WIDTH/3, HEIGHT), 10)
    pygame.draw.line(display, (0,0,0), (WIDTH-WIDTH/3, 0), (WIDTH-WIDTH/3, HEIGHT), 10)
    pygame.draw.line(display, (0,0,0), (0, HEIGHT/3), (WIDTH, HEIGHT/3), 10)
    pygame.draw.line(display, (0,0,0), (0, HEIGHT-HEIGHT/3), (WIDTH, HEIGHT-HEIGHT/3), 10)
    
    for i in range(len(table[0])):
        for i2 in range(len(table)):
            if table[i][i2] != 0:
                if i2 == 0:
                    draw("x" if table[i][i2]==1 else "o", i2, i*169)
                elif i2 == 1:
                    draw("x" if table[i][i2]==1 else "o", WIDTH/3-4, i*169)
                else:
                    draw("x" if table[i][i2]==1 else "o", WIDTH-WIDTH/3-4, i*169)

    pygame.display.update()


pygame.quit()