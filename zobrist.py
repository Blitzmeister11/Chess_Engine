import random

PIECES = ["B", "-B", "S", "-S", "L", "-L", "T", "-T", "D", "-D", "K", "-K"]

random.seed(42)
ZOBRIST_TABLE = {}
for row in range(8):
    for col in range(8):
        for piece in PIECES:
            ZOBRIST_TABLE[(row, col, piece)] = random.getrandbits(64)

ZOBRIST_TURN = random.getrandbits(64)

def compute_hash(board, color):
    h = 0
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece != "0":
                h ^= ZOBRIST_TABLE[(row, col, piece)]
    if color == "black":
        h ^= ZOBRIST_TURN
    return h