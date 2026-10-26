import socket
import threading
import random

clients = []
mode = "x" if round(random.randint(0,1)) == 1 else "o" # x or o
win = 0 # 0 - NONE, 1 - X, 2 - O, 3 - tie
table = [[0 for i in range(3)] for i in range(3)] # table[0][0] = 0,1,2 - 0 = semmi, 1 = X, 2 = O
turn = "x"

def check_win():
    global win
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

def reset():
    global win,table,mode,turn
    win = 0
    table = [[0 for i in range(3)] for i in range(3)]
    mode = "x" if round(random.randint(0,1)) == 1 else "o"
    turn = "x"

def hadle_client(connect, client_add):
    global mode, win, table, turn
    print(f"[+] {client_add[0]}")
    clients.append(connect)

    try:
        while True:
            data = connect.recv(1024)

            if not data:
                break

            message:str = data.decode("utf-8").strip()
            print(f"[{client_add[0]}] {message}")

            if message == "get mode":
                connect.sendall(
                    f"mode:{mode}".encode("utf-8")
                )
                print(f"[SERVER]: mode:{mode}")

                mode = "x" if mode == "o" else "o"

            elif message == "get win":
                check_win()
                connect.sendall(
                    f"win:{win}".encode("utf-8")
                )
                print(f"[SERVER]: win:{win}")

            elif message.startswith("get turn"):
                connect.sendall(
                    f"turn:{True if turn == message[-1:] else False}".encode("utf-8")
                )
                print(f"[SERVER]: turn:{turn}")

            elif message == "get table":
                connect.sendall(
                    f"table:{table}".encode("utf-8")
                )
                
                print(f"[SERVER]: table:{table}")

            #place table 0 0 x/o
            elif message.startswith("place table"):
                table[int(message[-5:-4])][int(message[-3:-1])] = 1 if message[-1:] == "x" else 2
                turn = "o" if message[-1:] == "x" else "x"
                
                connect.sendall(
                    "Done place table".encode("utf-8")
                )
                
                print(f"table = {table}\nturn={turn}")

            elif message == "reset":
                if win != 0:
                    reset()
                connect.sendall(
                    "Done reset".encode("utf-8")
                )


    except OSError:
        pass

    finally:
        if connect in clients:
            clients.remove(connect)
        
        connect.close()
        print(f"[-] {client_add[0]}")

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_add = ("0.0.0.0", 5000)
sock.bind(server_add)
sock.listen()
print(f"Szerver elindult! ({server_add[0]}:{server_add[1]})")

while True:
    connect, client_add = sock.accept()

    threading.Thread(
        target=hadle_client,
        args=(connect, client_add),
        daemon=True
    ).start()
