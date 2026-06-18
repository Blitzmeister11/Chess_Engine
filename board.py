symbole = {
    "-T":"♜ ","-S":"♞ ","-L":"♝ ","-D":"♛ ","-K":"♚ ","-B":"♟ ",
    "T":"♖ ","S":"♘ ","L":"♗ ","D":"♕ ","K":"♔ ","B":"♙ ","0": "    "
}

def create_board():
    reihe_1 = ["T","S","L","D","K","L","S","T"]
    reihe_2 = ["B","B","B","B","B","B","B","B"]
    reihe_3 = ["0","0","0","0","0","0","0","0"]
    reihe_4 = ["0","0","0","0","0","0","0","0"]
    reihe_5 = ["0","0","0","0","0","0","0","0"]
    reihe_6 = ["0","0","0","0","0","0","0","0"]
    reihe_7 = ["-B","-B","-B","-B","-B","-B","-B","-B"]
    reihe_8 = ["-T","-S","-L","-D","-K","-L","-S","-T"]

    reihen = [reihe_8, reihe_7, reihe_6, reihe_5, reihe_4, reihe_3, reihe_2, reihe_1]

    return reihen


def print_board(board):
    print()
    for index, reihe in enumerate(board):
        reihenummer = 8 - index
        print(reihenummer, end="  ")
        for feld in reihe:
            print(symbole[feld], end="  ")
        print()
    print("   a    b    c    d   e    f    g    h")