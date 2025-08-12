# server.py

import socket
import threading
from utils import create_board, check_win, is_draw

HOST = '0.0.0.0'
PORT = 9999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(2)

print("Server started. Waiting for players...")

players = []
symbols = ['X', 'O']
board = create_board()

# Send board state to both players
def broadcast(msg):
    for player in players:
        player.send(msg.encode())

# Handle each player
def handle_player(player, index):
    global board
    player.send(f"You are Player {symbols[index]}\n".encode())

    while True:
        broadcast_board = ''.join(board)
        broadcast(f"BOARD:{broadcast_board}")

        if symbols[index] == current_turn[0]:
            player.send("Your turn. Enter position (0-8): ".encode())
            move = int(player.recv(1024).decode())

            if board[move] == ' ':
                board[move] = symbols[index]

                if check_win(board, symbols[index]):
                    broadcast_board = ''.join(board)
                    broadcast(f"BOARD:{broadcast_board}")
                    broadcast(f"Player {symbols[index]} wins!")
                    break

                elif is_draw(board):
                    broadcast(f"Draw!")
                    break

                current_turn[0] = symbols[1 - index]  # switch turns
            else:
                player.send("Invalid move. Try again.\n".encode())

# Accept players and start game
current_turn = ['X']
while len(players) < 2:
    conn, addr = server.accept()
    print(f"Player connected: {addr}")
    players.append(conn)

for idx, player in enumerate(players):
    threading.Thread(target=handle_player, args=(player, idx)).start()
