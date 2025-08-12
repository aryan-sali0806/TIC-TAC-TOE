# client.py

import socket
from utils import print_board

HOST = 'localhost'  # or server IP
PORT = 9999

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

while True:
    data = client.recv(1024).decode()

    if not data:
        break  # connection closed

    if data.startswith("You are"):
        print(data)

    elif data.startswith("BOARD:"):
        board_data = list(data[6:])
        print_board(board_data)

    elif "Your turn" in data:
        print(data.strip())  # show the prompt
        move = input("Enter move (0-8): ").strip()
        client.send(move.encode())

    elif any(word in data for word in ["wins", "Draw", "draw", "Win"]):
        print(data.strip())
        break

    else:
        print(data.strip())  # for messages like "Invalid move"