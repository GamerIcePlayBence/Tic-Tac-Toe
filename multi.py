import pygame
import socket
import threading
import ast

WIDTH = 500
HEIGHT = 500
turn = True
mode = ""
win = 0 # 0 - NONE, 1 - X, 2 - O, 3 - tie
# table[0][0] = 0,1,2 - 0 = semmi, 1 = X, 2 = O
table = []
socketing = True

response_e = threading.Event()

def sendmsg(msg:str):
    response_e.clear()
    sock.sendall((msg+"\n").encode("utf-8"))
    response_e.wait()


def recive_message(sock):
    global response_e

    while True:
        try:
            data = sock.recv(1024)

            if not data:
                break

            msg:str = data.decode('utf-8')

            if msg.startswith("win:"):
                global win
                win = int(msg.replace("win:", ""))

            elif msg.startswith("table:"):
                value = msg.replace("table:", "")
                global table
                #[[0, 0, 0], [0, 0, 0], [0, 0, 0]]
                table = ast.literal_eval(value)
                    

            elif msg.startswith("turn:"):
                global turn
                turn = msg.replace("turn:", "").strip().lower() == "true"

            elif msg.startswith("mode:"):
                global mode
                mode = msg.replace("mode:", "")

            response_e.set()
        
        except OSError:
            break

ip = input("Kérem a szerver ip címét! (A [localhost] is működik):\t")
if ip == "localhost":
    ip = socket.gethostbyname(socket.gethostname())

server_add = (ip, 5000)
print(f"Csatlakozás... ({server_add[0]}:{server_add[1]})")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    try:
        sock.connect(server_add)
        print("Sikeres csatlakozás!")

        threading.Thread(
            target=recive_message,
            args=(sock,),
            daemon=True
        ).start()


        while socketing:
            pygame.init()

            display = pygame.display.set_mode((WIDTH, HEIGHT))

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

            while running:             
                sendmsg("get table")
                sendmsg("get win")

                if mode == "":
                    sendmsg("get mode")
                    pygame.display.set_caption(f"Tic-Tac-Toe (Te vagy az [{mode.upper()}] !)")
                
                sendmsg(f"get turn {mode}")

                if win != 0:
                    pause = True

                    while pause:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                socketing = False
                                running = False
                                pause = False
                            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                                sendmsg("reset")
                                win = 0
                                table = []
                                mode = ""
                                turn = True
                                sendmsg("get table")
                                sendmsg("get win")
                                sendmsg("get mode")
                                sendmsg(f"get turn {mode}")

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
                        socketing = False
                        running = False
                    if event.type == pygame.MOUSEBUTTONUP:
                        for i in range(len(table_rect[0])):
                            for i2 in range(len(table_rect)):
                                if table_rect[i][i2].collidepoint(event.pos):
                                    if table[i][i2] == 0 and turn:
                                        sendmsg(f"place table {i} {i2} {mode}")
                                        sendmsg("get table")
                                        sendmsg(f"get turn {mode}")


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

    except OSError as e:
        print(f"Hiba: {e}")

sock.close()