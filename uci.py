import sys
from board import create_board
from moves import make_move
from engine import choose_move_iterative
import moves
import zobrist
current_color = "white"
board = create_board()
def uci_to_square(uci_str):
    col = ord(uci_str[0]) - ord('a')
    row = 8 - int(uci_str[1])
    return (row, col)

def parse_move(move_str):
    start = uci_to_square(move_str[0:2])
    end = uci_to_square(move_str[2:4])
    promotion = None
    if len(move_str) == 5:
        promo_map = {"q": "Queen", "r": "rook", "b": "bishop", "n": "knight"}
        promotion = promo_map.get(move_str[4])
    return (start, end, promotion)

def square_to_uci(square):
    col = chr(ord('a') + square[1])
    row = 8 - square[0]
    return f"{col}{row}"

while True:
    command = input().strip()
    if command == "uci":
        print("id name MyEngine", flush=True)
        print("id author Malte", flush=True)
        print("uciok", flush=True)
    elif command == "isready":
        print("readyok", flush=True)
    elif command == "quit":
        break
    elif command.startswith("position"):
        parts = command.split()
        board = create_board()
        current_color = "white"
        moves.white_short = True
        moves.white_long = True
        moves.black_short = True
        moves.black_long = True
        moves.last_move = None
        moves.current_hash = zobrist.compute_hash(board, "white")
        moves.position_history = {moves.current_hash: 1}
        moves.halfmove_clock = 0
        import engine
        engine.transsquare_table.clear()
        if "moves" in parts:
            moves_index = parts.index("moves")
            move_strings = parts[moves_index + 1:]
            for move_str in move_strings:
                start, end, promotion = parse_move(move_str)
                make_move(board, start, end, promotion_piece=promotion)
                current_color = "black" if current_color == "white" else "white"
    elif command.startswith("go"):
        move = choose_move_iterative(board, current_color)
        if move is not None:
            start_square, end_square, promo = move
            piece = board[start_square[0]][start_square[1]]
            uci_move = square_to_uci(start_square) + square_to_uci(end_square)
            if piece == "B" and end_square[0] == 0:
                uci_move += "q"
            if piece == "-B" and end_square[0] == 7:
                uci_move += "q"
            print(f"bestmove {uci_move}", flush=True)
