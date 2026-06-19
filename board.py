symbols= {
    "-T":"♜ ","-S":"♞ ","-L":"♝ ","-D":"♛ ","-K":"♚ ","-B":"♟ ",
    "T":"♖ ","S":"♘ ","L":"♗ ","D":"♕ ","K":"♔ ","B":"♙ ","0": "    "
}

def create_board():
    row_1 = ["T","S","L","D","K","L","S","T"]
    row_2 = ["B","B","B","B","B","B","B","B"]
    row_3 = ["0","0","0","0","0","0","0","0"]
    row_4 = ["0","0","0","0","0","0","0","0"]
    row_5 = ["0","0","0","0","0","0","0","0"]
    row_6 = ["0","0","0","0","0","0","0","0"]
    row_7 = ["-B","-B","-B","-B","-B","-B","-B","-B"]
    row_8 = ["-T","-S","-L","-D","-K","-L","-S","-T"]

    rows = [row_8, row_7, row_6, row_5, row_4, row_3, row_2, row_1]

    return rows


def print_board(board):
    print()
    for index, row in enumerate(board):
        row_number = 8 - index
        print(row_number, end="  ")
        for square in row:
            print(symbols[square], end="  ")
        print()
    print("   a    b    c    d   e    f    g    h")