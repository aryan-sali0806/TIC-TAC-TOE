def create_board():
    return ['' for _ in range(9)]

def print_board(board):
    print()
    for i in range(3):
        print("|".join(board[i*3:(i+1)*3]))
        if i<2:
            print("---------")

    print()

def check_win(board,player):
    win_conditions = [ [0,1,2],[3,4,5],[6,7,8], #rows
                    [0,3,6],[1,4,7],[2,5,8],   #cols
                    [0,4,8],[2,4,6] ]          #diagonals
                    
    return any(all(board[i]==player for i in cond) for cond in win_conditions)

def is_draw(board):
    return all(cell!='' for cell in board)
