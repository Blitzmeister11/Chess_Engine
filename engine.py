from board import create_board
from moves import *
import zobrist
import moves
import time

def copy_board(board):
    return [row[:] for row in board]


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
TT_GENERATION = 0
SEARCH_START = 0
SEARCH_LIMIT = 0
board = create_board()
move_stack = []
KILLER = [[None, None] for _ in range(128)]
HISTORY = [[0 for _ in range(64)] for _ in range(64)]
NODE_COUNT = 0


def all_moves(board):
    all_moves_list = []
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
                    piece = board[row][col]
                    if piece == "-B" and target[0] == 7:
                        all_moves_list.append((square, target, "D"))
                        all_moves_list.append((square, target, "T"))
                        all_moves_list.append((square, target, "L"))
                        all_moves_list.append((square, target, "S"))
                    else:
                        all_moves_list.append((square, target, None))

    in_check_now = in_check(board, "black")
    pinned = get_pinned_pieces(board, "black")

    prev_last_move = moves.last_move
    for zug in all_moves_list[:]:
        start, target, promo = zug
        piece = board[start[0]][start[1]]
        target_inhalt = board[target[0]][target[1]]

        is_king = piece == "-K"
        is_pinned = start in pinned
        is_ep = piece == "-B" and target_inhalt == "0" and start[1] != target[1]

        if not in_check_now and not is_king and not is_pinned and not is_ep:
            continue

        ep_square = None
        ep_piece = None
        if is_ep:
            ep_square = (target[0] - 1, target[1])
            ep_piece = board[ep_square[0]][ep_square[1]]
            board[ep_square[0]][ep_square[1]] = "0"

        board[target[0]][target[1]] = piece
        board[start[0]][start[1]] = "0"
        possible = in_check(board, "black")
        if possible:
            all_moves_list.remove(zug)
        board[start[0]][start[1]] = piece
        board[target[0]][target[1]] = target_inhalt
        if ep_square is not None:
            board[ep_square[0]][ep_square[1]] = ep_piece

        moves.last_move = prev_last_move

    return all_moves_list

def all_moves_white(board):
    all_moves_list = []
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
                    piece = board[row][col]
                    if piece == "B" and target[0] == 0:
                        all_moves_list.append((square, target, "D"))
                        all_moves_list.append((square, target, "T"))
                        all_moves_list.append((square, target, "L"))
                        all_moves_list.append((square, target, "S"))
                    else:
                        all_moves_list.append((square, target, None))

    in_check_now = in_check(board, "white")
    pinned = get_pinned_pieces(board, "white")

    prev_last_move = moves.last_move
    for zug in all_moves_list[:]:
        start, target, promo = zug
        piece = board[start[0]][start[1]]
        target_inhalt = board[target[0]][target[1]]

        is_king = piece == "K"
        is_pinned = start in pinned
        is_ep = piece == "B" and target_inhalt == "0" and start[1] != target[1]

        if not in_check_now and not is_king and not is_pinned and not is_ep:
            continue

        ep_square = None
        ep_piece = None
        if is_ep:
            ep_square = (target[0] + 1, target[1])
            ep_piece = board[ep_square[0]][ep_square[1]]
            board[ep_square[0]][ep_square[1]] = "0"

        board[target[0]][target[1]] = piece
        board[start[0]][start[1]] = "0"
        possible = in_check(board, "white")
        if possible:
            all_moves_list.remove(zug)
        board[start[0]][start[1]] = piece
        board[target[0]][target[1]] = target_inhalt

        if ep_square is not None:
            board[ep_square[0]][ep_square[1]] = ep_piece

        moves.last_move = prev_last_move

    return all_moves_list

def bewerte_material(board):
    material = 0
    white_king_pos = (7,4)
    black_king_pos = (0,4)
    piece_count = 0
    white_pawns_per_col = [0] * 8
    black_pawns_per_col = [0] * 8
    white_pawn_rows = [[] for _ in range(8)]
    black_pawn_rows = [[] for _ in range(8)]
    white_bishops = 0
    black_bishops = 0
    white_rooks = []
    black_rooks = []
    for row in range(8):
        for col in range(8):
            if board[row][col] == "B":
                material -= 1
                material -= piece_square_table_pawn[row][col] / 50
                piece_count += 1
                white_pawns_per_col[col] += 1
                white_pawn_rows[col].append(row)
            if board[row][col] == "-B":
                material += 1
                material += piece_square_table_pawn[7 - row][col] / 50
                piece_count += 1
                black_pawns_per_col[col] += 1
                black_pawn_rows[col].append(row)
            if board[row][col] == "L":
                material -= 3
                material -= piece_square_table_bishop[row][col] / 50
                piece_count += 1
                white_bishops +=1
            if board[row][col] == "-L":
                material += 3
                material += piece_square_table_bishop[7- row][col] / 50
                piece_count += 1
                black_bishops +=1
            if board[row][col] == "S":
                material -= 3
                material -= piece_square_table_knight[row][col] / 50
                piece_count += 1
            if board[row][col] == "-S":
                material += 3
                material += piece_square_table_knight[7 - row][col] / 50
                piece_count += 1
            if board[row][col] == "T":
                material -= 5
                material -= piece_square_table_rook[row][col] / 50
                piece_count += 1
                white_rooks.append((row, col))
            if board[row][col] == "-T":
                material += 5
                material += piece_square_table_rook[7 - row][col] / 50
                piece_count += 1
                black_rooks.append((row, col))
            if board[row][col] == "D":
                material -= 9
                material -= piece_square_table_queen[row][col] / 50
                piece_count += 1
            if board[row][col] == "-D":
                material += 9
                material += piece_square_table_queen[7 - row][col] / 50
                piece_count += 1
            if board[row][col] == "K":
                material -= piece_square_table_king[row][col] / 50
                white_king_pos = (row, col)
            if board[row][col] == "-K":
                material += piece_square_table_king[7 - row][col] / 50
                black_king_pos = (row, col)

    if white_bishops >= 2:
        material -= 0.3
    if black_bishops >= 2:
        material += 0.3

    if piece_count <= 6 and abs(material) >= 3:
        if material < 0:
            edge_dist = min(black_king_pos[0], 7 - black_king_pos[0],
                            black_king_pos[1], 7 - black_king_pos[1])
            king_dist = max(abs(white_king_pos[0] - black_king_pos[0]),
                            abs(white_king_pos[1] - black_king_pos[1]))
            material -= (3 - edge_dist) * 0.1
            material -= (7 - king_dist) * 0.05
        if material > 0:
            edge_dist = min(white_king_pos[0], 7 - white_king_pos[0],
                            white_king_pos[1], 7 - white_king_pos[1])
            king_dist = max(abs(black_king_pos[0] - white_king_pos[0]),
                            abs(black_king_pos[1] - white_king_pos[1]))
            material += (3 - edge_dist) * 0.1
            material += (7 - king_dist) * 0.05

    for col in range(8):
        if white_pawns_per_col[col] >= 2:
            material += 0.3 * (white_pawns_per_col[col] - 1)
        if black_pawns_per_col[col] >= 2:
            material -= 0.3 * (black_pawns_per_col[col] - 1)

    for col in range(8):
        if white_pawns_per_col[col] > 0:
            left = white_pawns_per_col[col - 1] if col > 0 else 0
            right = white_pawns_per_col[col + 1] if col < 7 else 0
            if left == 0 and right == 0:
                material += 0.2 * white_pawns_per_col[col]
        if black_pawns_per_col[col] > 0:
            left = black_pawns_per_col[col - 1] if col > 0 else 0
            right = black_pawns_per_col[col + 1] if col < 7 else 0
            if left == 0 and right == 0:
                material -= 0.2 * black_pawns_per_col[col]

    for col in range(8):
        for row in white_pawn_rows[col]:
            blockers = False
            for r in black_pawn_rows[col]:
                if r < row:
                    blockers = True
            if col > 0:
                for r in black_pawn_rows[col - 1]:
                    if r < row:
                        blockers = True
            if col < 7:
                for r in black_pawn_rows[col + 1]:
                    if r < row:
                        blockers = True
            if not blockers:
                material -= 0.3 + (6 - row) * 0.1

    for col in range(8):
        for row in black_pawn_rows[col]:
            blockers = False
            for r in white_pawn_rows[col]:
                if r > row:
                    blockers = True
            if col > 0:
                for r in white_pawn_rows[col - 1]:
                    if r > row:
                        blockers = True
            if col < 7:
                for r in white_pawn_rows[col + 1]:
                    if r > row:
                        blockers = True
            if not blockers:
                material += 0.3 + (row - 1) * 0.1

    if piece_count > 6:
        wkr, wkc = white_king_pos
        white_king_safety = 0
        for dc in [-1, 0, 1]:
            c = wkc + dc
            if 0 <= c <= 7:
                if wkr - 1 >= 0 and board[wkr - 1][c] == "B":
                    white_king_safety += 1
                elif wkr - 2 >= 0 and board[wkr - 2][c] == "B":
                    white_king_safety += 0.5
        material += white_king_safety * 0.15

        bkr, bkc = black_king_pos
        black_king_safety = 0
        for dc in [-1, 0, 1]:
            c = bkc + dc
            if 0 <= c <= 7:
                if bkr + 1 <= 7 and board[bkr + 1][c] == "-B":
                    black_king_safety += 1
                elif bkr + 2 <= 7 and board[bkr + 2][c] == "-B":
                    black_king_safety += 0.5
        material -= black_king_safety * 0.15

        if 2 <= wkc <= 5:
            material += 0.3
        if 2 <= bkc <= 5:
            material -= 0.3

        for dc in [-1, 0, 1]:
            c = wkc + dc
            if 0 <= c <= 7:
                if white_pawns_per_col[c] == 0 and black_pawns_per_col[c] == 0:
                    material += 0.2
                elif white_pawns_per_col[c] == 0:
                    material += 0.1
        for dc in [-1, 0, 1]:
            c = bkc + dc
            if 0 <= c <= 7:
                if white_pawns_per_col[c] == 0 and black_pawns_per_col[c] == 0:
                    material -= 0.2
                elif black_pawns_per_col[c] == 0:
                    material -= 0.1

    for rook in white_rooks:
        col = rook[1]
        if white_pawns_per_col[col] == 0 and black_pawns_per_col[col] == 0:
            material -= 0.2
        elif white_pawns_per_col[col] == 0:
            material -= 0.1
    for rook in black_rooks:
        col = rook[1]
        if white_pawns_per_col[col] == 0 and black_pawns_per_col[col] == 0:
            material += 0.2
        elif black_pawns_per_col[col] == 0:
            material += 0.1

    return material

def choose_move(board, color, depth=5):
    alpha = -1000000
    beta = 1000000

    moves_list = all_moves(board) if color == "black" else all_moves_white(board)
    if not moves_list:
        return None

    capture_moves = []
    quiet_moves = []
    for zug in moves_list:
        start, target, promo = zug
        if board[target[0]][target[1]] != "0":
            capture_moves.append(zug)
        else:
            quiet_moves.append(zug)

    capture_moves.sort(key=lambda zug: move_score(zug, depth), reverse=True)
    quiet_moves.sort(key=lambda zug: move_score(zug, depth), reverse=True)
    moves_list = capture_moves + quiet_moves

    best_move = None
    best_score = -9999999

    for start, target, promo in moves_list:
        make_move_search(board, start, target, promo)

        next_color = "white" if color == "black" else "black"
        evaluation = -negamax(
            board,
            depth - 1,
            next_color,
            -beta,
            -alpha,
            moves.current_hash,
            moves.position_history,
            moves.halfmove_clock
        )

        unmake_move_search(board)

        if evaluation > best_score:
            best_score = evaluation
            best_move = (start, target, promo)
            alpha = evaluation

    return best_move

def move_score(move, depth):
    start, target, promo = move
    if board[target[0]][target[1]] != "0":
        see_value = SEE(board, target)
        if see_value > 0:
            return 900000 + see_value
        elif see_value == 0:
            return 800000
        else:
            return 100000 + see_value
    if move == KILLER[depth][0]:
        return 700000
    if move == KILLER[depth][1]:
        return 600000
    return history_score(move)


def negamax(board, depth, color, alpha, beta, zobrist_hash, history, halfmove_clock):
    alpha_orig = alpha
    global NODE_COUNT
    NODE_COUNT += 1
    if zobrist_hash in transsquare_table:
        d, v, bound, gen = transsquare_table[zobrist_hash]
        if gen == TT_GENERATION and d >= depth:
            if bound == "exact":
                return v
            if bound == "lower":
                alpha = max(alpha, v)
            if bound == "upper":
                beta = min(beta, v)
            if alpha >= beta:
                return v

    if halfmove_clock >= 100:
        return 0
    if history.get(zobrist_hash, 0) >= 3:
        return 0

    if time.time() - SEARCH_START > SEARCH_LIMIT:
        return bewerte_material(board) if color == "black" else -bewerte_material(board)

    if depth == 0:
        return quiescence(board, alpha, beta, color)

    moves_list = all_moves(board) if color == "black" else all_moves_white(board)

    in_check_now = in_check(board, color)

    if not moves_list:
        if in_check_now:
            return -1000 - depth
        return 0

    capture_moves = []
    quiet_moves = []
    for start, target, promo in moves_list:
        if board[target[0]][target[1]] != "0":
            capture_moves.append((start, target, promo))
        else:
            quiet_moves.append((start, target, promo))

    capture_moves.sort(key=lambda zug: SEE(board, zug[1]), reverse=True)
    quiet_moves.sort(key=lambda zug: move_score(zug, depth), reverse=True)
    moves_list = capture_moves + quiet_moves

    best_score = -9999999
    move_index = 0

    for move in moves_list:
        start, target, promo = move

        is_capture = board[target[0]][target[1]] != "0"

        make_move_search(board, start, target, promo)

        move_gives_check = False
        new_depth = depth - 1

        next_color = "white" if color == "black" else "black"

        if move_index == 0:
            score_result = -negamax(
                board,
                new_depth,
                next_color,
                -beta,
                -alpha,
                moves.current_hash,
                moves.position_history,
                moves.halfmove_clock
            )
        else:
            can_reduce = (
                move_index >= 3
                and new_depth >= 3
                and not is_capture
                and move != KILLER[depth][0]
                and move != KILLER[depth][1]
                and not move_gives_check
                and not in_check_now
            )

            if can_reduce:
                reduction = 1 + move_index // 6
                reduced_depth = max(1, new_depth - reduction)
            else:
                reduced_depth = new_depth

            score_result = -negamax(
                board,
                reduced_depth,
                next_color,
                -alpha - 1,
                -alpha,
                moves.current_hash,
                moves.position_history,
                moves.halfmove_clock
            )

            if score_result > alpha:
                score_result = -negamax(
                    board,
                    new_depth,
                    next_color,
                    -beta,
                    -alpha,
                    moves.current_hash,
                    moves.position_history,
                    moves.halfmove_clock
                )

        unmake_move_search(board)

        if score_result > best_score:
            best_score = score_result

        if score_result > alpha:
            alpha = score_result

        if alpha >= beta:
            if not is_capture:
                if KILLER[depth][0] != move:
                    KILLER[depth][1] = KILLER[depth][0]
                    KILLER[depth][0] = move
                HISTORY[start[0] * 8 + start[1]][target[0] * 8 + target[1]] += depth * depth
            break

        move_index += 1

    if best_score <= alpha_orig:
        transsquare_table[zobrist_hash] = (depth, best_score, "upper", TT_GENERATION)
    elif best_score >= beta:
        transsquare_table[zobrist_hash] = (depth, best_score, "lower", TT_GENERATION)
    else:
        transsquare_table[zobrist_hash] = (depth, best_score, "exact", TT_GENERATION)

    return best_score


def quiescence(board, alpha, beta, color, depth=10):
    if time.time() - SEARCH_START > SEARCH_LIMIT:
        return bewerte_material(board) if color == "black" else -bewerte_material(board)
    stand_pat = bewerte_material(board) if color == "black" else -bewerte_material(board)
    if depth <= 0:
        return stand_pat
    if stand_pat >= beta:
        return beta
    if alpha < stand_pat:
        alpha = stand_pat

    moves_list = all_moves(board) if color == "black" else all_moves_white(board)

    capture_moves = []
    for zug in moves_list:
        start, target, promo = zug
        if board[target[0]][target[1]] != "0":
            if SEE(board, target) >= 0:
                capture_moves.append(zug)

    for start, target, promo in capture_moves:
        make_move_search(board, start, target, promo)

        next_color = "white" if color == "black" else "black"
        score_result = -quiescence(board, -beta, -alpha, next_color, depth - 1)

        unmake_move_search(board)

        if score_result >= beta:
            return beta
        if score_result > alpha:
            alpha = score_result

    return alpha


def score(board, start, target):
    if board[target[0]][target[1]] != "0":
        return SEE(board, target)
    return 0


def SEE(board, target):
    piece_on_target = board[target[0]][target[1]]
    if piece_on_target == "0":
        return 0

    attackers_white = []
    attackers_black = []

    for dr, dc in direction_straight:
        r, c = target
        while True:
            r += dr
            c += dc
            if r < 0 or r > 7 or c < 0 or c > 7:
                break
            p = board[r][c]
            if p != "0":
                if p in ("T", "D"):
                    attackers_white.append((r, c, piece_score[p]))
                if p in ("-T", "-D"):
                    attackers_black.append((r, c, piece_score[p]))
                break

    for dr, dc in direction_diagonal:
        r, c = target
        while True:
            r += dr
            c += dc
            if r < 0 or r > 7 or c < 0 or c > 7:
                break
            p = board[r][c]
            if p != "0":
                if p in ("L", "D"):
                    attackers_white.append((r, c, piece_score[p]))
                if p in ("-L", "-D"):
                    attackers_black.append((r, c, piece_score[p]))
                break

    for dr, dc in direction_Knight:
        r = target[0] + dr
        c = target[1] + dc
        if 0 <= r <= 7 and 0 <= c <= 7:
            p = board[r][c]
            if p == "S":
                attackers_white.append((r, c, piece_score[p]))
            if p == "-S":
                attackers_black.append((r, c, piece_score[p]))

    for dr, dc in direction_King:
        r = target[0] + dr
        c = target[1] + dc
        if 0 <= r <= 7 and 0 <= c <= 7:
            p = board[r][c]
            if p == "K":
                attackers_white.append((r, c, piece_score[p]))
            if p == "-K":
                attackers_black.append((r, c, piece_score[p]))

    r, c = target
    if r > 0:
        if c > 0 and board[r-1][c-1] == "-B":
            attackers_black.append((r-1, c-1, 1))
        if c < 7 and board[r-1][c+1] == "-B":
            attackers_black.append((r-1, c+1, 1))
    if r < 7:
        if c > 0 and board[r+1][c-1] == "B":
            attackers_white.append((r+1, c-1, 1))
        if c < 7 and board[r+1][c+1] == "B":
            attackers_white.append((r+1, c+1, 1))

    attackers_white.sort(key=lambda x: x[2])
    attackers_black.sort(key=lambda x: x[2])

    def exchange(side, w, b, gain):
        if side == "white":
            if not w:
                return gain
            r, c, v = w[0]
            new_w = w[1:]
            new_b = [(rr, cc, vv) for rr, cc, vv in b if not (rr == r and cc == c)]
            return max(gain, -exchange("black", new_w, new_b, gain - v))
        else:
            if not b:
                return gain
            r, c, v = b[0]
            new_b = b[1:]
            new_w = [(rr, cc, vv) for rr, cc, vv in w if not (rr == r and cc == c)]
            return max(gain, -exchange("white", new_w, new_b, gain - v))

    return exchange("white", attackers_white, attackers_black, 0)

def choose_move_iterative(board, color, max_depth=99, time_limit=180):
    global SEARCH_START, SEARCH_LIMIT
    global TT_GENERATION
    global NODE_COUNT
    TT_GENERATION += 1
    SEARCH_START = time.time()
    SEARCH_LIMIT = time_limit

    best_move_overall = None

    for depth in range(1, max_depth + 1):
        if time.time() - SEARCH_START > SEARCH_LIMIT:
            break

        result = choose_move(board, color, depth)
        if result is None:
            break

        best_move_overall = result
        elapsed = time.time() - SEARCH_START
        elapsed = time.time() - SEARCH_START
        print(f"Tiefe {depth} | Nodes: {NODE_COUNT} | Zeit: {elapsed:.2f}s")
        NODE_COUNT = 0

        if time.time() - SEARCH_START > SEARCH_LIMIT:
            break

    return best_move_overall


def make_move_search(board, start, target, promotion_piece=None):
    piece = board[start[0]][start[1]]
    captured = board[target[0]][target[1]]

    is_castling = False
    rook_start = None
    rook_target = None
    rook_piece = None

    if piece == "K":
        if start == (7, 4) and target == (7, 6):
            is_castling = True
            rook_start = (7, 7)
            rook_target = (7, 5)
        if start == (7, 4) and target == (7, 2):
            is_castling = True
            rook_start = (7, 0)
            rook_target = (7, 3)
    if piece == "-K":
        if start == (0, 4) and target == (0, 6):
            is_castling = True
            rook_start = (0, 7)
            rook_target = (0, 5)
        if start == (0, 4) and target == (0, 2):
            is_castling = True
            rook_start = (0, 0)
            rook_target = (0, 3)

    is_en_passant = False
    ep_square = None
    ep_piece = None
    if piece == "B" and captured == "0" and start[1] != target[1]:
        is_en_passant = True
        ep_square = (target[0] + 1, target[1])
        ep_piece = board[ep_square[0]][ep_square[1]]
    if piece == "-B" and captured == "0" and start[1] != target[1]:
        is_en_passant = True
        ep_square = (target[0] - 1, target[1])
        ep_piece = board[ep_square[0]][ep_square[1]]

    prev_hash = moves.current_hash
    prev_count = moves.position_history.get(prev_hash, 0)

    state = (
        start, target, piece, captured,
        moves.white_short, moves.white_long,
        moves.black_short, moves.black_long,
        moves.last_move, moves.halfmove_clock,
        moves.current_hash, prev_hash, prev_count,
        is_castling, rook_start, rook_target,
        is_en_passant, ep_square, ep_piece
    )
    move_stack.append(state)

    h = moves.current_hash
    h = zobrist.update_hash(h, start[0], start[1], piece)

    if captured != "0":
        h = zobrist.update_hash(h, target[0], target[1], captured)

    board[target[0]][target[1]] = piece
    board[start[0]][start[1]] = "0"

    if is_en_passant:
        h = zobrist.update_hash(h, ep_square[0], ep_square[1], ep_piece)
        board[ep_square[0]][ep_square[1]] = "0"

    if is_castling:
        rook_piece = board[rook_start[0]][rook_start[1]]
        h = zobrist.update_hash(h, rook_start[0], rook_start[1], rook_piece)
        board[rook_start[0]][rook_start[1]] = "0"
        board[rook_target[0]][rook_target[1]] = rook_piece
        h = zobrist.update_hash(h, rook_target[0], rook_target[1], rook_piece)

    actual_promotion = None
    if piece == "B" and target[0] == 0:
        actual_promotion = promotion_piece if promotion_piece else "D"
        board[target[0]][target[1]] = actual_promotion
        h = zobrist.update_hash(h, target[0], target[1], actual_promotion)
    elif piece == "-B" and target[0] == 7:
        actual_promotion = promotion_piece if promotion_piece else "-D"
        board[target[0]][target[1]] = actual_promotion
        h = zobrist.update_hash(h, target[0], target[1], actual_promotion)
    else:
        h = zobrist.update_hash(h, target[0], target[1], piece)

    if piece == "K":
        moves.white_short = False
        moves.white_long = False
    if piece == "-K":
        moves.black_short = False
        moves.black_long = False
    if start == (7, 0): moves.white_long = False
    if start == (7, 7): moves.white_short = False
    if start == (0, 0): moves.black_long = False
    if start == (0, 7): moves.black_short = False
    if target == (7, 0): moves.white_long = False
    if target == (7, 7): moves.white_short = False
    if target == (0, 0): moves.black_long = False
    if target == (0, 7): moves.black_short = False

    if piece in ("B", "-B") or captured != "0":
        moves.halfmove_clock = 0
    else:
        moves.halfmove_clock += 1

    h = zobrist.flip_turn(h)

    moves.current_hash = h
    moves.position_history[h] = moves.position_history.get(h, 0) + 1
    moves.last_move = (start, target, piece)


def unmake_move_search(board):
    (
        start, target, piece, captured,
        ws, wl, bs, bl,
        last, half, h, prev_hash, prev_count,
        is_castling, rook_start, rook_target,
        is_en_passant, ep_square, ep_piece
    ) = move_stack.pop()

    board[start[0]][start[1]] = piece
    board[target[0]][target[1]] = captured

    if is_castling:
        rook_piece = board[rook_target[0]][rook_target[1]]
        board[rook_start[0]][rook_start[1]] = rook_piece
        board[rook_target[0]][rook_target[1]] = "0"

    if is_en_passant and ep_square is not None:
        board[ep_square[0]][ep_square[1]] = ep_piece

    moves.white_short = ws
    moves.white_long = wl
    moves.black_short = bs
    moves.black_long = bl
    moves.last_move = last
    moves.halfmove_clock = half

    post_move_hash = moves.current_hash
    current_count = moves.position_history.get(post_move_hash, 0)
    if current_count > 1:
        moves.position_history[post_move_hash] = current_count - 1
    else:
        moves.position_history.pop(post_move_hash, None)

    moves.position_history[prev_hash] = prev_count
    moves.current_hash = h

def gives_check(board, start, target, promo, color):
    piece = board[start[0]][start[1]]
    captured = board[target[0]][target[1]]
    board[target[0]][target[1]] = piece
    board[start[0]][start[1]] = "0"
    result = in_check(board, "white" if color == "black" else "black")
    board[start[0]][start[1]] = piece
    board[target[0]][target[1]] = captured
    return result

def history_score(move):
    start, target, promo = move
    return HISTORY[start[0]*8 + start[1]][target[0]*8 + target[1]]


def get_pinned_pieces(board, color):
    pinned = set()
    king_pos = None
    own = "-" if color == "black" else ""
    enemy_straight = ("-T", "-D") if color == "white" else ("T", "D")
    enemy_diagonal = ("-L", "-D") if color == "white" else ("L", "D")

    for row in range(8):
        for col in range(8):
            p = board[row][col]
            if color == "white" and p == "K":
                king_pos = (row, col)
            if color == "black" and p == "-K":
                king_pos = (row, col)

    if king_pos is None:
        return pinned

    for dr, dc in direction_straight:
        r, c = king_pos
        candidate = None
        while True:
            r += dr
            c += dc
            if r < 0 or r > 7 or c < 0 or c > 7:
                break
            p = board[r][c]
            if p == "0":
                continue
            if candidate is None:
                if color == "white" and "-" not in p:
                    candidate = (r, c)
                elif color == "black" and "-" in p:
                    candidate = (r, c)
                else:
                    break
            else:
                if p in enemy_straight:
                    pinned.add(candidate)
                break

    for dr, dc in direction_diagonal:
        r, c = king_pos
        candidate = None
        while True:
            r += dr
            c += dc
            if r < 0 or r > 7 or c < 0 or c > 7:
                break
            p = board[r][c]
            if p == "0":
                continue
            if candidate is None:
                if color == "white" and "-" not in p:
                    candidate = (r, c)
                elif color == "black" and "-" in p:
                    candidate = (r, c)
                else:
                    break
            else:
                if p in enemy_diagonal:
                    pinned.add(candidate)
                break

    return pinned