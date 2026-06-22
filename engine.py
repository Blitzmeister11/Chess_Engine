from board import create_board
from moves import *
import zobrist
import moves
import time
piece_square_table_knight = [
    [-50,-40,-30,-30,-30,-30,-40,-50],
    [-40,-20,+0,+0,+0,+0,-20,-40],
    [-30,+0,+10,+15,+15,+10,+0,-30],
    [-30,+5,+15,+20,+20,+15,+5,-30],
    [-30,+5,+15,+20,+20,+15,+5,-30],
    [-30,+0,+10,+15,+15,+10,+0,-30],
    [-40,-20,+0,+0,+0,+0,-20,-40],
    [-50,-40,-30,-30,-30,-30,-40,-50]
]
piece_square_table_bishop = [
    [-20,-10,-10,-10,-10,-10,-10,-20],
    [-10,+0,+0,+0,+0,+0,+0,-10],
    [-10,+0,+5,+10,+10,+5,+0,-10],
    [-10,+5,+5,+10,+10,+5,+5,-10],
    [-10,+0,+10,+10,+10,+10,+0,-10],
    [-10,+10,+10,+10,+10,+10,+10,-10],
    [-10,+5,+0,+0,+0,+0,+5,-10],
    [-20,-10,-10,-10,-10,-10,-10,-20],
]
piece_square_table_rook = [
    [+0,+0,+0,+0,+0,+0,+0,+0],
    [+5,+10,+10,+10,+10,+10,+10,+5],
    [-5,+0,+0,+0,+0,+0,+0,-5],
    [-5,+0,+0,+0,+0,+0,+0,-5],
    [-5,+0,+0,+0,+0,+0,+0,-5],
    [-5,+0,+0,+0,+0,+0,+0,-5],
    [-5,+0,+0,+0,+0,+0,+0,-5],
    [+0,+0,+0,+5,+5,+0,+0,+0]
]
piece_square_table_queen = [
    [-20,-10,-10,-5,-5,-10,-10,-20],
    [-10,+0,+0,+0,+0,+0,+0,+10],
    [-10,+0,+5,+5,+5,+5,+0,-10],
    [-5,+0,+5,+5,+5,+5,+0,-5],
    [+0,+0,+5,+5,+5,+5,+0,-5],
    [-10,+5,+5,+5,+5,+5,+5,-10],
    [-10,+0,+5,+0,+0,+0,+0,-10],
    [-20,-10,-10,-5,-5,-10,-10,-20]
]
piece_square_table_pawn = [
    [+0,+0,+0,+0,+0,+0,+0,+0],
    [+5,+5,+5,+5,+5,+5,+5,+5],
    [+10,+10,+20,+30,+30,+20,+10,+10],
    [+5,+5,+10,+25,+25,+10,+5,+5],
    [+0,+0,+0,+20,+20,+0,+0,+0],
    [-5,-10,-15,+0,+0,-15,-10,-5],
    [+5,+10,+10,-20,-20,+10,+10,+5],
    [+0,+0,+0,+0,+0,+0,+0,+0]
]
piece_square_table_king = [
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-20,-30,-30,-40,-40,-30,-30,-20],
    [-10,-20,-20,-20,-20,-20,-20,-10],
    [+20,+20,+0,+0,+0,+0,+20,+20],
    [+20,+30,+5,+0,+0,+5,+30,+20]
]
piece_score = {
        "B": 1,
        "-B": 1,
        "L": 3,
        "-L": 3,
        "S": 3,
        "-S": 3,
        "T": 5,
        "-T": 5,
        "D": 9,
        "-D": 9,
        "K": 0,
        "-K":0
}
transsquare_table = {}
SEARCH_START = 0
SEARCH_LIMIT = 0
board = create_board()
def all_moves(board):
    all_moves = []
    for row in range(8):
        for col in range(8):
            felder = []
            if "-" in board[row][col]:
                if board[row][col] == "-D":
                    square = (row, col)
                    felder = queen_moves(board, square)
                if board[row][col] == "-T":
                    square = (row, col)
                    felder = rook_moves(board, square)
                if board[row][col] == "-L":
                    square = (row, col)
                    felder = bishop_moves(board, square)
                if board[row][col] == "-S":
                    square = (row, col)
                    felder = knight_moves(board, square)
                if board[row][col] == "-B":
                    square = (row, col)
                    felder = pawn_moves(board, square, "black", last_move)
                if board[row][col] == "-K":
                    square = (row, col)
                    felder = king_moves(board, square)
                for target in felder:
                    all_moves.append((square, target))
    prev_last_move = moves.last_move
    for zug in all_moves[:]:
        start, target = zug
        piece = board[start[0]][start[1]]
        target_inhalt = board[target[0]][target[1]]
        board[target[0]][target[1]] = piece
        board[start[0]][start[1]] = "0"
        possible = in_check(board, "black")
        if possible == True:
            all_moves.remove(zug)
        board[start[0]][start[1]] = piece
        board[target[0]][target[1]] = target_inhalt
        moves.last_move = prev_last_move

    return all_moves

def all_moves_white(board):
    all_moves = []
    for row in range(8):
        for col in range(8):
            felder = []
            if "-" not in board[row][col] and board[row][col] != "0":
                if board[row][col] == "D":
                    square = (row, col)
                    felder = queen_moves(board, square)
                if board[row][col] == "T":
                    square = (row, col)
                    felder = rook_moves(board, square)
                if board[row][col] == "L":
                    square = (row, col)
                    felder = bishop_moves(board, square)
                if board[row][col] == "S":
                    square = (row, col)
                    felder = knight_moves(board, square)
                if board[row][col] == "B":
                    square = (row, col)
                    felder = pawn_moves(board, square, "white", last_move)
                if board[row][col] == "K":
                    square = (row, col)
                    felder = king_moves(board, square)
                for target in felder:
                    all_moves.append((square, target))
    prev_last_move = moves.last_move
    for zug in all_moves[:]:
        start, target = zug
        piece = board[start[0]][start[1]]
        target_inhalt = board[target[0]][target[1]]
        board[target[0]][target[1]] = piece
        board[start[0]][start[1]] = "0"
        possible = in_check(board, "white")
        if possible == True:
            all_moves.remove(zug)
        board[start[0]][start[1]] = piece
        board[target[0]][target[1]] = target_inhalt
        moves.last_move = prev_last_move

    return all_moves

def bewerte_material(board):
    material = 0
    for row in range(8):
        for col in range(8):
            if board[row][col] == "B":
                material -= 1
                material -= piece_square_table_pawn[row][col] / 100
            if board[row][col] == "-B":
                material += 1
                material += piece_square_table_pawn[7 - row][col] / 100
            if board[row][col] == "L":
                material -= 3
                material -= piece_square_table_bishop[row][col] / 100
            if board[row][col] == "-L":
                material += 3
                material += piece_square_table_bishop[7- row][col] / 100
            if board[row][col] == "S":
                material -= 3
                material -= piece_square_table_knight[row][col] / 100
            if board[row][col] == "-S":
                material += 3
                material += piece_square_table_knight[7 - row][col] / 100
            if board[row][col] == "T":
                material -= 5
                material -= piece_square_table_rook[row][col] / 100
            if board[row][col] == "-T":
                material += 5
                material += piece_square_table_rook[7 - row][col] / 100
            if board[row][col] == "D":
                material -= 9
                material -= piece_square_table_queen[row][col] / 100
            if board[row][col] == "-D":
                material += 9
                material += piece_square_table_queen[7 - row][col] / 100
            if board[row][col] == "K":
                material -= piece_square_table_king[row][col] / 100
                white_king_pos = (row, col)
            if board[row][col] == "-K":
                material += piece_square_table_king[7 - row][col] / 100
                black_king_pos = (row, col)

    return material

def choose_move(board, color, depth=5):
    capture_moves = []
    quiet_moves = []
    alpha = -1000
    beta = 1000

    old_white_short = moves.white_short
    old_white_long = moves.white_long
    old_black_short = moves.black_short
    old_black_long = moves.black_long
    prev_last_move = moves.last_move

    zobrist_hash = moves.current_hash
    history = dict(moves.position_history)
    halfmove_clock = moves.halfmove_clock

    moves_list = all_moves(board) if color == "black" else all_moves_white(board)
    if not moves_list:
        return None

    for zug in moves_list:
        start, target = zug
        if board[target[0]][target[1]] != "0":
            capture_moves.append(zug)
        else:
            quiet_moves.append(zug)
    moves_list = capture_moves + quiet_moves

    moves_list.sort(key=lambda zug: score(board, zug[0], zug[1], color), reverse=True)

    best_move = None
    best_score = -9999999

    for zug in moves_list:
        start, target = zug
        piece = board[start[0]][start[1]]
        target_inhalt = board[target[0]][target[1]]

        board[target[0]][target[1]] = piece
        board[start[0]][start[1]] = "0"

        new_hash = zobrist_hash
        new_hash ^= zobrist.ZOBRIST_TABLE[(start[0], start[1], piece)]
        if target_inhalt != "0":
            new_hash ^= zobrist.ZOBRIST_TABLE[(target[0], target[1], target_inhalt)]
        new_hash ^= zobrist.ZOBRIST_TABLE[(target[0], target[1], piece)]
        new_hash ^= zobrist.ZOBRIST_TURN
        new_halfmove = 0 if piece in ("B", "-B") or target_inhalt != "0" else halfmove_clock + 1
        history[new_hash] = history.get(new_hash, 0) + 1

        next_color = "white" if color == "black" else "black"
        evaluation = negamax(board, depth - 1, next_color, -beta, -alpha, new_hash, history, new_halfmove)
        evaluation = -evaluation

        history[new_hash] -= 1
        if history[new_hash] == 0:
            del history[new_hash]

        if evaluation > best_score:
            best_score = evaluation
            best_move = zug
            alpha = best_score

        board[start[0]][start[1]] = piece
        board[target[0]][target[1]] = target_inhalt
        moves.white_short = old_white_short
        moves.white_long = old_white_long
        moves.black_short = old_black_short
        moves.black_long = old_black_long
        moves.last_move = prev_last_move

    return best_move



def negamax(board, tiefe, color, alpha, beta, zobrist_hash, history, halfmove_clock):
    if halfmove_clock >= 100:
        return 0
    if history.get(zobrist_hash, 0) >= 3:
        return 0
    if tiefe == 0:
        return quiescence(board, alpha, beta, color)
    if time.time() - SEARCH_START > SEARCH_LIMIT:
        return alpha
    if color == "black":
        moves_list = all_moves(board)
    else:
        moves_list = all_moves_white(board)

    if moves_list == []:
        if in_check(board, color) == True:
            return -1000 - tiefe
        return 0

    prev_last_move = moves.last_move
    old_white_short = moves.white_short
    old_white_long = moves.white_long
    old_black_short = moves.black_short
    old_black_long = moves.black_long

    capture_moves = []
    quiet_moves = []
    for zug in moves_list:
        start, target = zug
        if not board[target[0]][target[1]] == "0":
            capture_moves.append(zug)
        else:
            quiet_moves.append(zug)
    moves_list = capture_moves + quiet_moves

    best_score = -9999999
    for zug in moves_list:
        start, target = zug
        piece = board[start[0]][start[1]]
        target_inhalt = board[target[0]][target[1]]
        board[target[0]][target[1]] = piece
        board[start[0]][start[1]] = "0"

        new_hash = zobrist_hash
        new_hash ^= zobrist.ZOBRIST_TABLE[(start[0], start[1], piece)]
        if target_inhalt != "0":
            new_hash ^= zobrist.ZOBRIST_TABLE[(target[0], target[1], target_inhalt)]
        new_hash ^= zobrist.ZOBRIST_TABLE[(target[0], target[1], piece)]
        new_hash ^= zobrist.ZOBRIST_TURN

        new_halfmove = 0 if piece in ("B", "-B") or target_inhalt != "0" else halfmove_clock + 1
        history[new_hash] = history.get(new_hash, 0) + 1

        next_color = "white" if color == "black" else "black"
        score_result = -negamax(board, tiefe - 1, next_color, -beta, -alpha, new_hash, history, new_halfmove)

        history[new_hash] -= 1
        if history[new_hash] == 0:
            del history[new_hash]

        board[start[0]][start[1]] = piece
        board[target[0]][target[1]] = target_inhalt
        moves.white_short = old_white_short
        moves.white_long = old_white_long
        moves.black_short = old_black_short
        moves.black_long = old_black_long
        moves.last_move = prev_last_move

        if score_result > best_score:
            best_score = score_result
        if score_result > alpha:
            alpha = score_result
        if alpha >= beta:
            break

    return best_score


def quiescence(board, alpha, beta, color, depth = 10):
    if time.time() - SEARCH_START > SEARCH_LIMIT:
        return alpha
    stand_pat = bewerte_material(board) if color == "black" else -bewerte_material(board)
    if depth <= 0:
        return stand_pat
    if stand_pat >= beta:
        return beta
    if alpha < stand_pat:
        alpha = stand_pat

    if color == "black":
        moves_list = all_moves(board)
    else:
        moves_list = all_moves_white(board)

    capture_moves = [zug for zug in moves_list if board[zug[1][0]][zug[1][1]] != "0"]

    prev_last_move = moves.last_move
    old_white_short = moves.white_short
    old_white_long = moves.white_long
    old_black_short = moves.black_short
    old_black_long = moves.black_long

    for zug in capture_moves:
        start, target = zug
        piece = board[start[0]][start[1]]
        target_inhalt = board[target[0]][target[1]]
        board[target[0]][target[1]] = piece
        board[start[0]][start[1]] = "0"

        next_color = "white" if color == "black" else "black"
        score_result = -quiescence(board, -beta, -alpha, next_color, depth - 1)

        board[start[0]][start[1]] = piece
        board[target[0]][target[1]] = target_inhalt
        moves.white_short = old_white_short
        moves.white_long = old_white_long
        moves.black_short = old_black_short
        moves.black_long = old_black_long
        moves.last_move = prev_last_move

        if score_result >= beta:
            return beta
        if score_result > alpha:
            alpha = score_result

    return alpha

def score(board, start, target, color):
    if board[target[0]][target[1]] != "0":
        return SEE(board, target, color)
    wert_start = piece_score.get(board[start[0]][start[1]], 0)
    wert_target = piece_score.get(board[target[0]][target[1]], 0)
    return wert_target - wert_start

def SEE(board,target,color):
    attackers = []
    for richtung in direction_straight:
        aktuelle_reihe = target[0]
        aktuelle_spalte = target[1]
        piece_gefunden = False
        while not piece_gefunden:
            neue_reihe = aktuelle_reihe + richtung[0]
            neue_spalte = aktuelle_spalte + richtung[1]
            if neue_reihe < 0 or neue_reihe > 7 or neue_spalte < 0 or neue_spalte > 7:
                piece_gefunden = True
                continue
            if color == "white":
                if board[neue_reihe][neue_spalte] == "-T" or board[neue_reihe][neue_spalte] == "-D":
                    piece_gefunden = True
                    attackers.append((neue_reihe, neue_spalte))
                if not board[neue_reihe][neue_spalte] == "0":
                    piece_gefunden = True
                    continue
            else:
                if board[neue_reihe][neue_spalte] == "T" or board[neue_reihe][neue_spalte] == "D":
                    piece_gefunden = True
                    attackers.append((neue_reihe, neue_spalte))
                if not board[neue_reihe][neue_spalte] == "0":
                    piece_gefunden = True
                    continue
            aktuelle_reihe = neue_reihe
            aktuelle_spalte = neue_spalte

    for richtung in direction_diagonal:
        aktuelle_reihe = target[0]
        aktuelle_spalte = target[1]
        piece_gefunden = False
        while not piece_gefunden:
            neue_reihe = aktuelle_reihe + richtung[0]
            neue_spalte = aktuelle_spalte + richtung[1]
            if neue_reihe < 0 or neue_reihe > 7 or neue_spalte < 0 or neue_spalte > 7:
                piece_gefunden = True
                continue
            if color == "white":
                if board[neue_reihe][neue_spalte] == "-L" or board[neue_reihe][neue_spalte] == "-D":
                    piece_gefunden = True
                    attackers.append((neue_reihe, neue_spalte))
                if not board[neue_reihe][neue_spalte] == "0":
                    piece_gefunden = True
                    continue
            else:
                if board[neue_reihe][neue_spalte] == "L" or board[neue_reihe][neue_spalte] == "D":
                    piece_gefunden = True
                    attackers.append((neue_reihe, neue_spalte))
                if not board[neue_reihe][neue_spalte] == "0":
                    piece_gefunden = True
                    continue
            aktuelle_reihe = neue_reihe
            aktuelle_spalte = neue_spalte

    for richtung in direction_Knight:
        neue_reihe = target[0] + richtung[0]
        neue_spalte = target[1] + richtung[1]
        if neue_reihe < 0 or neue_reihe > 7 or neue_spalte < 0 or neue_spalte > 7:
            continue
        if color == "white":
            if board[neue_reihe][neue_spalte] == "-S":
                attackers.append((neue_reihe, neue_spalte))
        if color == "black":
            if board[neue_reihe][neue_spalte] == "S":
                attackers.append((neue_reihe, neue_spalte))

    for richtung in direction_King:
        neue_reihe = target[0] + richtung[0]
        neue_spalte = target[1] + richtung[1]
        if neue_reihe < 0 or neue_reihe > 7 or neue_spalte < 0 or neue_spalte > 7:
            continue
        if color == "white":
            if board[neue_reihe][neue_spalte] == "-K":
                attackers.append((neue_reihe, neue_spalte))
        if color == "black":
            if board[neue_reihe][neue_spalte] == "K":
                attackers.append((neue_reihe, neue_spalte))
    if color == "white":
        if target[0] - 1 >= 0 and target[1] + 1 <= 7:
            if board[target[0] - 1][target[1] + 1] == "-B":
                attackers.append((target[0]-1, target[1]+1))
        if target[0] - 1 >= 0 and target[1] - 1 >= 0:
            if board[target[0] - 1][target[1] - 1] == "-B":
                attackers.append((target[0]-1, target[1]-1))
    if color == "black":
        if target[0] + 1 <= 7 and target[1] + 1 <= 7:
            if board[target[0] + 1][target[1] + 1] == "B":
                attackers.append((target[0]+1, target[1]+1))
        if target[0] + 1 <= 7 and target[1] - 1 >= 0:
            if board[target[0] + 1][target[1] - 1] == "B":
                attackers.append((target[0]+1, target[1]-1))
    weakest = None
    weakest_wert = 9999
    for angriff in attackers:
        wert = piece_score.get(board[angriff[0]][angriff[1]],0)
        if wert < weakest_wert:
            weakest_wert = wert
            weakest = angriff
    if weakest == None:
        return 0
    captured_value = piece_score.get(board[target[0]][target[1]],0)
    captured_piece = board[target[0]][target[1]]
    capturing_piece = board[weakest[0]][weakest[1]]
    board[target[0]][target[1]] = capturing_piece
    board[weakest[0]][weakest[1]] = "0"
    see_result = SEE(board,target, "black" if color == "white" else "white")
    board[target[0]][target[1]] = captured_piece
    board[weakest[0]][weakest[1]] = capturing_piece
    return max(0, captured_value - see_result)

def choose_move_iterative(board, color, max_depth=99, time_limit=180):
    global SEARCH_START, SEARCH_LIMIT
    SEARCH_START = time.time()
    SEARCH_LIMIT = time_limit

    best_move_overall = None
    last_depth_time = 0.01

    for depth in range(1, max_depth + 1):
        start = time.time()
        result = choose_move(board, color, depth)
        if result is None:
            break
        best_move_overall = result
        depth_time = time.time() - start
        if time.time() - SEARCH_START > SEARCH_LIMIT:
            break
        if depth_time > last_depth_time * 2.5:
            break
        if depth >= 3 and depth_time < 0.01:
            break
        last_depth_time = depth_time

    return best_move_overall