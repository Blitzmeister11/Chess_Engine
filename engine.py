from board import create_board
from moves import *
import moves
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
        möglich = in_check(board, "black")
        if möglich == True:
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
        möglich = in_check(board, "white")
        if möglich == True:
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
                material -= piece_square_table_pawn[row][col] / 50
            if board[row][col] == "-B":
                material += 1
                material += piece_square_table_pawn[7 - row][col] / 50
            if board[row][col] == "L":
                material -= 3
                material -= piece_square_table_bishop[row][col] / 50
            if board[row][col] == "-L":
                material += 3
                material += piece_square_table_bishop[7- row][col] / 50
            if board[row][col] == "S":
                material -= 3
                material -= piece_square_table_knight[row][col] / 50
            if board[row][col] == "-S":
                material += 3
                material += piece_square_table_knight[7 - row][col] / 50
            if board[row][col] == "T":
                material -= 5
                material -= piece_square_table_rook[row][col] / 20
            if board[row][col] == "-T":
                material += 5
                material += piece_square_table_rook[7 - row][col] / 20
            if board[row][col] == "D":
                material -= 9
                material -= piece_square_table_queen[row][col] / 20
            if board[row][col] == "-D":
                material += 9
                material += piece_square_table_queen[7 - row][col] / 20
            if board[row][col] == "K":
                material -= piece_square_table_king[row][col] / 20
            if board[row][col] == "-K":
                material += piece_square_table_king[7 - row][col] / 20

    return material

def choose_move(board):
    capture_moves = []
    quiet_moves = []
    tiefe = 5
    alpha = -1000
    beta = 1000
    old_white_short = moves.white_short
    old_white_long = moves.white_long
    old_black_short = moves.black_short
    old_black_long = moves.black_long
    prev_last_move = moves.last_move
    moves_list = all_moves(board)
    if moves_list == []:
        return None
    best_move = []
    best_score = -9999999
    for zug in moves_list:
        start, target = zug
        if not board[target[0]][target[1]] == "0":
            capture_moves.append(zug)
        else:
            quiet_moves.append(zug)
    moves_list = capture_moves + quiet_moves
    moves_list.sort(key=lambda zug: score(board, zug[0], zug[1], "black"), reverse=True)
    for zug in moves_list:
        start, target = zug
        piece = board[start[0]][start[1]]
        target_inhalt = board[target[0]][target[1]]
        board[target[0]][target[1]] = piece
        board[start[0]][start[1]] = "0"
        evaluation = minimax(board, tiefe -1, False, alpha, beta)
        if evaluation > best_score:
            best_score = evaluation
            best_move = []
            best_move.append(zug)
            alpha = best_score
        elif evaluation == best_score:
            best_move.append(zug)
        board[start[0]][start[1]] = piece
        board[target[0]][target[1]] = target_inhalt
        moves.white_short = old_white_short
        moves.white_long = old_white_long
        moves.black_short = old_black_short
        moves.black_long = old_black_long
        moves.last_move = prev_last_move
    return best_move[0]


def minimax(board, tiefe, is_maximizing, alpha, beta):
    if tiefe == 0:
        return bewerte_material(board)
    key = (tuple(tuple(reihe) for reihe in board), tiefe)
    if key in transsquare_table:
        stored_value, stored_type = transsquare_table[key]
        if stored_type == "exakt":
            return stored_value
        if stored_type == "untere_grenze":
            alpha = max(alpha, stored_value)
        if stored_type == "obere_grenze":
            beta = min(beta, stored_value)
        if alpha >= beta:
            return stored_value
    scores = []
    if is_maximizing == True:
        moves_list = all_moves(board)
    if is_maximizing == False:
        moves_list = all_moves_white(board)
    if moves_list == []:
        if in_check(board, "white") == True and is_maximizing == False:
            return 1000 + tiefe
        if in_check(board, "black") == True and is_maximizing == True:
            return -1000 - tiefe
        return 0
    prev_last_move = moves.last_move
    old_white_short = moves.white_short
    old_white_long = moves.white_long
    old_black_short = moves.black_short
    old_black_long = moves.black_long
    for zug in moves_list:
        start, target = zug
        piece = board[start[0]][start[1]]
        target_inhalt = board[target[0]][target[1]]
        board[target[0]][target[1]] = piece
        board[start[0]][start[1]] = "0"
        ergebnis = minimax(board, tiefe - 1, not is_maximizing, alpha, beta)
        scores.append(ergebnis)
        if is_maximizing == True:
            alpha = max(alpha, ergebnis)
        if is_maximizing == False:
            beta = min(beta, ergebnis)
        board[start[0]][start[1]] = piece
        board[target[0]][target[1]] = target_inhalt
        moves.white_short = old_white_short
        moves.white_long = old_white_long
        moves.black_short = old_black_short
        moves.black_long = old_black_long
        moves.last_move = prev_last_move
        if alpha >= beta:
            break
    ergebnis = max(scores) if is_maximizing else min(scores)
    if ergebnis <= alpha:
        transsquare_table[key] = (ergebnis, "obere_grenze")
    elif ergebnis >= beta:
        transsquare_table[key] = (ergebnis, "untere_grenze")
    else:
        transsquare_table[key] = (ergebnis, "exakt")
    return ergebnis

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
