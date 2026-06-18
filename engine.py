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
figuren_werte = {
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
transposition_tabelle = {}
board = create_board()
def alle_züge(board):
    alle_züge = []
    for row in range(8):
        for col in range(8):
            felder = []
            if "-" in board[row][col]:
                if board[row][col] == "-D":
                    position = (row, col)
                    felder = dame_züge(board, position)
                if board[row][col] == "-T":
                    position = (row, col)
                    felder = turm_züge(board, position)
                if board[row][col] == "-L":
                    position = (row, col)
                    felder = läufer_züge(board, position)
                if board[row][col] == "-S":
                    position = (row, col)
                    felder = springer_züge(board, position)
                if board[row][col] == "-B":
                    position = (row, col)
                    felder = bauer_züge(board, position, "schwarz", letzter_zug)
                if board[row][col] == "-K":
                    position = (row, col)
                    felder = könig_züge(board, position)
                for ziel in felder:
                    alle_züge.append((position, ziel))
    alt_letzter_zug = moves.letzter_zug
    for zug in alle_züge[:]:
        start, ziel = zug
        figur = board[start[0]][start[1]]
        ziel_inhalt = board[ziel[0]][ziel[1]]
        board[ziel[0]][ziel[1]] = figur
        board[start[0]][start[1]] = "0"
        möglich = im_schach(board, "schwarz")
        if möglich == True:
            alle_züge.remove(zug)
        board[start[0]][start[1]] = figur
        board[ziel[0]][ziel[1]] = ziel_inhalt
        moves.letzter_zug = alt_letzter_zug

    return alle_züge

def alle_züge_weiß(board):
    alle_züge = []
    for row in range(8):
        for col in range(8):
            felder = []
            if "-" not in board[row][col] and board[row][col] != "0":
                if board[row][col] == "D":
                    position = (row, col)
                    felder = dame_züge(board, position)
                if board[row][col] == "T":
                    position = (row, col)
                    felder = turm_züge(board, position)
                if board[row][col] == "L":
                    position = (row, col)
                    felder = läufer_züge(board, position)
                if board[row][col] == "S":
                    position = (row, col)
                    felder = springer_züge(board, position)
                if board[row][col] == "B":
                    position = (row, col)
                    felder = bauer_züge(board, position, "weiß", letzter_zug)
                if board[row][col] == "K":
                    position = (row, col)
                    felder = könig_züge(board, position)
                for ziel in felder:
                    alle_züge.append((position, ziel))
    alt_letzter_zug = moves.letzter_zug
    for zug in alle_züge[:]:
        start, ziel = zug
        figur = board[start[0]][start[1]]
        ziel_inhalt = board[ziel[0]][ziel[1]]
        board[ziel[0]][ziel[1]] = figur
        board[start[0]][start[1]] = "0"
        möglich = im_schach(board, "weiß")
        if möglich == True:
            alle_züge.remove(zug)
        board[start[0]][start[1]] = figur
        board[ziel[0]][ziel[1]] = ziel_inhalt
        moves.letzter_zug = alt_letzter_zug

    return alle_züge

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

def wähle_zug(board):
    schlag_züge = []
    ruhige_züge = []
    tiefe = 5
    alpha = -1000
    beta = 1000
    alt_weiß_kurz = moves.weiß_kurz
    alt_weiß_lang = moves.weiß_lang
    alt_schwarz_kurz = moves.schwarz_kurz
    alt_schwarz_lang = moves.schwarz_lang
    alt_letzter_zug = moves.letzter_zug
    züge_liste = alle_züge(board)
    if züge_liste == []:
        return None
    bester_zug = []
    beste_bewertung = -9999999
    for zug in züge_liste:
        start, ziel = zug
        if not board[ziel[0]][ziel[1]] == "0":
            schlag_züge.append(zug)
        else:
            ruhige_züge.append(zug)
    züge_liste = schlag_züge + ruhige_züge
    züge_liste.sort(key=lambda zug: score(board, zug[0], zug[1], "schwarz"), reverse=True)
    for zug in züge_liste:
        start, ziel = zug
        figur = board[start[0]][start[1]]
        ziel_inhalt = board[ziel[0]][ziel[1]]
        board[ziel[0]][ziel[1]] = figur
        board[start[0]][start[1]] = "0"
        evaluation = minimax(board, tiefe -1, False, alpha, beta)
        if evaluation > beste_bewertung:
            beste_bewertung = evaluation
            bester_zug = []
            bester_zug.append(zug)
            alpha = beste_bewertung
        elif evaluation == beste_bewertung:
            bester_zug.append(zug)
        board[start[0]][start[1]] = figur
        board[ziel[0]][ziel[1]] = ziel_inhalt
        moves.weiß_kurz = alt_weiß_kurz
        moves.weiß_lang = alt_weiß_lang
        moves.schwarz_kurz = alt_schwarz_kurz
        moves.schwarz_lang = alt_schwarz_lang
        moves.letzter_zug = alt_letzter_zug
    return bester_zug[0]


def minimax(board, tiefe, ist_maximirend, alpha, beta):
    if tiefe == 0:
        return bewerte_material(board)
    schlüssel = (tuple(tuple(reihe) for reihe in board), tiefe)
    if schlüssel in transposition_tabelle:
        gespeichert_wert, gespeichert_typ = transposition_tabelle[schlüssel]
        if gespeichert_typ == "exakt":
            return gespeichert_wert
        if gespeichert_typ == "untere_grenze":
            alpha = max(alpha, gespeichert_wert)
        if gespeichert_typ == "obere_grenze":
            beta = min(beta, gespeichert_wert)
        if alpha >= beta:
            return gespeichert_wert
    bewertungen = []
    if ist_maximirend == True:
        züge_liste = alle_züge(board)
    if ist_maximirend == False:
        züge_liste = alle_züge_weiß(board)
    if züge_liste == []:
        if im_schach(board, "weiß") == True and ist_maximirend == False:
            return 1000 + tiefe
        if im_schach(board, "schwarz") == True and ist_maximirend == True:
            return -1000 - tiefe
        return 0
    alt_letzter_zug = moves.letzter_zug
    alt_weiß_kurz = moves.weiß_kurz
    alt_weiß_lang = moves.weiß_lang
    alt_schwarz_kurz = moves.schwarz_kurz
    alt_schwarz_lang = moves.schwarz_lang
    for zug in züge_liste:
        start, ziel = zug
        figur = board[start[0]][start[1]]
        ziel_inhalt = board[ziel[0]][ziel[1]]
        board[ziel[0]][ziel[1]] = figur
        board[start[0]][start[1]] = "0"
        ergebnis = minimax(board, tiefe - 1, not ist_maximirend, alpha, beta)
        bewertungen.append(ergebnis)
        if ist_maximirend == True:
            alpha = max(alpha, ergebnis)
        if ist_maximirend == False:
            beta = min(beta, ergebnis)
        board[start[0]][start[1]] = figur
        board[ziel[0]][ziel[1]] = ziel_inhalt
        moves.weiß_kurz = alt_weiß_kurz
        moves.weiß_lang = alt_weiß_lang
        moves.schwarz_kurz = alt_schwarz_kurz
        moves.schwarz_lang = alt_schwarz_lang
        moves.letzter_zug = alt_letzter_zug
        if alpha >= beta:
            break
    ergebnis = max(bewertungen) if ist_maximirend else min(bewertungen)
    if ergebnis <= alpha:
        transposition_tabelle[schlüssel] = (ergebnis, "obere_grenze")
    elif ergebnis >= beta:
        transposition_tabelle[schlüssel] = (ergebnis, "untere_grenze")
    else:
        transposition_tabelle[schlüssel] = (ergebnis, "exakt")
    return ergebnis

def score(board, start, ziel, farbe):
    if board[ziel[0]][ziel[1]] != "0":
        return SEE(board, ziel, farbe)
    wert_start = figuren_werte.get(board[start[0]][start[1]], 0)
    wert_ziel = figuren_werte.get(board[ziel[0]][ziel[1]], 0)
    return wert_ziel - wert_start

def SEE(board,ziel,farbe):
    angreifer = []
    for richtung in richtungen_gerade:
        aktuelle_reihe = ziel[0]
        aktuelle_spalte = ziel[1]
        figur_gefunden = False
        while not figur_gefunden:
            neue_reihe = aktuelle_reihe + richtung[0]
            neue_spalte = aktuelle_spalte + richtung[1]
            if neue_reihe < 0 or neue_reihe > 7 or neue_spalte < 0 or neue_spalte > 7:
                figur_gefunden = True
                continue
            if farbe == "weiß":
                if board[neue_reihe][neue_spalte] == "-T" or board[neue_reihe][neue_spalte] == "-D":
                    figur_gefunden = True
                    angreifer.append((neue_reihe, neue_spalte))
                if not board[neue_reihe][neue_spalte] == "0":
                    figur_gefunden = True
                    continue
            else:
                if board[neue_reihe][neue_spalte] == "T" or board[neue_reihe][neue_spalte] == "D":
                    figur_gefunden = True
                    angreifer.append((neue_reihe, neue_spalte))
                if not board[neue_reihe][neue_spalte] == "0":
                    figur_gefunden = True
                    continue
            aktuelle_reihe = neue_reihe
            aktuelle_spalte = neue_spalte

    for richtung in richtungen_diagonal:
        aktuelle_reihe = ziel[0]
        aktuelle_spalte = ziel[1]
        figur_gefunden = False
        while not figur_gefunden:
            neue_reihe = aktuelle_reihe + richtung[0]
            neue_spalte = aktuelle_spalte + richtung[1]
            if neue_reihe < 0 or neue_reihe > 7 or neue_spalte < 0 or neue_spalte > 7:
                figur_gefunden = True
                continue
            if farbe == "weiß":
                if board[neue_reihe][neue_spalte] == "-L" or board[neue_reihe][neue_spalte] == "-D":
                    figur_gefunden = True
                    angreifer.append((neue_reihe, neue_spalte))
                if not board[neue_reihe][neue_spalte] == "0":
                    figur_gefunden = True
                    continue
            else:
                if board[neue_reihe][neue_spalte] == "L" or board[neue_reihe][neue_spalte] == "D":
                    figur_gefunden = True
                    angreifer.append((neue_reihe, neue_spalte))
                if not board[neue_reihe][neue_spalte] == "0":
                    figur_gefunden = True
                    continue
            aktuelle_reihe = neue_reihe
            aktuelle_spalte = neue_spalte

    for richtung in richtungen_Springer:
        neue_reihe = ziel[0] + richtung[0]
        neue_spalte = ziel[1] + richtung[1]
        if neue_reihe < 0 or neue_reihe > 7 or neue_spalte < 0 or neue_spalte > 7:
            continue
        if farbe == "weiß":
            if board[neue_reihe][neue_spalte] == "-S":
                angreifer.append((neue_reihe, neue_spalte))
        if farbe == "schwarz":
            if board[neue_reihe][neue_spalte] == "S":
                angreifer.append((neue_reihe, neue_spalte))

    for richtung in richtungen_König:
        neue_reihe = ziel[0] + richtung[0]
        neue_spalte = ziel[1] + richtung[1]
        if neue_reihe < 0 or neue_reihe > 7 or neue_spalte < 0 or neue_spalte > 7:
            continue
        if farbe == "weiß":
            if board[neue_reihe][neue_spalte] == "-K":
                angreifer.append((neue_reihe, neue_spalte))
        if farbe == "schwarz":
            if board[neue_reihe][neue_spalte] == "K":
                angreifer.append((neue_reihe, neue_spalte))
    if farbe == "weiß":
        if ziel[0] - 1 >= 0 and ziel[1] + 1 <= 7:
            if board[ziel[0] - 1][ziel[1] + 1] == "-B":
                angreifer.append((ziel[0]-1, ziel[1]+1))
        if ziel[0] - 1 >= 0 and ziel[1] - 1 >= 0:
            if board[ziel[0] - 1][ziel[1] - 1] == "-B":
                angreifer.append((ziel[0]-1, ziel[1]-1))
    if farbe == "schwarz":
        if ziel[0] + 1 <= 7 and ziel[1] + 1 <= 7:
            if board[ziel[0] + 1][ziel[1] + 1] == "B":
                angreifer.append((ziel[0]+1, ziel[1]+1))
        if ziel[0] + 1 <= 7 and ziel[1] - 1 >= 0:
            if board[ziel[0] + 1][ziel[1] - 1] == "B":
                angreifer.append((ziel[0]+1, ziel[1]-1))
    schwächster = None
    schwächster_wert = 9999
    for angriff in angreifer:
        wert = figuren_werte.get(board[angriff[0]][angriff[1]],0)
        if wert < schwächster_wert:
            schwächster_wert = wert
            schwächster = angriff
    if schwächster == None:
        return 0
    geschlagen_wert = figuren_werte.get(board[ziel[0]][ziel[1]],0)
    geschlagene_figur = board[ziel[0]][ziel[1]]
    schlagende_figur = board[schwächster[0]][schwächster[1]]
    board[ziel[0]][ziel[1]] = schlagende_figur
    board[schwächster[0]][schwächster[1]] = "0"
    SEE_ergebnis = SEE(board,ziel, "schwarz" if farbe == "weiß" else "weiß")
    board[ziel[0]][ziel[1]] = geschlagene_figur
    board[schwächster[0]][schwächster[1]] = schlagende_figur
    return max(0, geschlagen_wert - SEE_ergebnis)