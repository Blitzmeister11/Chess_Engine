from tkinter import *

weiß_kurz = True
weiß_lang = True
schwarz_kurz = True
schwarz_lang = True
weiß_kurz_ausführen = False
weiß_lang_ausführen = False
schwarz_kurz_ausführen = False
schwarz_lang_ausführen = False
letzter_zug = None

richtungen_gerade = [
    (+1, +0),
    (-1, +0),
    (+0, +1),
    (+0, -1)
]
richtungen_diagonal = [
    (+1, +1),
    (+1, -1),
    (-1, +1),
    (-1, -1)
]
richtungen_Springer = [
    (+2, +1),
    (+2, -1),
    (-2, +1),
    (-2, -1),
    (+1, +2),
    (+1, -2),
    (-1, +2),
    (-1, -2)
]
richtungen_König = [
    (+1, +1),
    (+1, -1),
    (+1, 0),
    (-1, +1),
    (-1, -1),
    (-1, 0),
    (0, +1),
    (0, -1),
]
zügeKönig = [
    (+1, +1),
    (+1, 0),
    (+1, -1),
    (0, +1),
    (0, -1),
    (-1, +1),
    (-1, 0),
    (-1, -1)
]
sprünge = [
    (+2, +1),
    (+2, -1),
    (-2, +1),
    (-2, -1),
    (+1, +2),
    (+1, -2),
    (-1, +2),
    (-1, -2)
]
zügeTurm = [
    (+1, 0),
    (-1, 0),
    (0, +1),
    (0, -1),
]
zügeLäufer = [
    (+1, +1),
    (-1, +1),
    (-1, -1),
    (+1, -1),
]
def finde_springer(board):
    Springer = []
    for index, reihe in enumerate(board):
            for spalte in range(8):
                if board[index][spalte] == "S" or board[index][spalte] == "-S":
                    Springer.append((index, spalte))
    return Springer

def springer_züge(board, position):
    felder_Springer = []
    for sprung in sprünge:
        neue_reihe = position[0] + sprung[0]
        neue_spalte = position[1] + sprung[1]

        if neue_reihe < 0 or neue_reihe > 7 or neue_spalte < 0 or neue_spalte > 7:
            continue
        if board[position[0]][position[1]] == "-S":
            if "-" in board[neue_reihe][neue_spalte]:
                continue
        if board[position[0]][position[1]] == "S":
            if ("-" not in board[neue_reihe][neue_spalte] and not board[neue_reihe][neue_spalte] == "0"):
                continue

        felder_Springer.append((neue_reihe, neue_spalte))
    return felder_Springer

def finde_turm(board):
    Turm = []
    for index, reihe in enumerate(board):
            for spalte in range(8):
                if board[index][spalte] == "T" or board[index][spalte] == "-T":
                    Turm.append((index, spalte))
    return Turm

def turm_züge(board, position):
    felder_Turm = []
    for richtung in zügeTurm:
        aktuelle_reihe = position[0]
        aktuelle_spalte = position[1]
        TurmPossible = True
        while TurmPossible == True:
            neue_reihe = aktuelle_reihe + richtung[0]
            neue_spalte = aktuelle_spalte + richtung[1]

            if neue_reihe < 0 or neue_reihe > 7 or neue_spalte < 0 or neue_spalte > 7:
                TurmPossible = False
                continue
            if board[position[0]][position[1]] == "-T" or board[position[0]][position[1]] == "-D":
                if "-" in board[neue_reihe][neue_spalte]:
                    TurmPossible = False
                    continue
            if board[position[0]][position[1]] == "T" or board[position[0]][position[1]] == "D":
                if ("-" not in board[neue_reihe][neue_spalte] and not board[neue_reihe][neue_spalte] == "0"):
                    TurmPossible = False
                    continue
            if board[position[0]][position[1]] == "-T" or board[position[0]][position[1]] == "-D":
                if ("-" not in board[neue_reihe][neue_spalte] and not board[neue_reihe][neue_spalte] == "0"):
                    felder_Turm.append((neue_reihe, neue_spalte))
                    TurmPossible = False
                    continue
            if board[position[0]][position[1]] == "T" or board[position[0]][position[1]] == "D":
                if "-" in board[neue_reihe][neue_spalte]:
                    felder_Turm.append((neue_reihe, neue_spalte))
                    TurmPossible = False
                    continue
            if TurmPossible == True:
                felder_Turm.append((neue_reihe, neue_spalte))

            aktuelle_reihe = neue_reihe
            aktuelle_spalte = neue_spalte

    return felder_Turm

def finde_läufer(board):
    Läufer = []
    for index, reihe in enumerate(board):
            for spalte in range(8):
                if board[index][spalte] == "L" or board[index][spalte] == "-L":
                    Läufer.append((index, spalte))
    return Läufer

def läufer_züge(board, position):
    felder_Läufer = []
    for richtung in zügeLäufer:
        aktuelle_reihe = position[0]
        aktuelle_spalte = position[1]
        LäuferPossible = True
        while LäuferPossible == True:
            neue_reihe = aktuelle_reihe + richtung[0]
            neue_spalte = aktuelle_spalte + richtung[1]
            if neue_reihe < 0 or neue_reihe > 7 or neue_spalte < 0 or neue_spalte > 7:
                LäuferPossible = False
                continue
            if board[position[0]][position[1]] == "-L" or board[position[0]][position[1]] == "-D":
                if "-" in board[neue_reihe][neue_spalte]:
                    LäuferPossible = False
                    continue
            if board[position[0]][position[1]] == "L" or board[position[0]][position[1]] =="D":
                if ("-" not in board[neue_reihe][neue_spalte] and not board[neue_reihe][neue_spalte] == "0"):
                    LäuferPossible = False
                    continue
            if board[position[0]][position[1]] == "-L" or board[position[0]][position[1]] == "-D":
                if ("-" not in board[neue_reihe][neue_spalte] and not board[neue_reihe][neue_spalte] == "0"):
                    felder_Läufer.append((neue_reihe, neue_spalte))
                    LäuferPossible = False
                    continue
            if board[position[0]][position[1]] == "L" or board[position[0]][position[1]] =="D":
                if "-" in board[neue_reihe][neue_spalte]:
                    felder_Läufer.append((neue_reihe, neue_spalte))
                    LäuferPossible = False
                    continue
            if LäuferPossible == True:
                felder_Läufer.append((neue_reihe, neue_spalte))

            aktuelle_reihe = neue_reihe
            aktuelle_spalte = neue_spalte

    return felder_Läufer

def finde_Dame(board):
    Dame = []
    for index, reihe in enumerate(board):
            for spalte in range(8):
                if board[index][spalte] == "D" or board[index][spalte] == "-D":
                    Dame.append((index, spalte))
    return Dame

def dame_züge(board, position):
    turm_ergebnis = turm_züge(board, position)
    läufer_ergebnis = läufer_züge(board, position)
    felder_Dame = turm_ergebnis + läufer_ergebnis
    return felder_Dame

def finde_König(board):
    König = []
    for index, reihe in enumerate(board):
            for spalte in range(8):
                if board[index][spalte] == "K" or board[index][spalte] == "-K":
                    König.append((index, spalte))
    return König

def könig_züge(board, position):
    felder_König = []
    for Zug in zügeKönig:
        neue_reihe = position[0] + Zug[0]
        neue_spalte = position[1] + Zug[1]

        if neue_reihe < 0 or neue_reihe > 7 or neue_spalte < 0 or neue_spalte > 7:
            continue
        if board[position[0]][position[1]] == "K":
            if ("-" not in board[neue_reihe][neue_spalte] and not board[neue_reihe][neue_spalte] == "0"):
                continue

        if board[position[0]][position[1]] == "-K":
            if "-" in board[neue_reihe][neue_spalte]:
                continue


        felder_König.append((neue_reihe, neue_spalte))
    if board[position[0]][position[1]] == "K":
        if weiß_kurz == True:
            if board[7][5] == "0" and board[7][6] == "0":
                felder_König.append((7,6))
        if weiß_lang == True:
            if board[7][1] == "0" and board[7][2] == "0" and board[7][3] == "0":
                felder_König.append((7,2))

    if board[position[0]][position[1]] == "-K":
        if schwarz_kurz == True:
            if board[0][5] == "0" and board[0][6] == "0":
                felder_König.append((0,6))
        if schwarz_lang == True:
            if board[0][1] == "0" and board[0][2] == "0" and board[0][3] == "0":
                felder_König.append((0,2))

    return  felder_König

def finde_Bauer(board):
    Bauer = []
    for index, reihe in enumerate(board):
        for spalte in range(8):
            if board[index][spalte] == "B" or board[index][spalte] == "-B":
                Bauer.append((index, spalte))
    return Bauer

def bauer_züge(board, position, farbe, letzter_zug):
    felder_Bauer = []
    zügeBauerWeiß = [
        (-1,+0)
    ]
    zügeBauerSchwarz = [
        (+1,+0),
    ]
    if farbe == "weiß":
        for Zug in zügeBauerWeiß:
            if board[position[0]][position[1]] == "B":
                neue_reihe = position[0] + Zug[0]
                neue_spalte = position[1] + Zug[1]
                if board[neue_reihe][neue_spalte] == "0":
                    felder_Bauer.append((neue_reihe, neue_spalte))
                if position[1] + 1 <= 7 and "-" in board[position[0] - 1][position[1] + 1]:
                    neue_reihe = position[0] - 1
                    neue_spalte = position[1] + 1
                    if neue_spalte <= 7:
                        felder_Bauer.append((neue_reihe, neue_spalte))
                if position[1] - 1 >= 0 and "-" in board[position[0] - 1][position[1] - 1]:
                    neue_reihe = position[0] - 1
                    neue_spalte = position[1] - 1
                    if neue_spalte >= 0:
                        felder_Bauer.append((neue_reihe, neue_spalte))
                if position[0] == 6:
                    if board[position[0] - 1][position[1]] == "0" and board[position[0] - 2][position[1]] == "0":
                        neue_reihe = position[0] - 2
                        neue_spalte = position[1] + Zug[1]
                        felder_Bauer.append((neue_reihe, neue_spalte))
                if letzter_zug is not None and letzter_zug[2] == "-B" and position[0] == 3:
                    if letzter_zug[0][0] == 1 and letzter_zug[1][0] == 3:
                        letzte_spalte = letzter_zug[1][1]
                        if letzte_spalte == position[1] + 1:
                            felder_Bauer.append((2, letzte_spalte))
                        if letzte_spalte == position[1] - 1:
                            felder_Bauer.append((2, letzte_spalte))

    if farbe == "schwarz":
        for Zug in zügeBauerSchwarz:
            if board[position[0]][position[1]] == "-B":
                neue_reihe = position[0] + Zug[0]
                neue_spalte = position[1] + Zug[1]
                if board[neue_reihe][neue_spalte] == "0":
                    felder_Bauer.append((neue_reihe, neue_spalte))
                if position[1] + 1 <= 7 and "-" not in board[position[0] + 1][position[1] + 1] and not board[position[0] + 1][position[1] + 1] == "0":
                        neue_reihe = position[0] + 1
                        neue_spalte = position[1] + 1
                        if neue_spalte <= 7:
                            felder_Bauer.append((neue_reihe, neue_spalte))
                if position[1] - 1 >= 0 and "-" not in board[position[0] + 1][position[1] - 1] and not board[position[0] + 1][position[1] - 1] == "0":
                    neue_reihe = position[0] + 1
                    neue_spalte = position[1] - 1
                    if neue_spalte >= 0:
                        felder_Bauer.append((neue_reihe, neue_spalte))
                if position[0] == 1:
                    if board[position[0] + 1][position[1]] == "0" and board[position[0] + 2][position[1]] == "0":
                        neue_reihe = position[0] + 2
                        neue_spalte = position[1] + Zug[1]
                        felder_Bauer.append((neue_reihe, neue_spalte))
                if letzter_zug is not None and letzter_zug[2] == "B" and position[0] == 4:
                    if letzter_zug[0][0] == 6 and letzter_zug[1][0] == 4:
                        letzte_spalte = letzter_zug[1][1]
                        if letzte_spalte == position[1] + 1:
                            felder_Bauer.append((5, letzte_spalte))
                        if letzte_spalte == position[1] - 1:
                            felder_Bauer.append((5, letzte_spalte))


    return felder_Bauer

def mache_zug(board,start_feld,ziel_feld):
    global weiß_kurz, weiß_lang, schwarz_kurz, schwarz_lang
    global weiß_kurz_ausführen, weiß_lang_ausführen
    global schwarz_kurz_ausführen, schwarz_lang_ausführen
    global letzter_zug

    felder = []
    erfolg = False
    if "-" in board[start_feld[0]][start_feld[1]]:
        farbe = "schwarz"
    else:
        farbe = "weiß"
    if board[start_feld[0]][start_feld[1]] == "B":
        felder = bauer_züge(board,start_feld, "weiß",letzter_zug)
        farbe = "weiß"
    if board[start_feld[0]][start_feld[1]] == "-B":
        felder = bauer_züge(board, start_feld, "schwarz", letzter_zug)
        farbe = "schwarz"
    if "S" in board[start_feld[0]][start_feld[1]]:
        felder = springer_züge(board,start_feld)
    if "T" in board[start_feld[0]][start_feld[1]]:
        felder = turm_züge(board, start_feld)
    if "L" in board[start_feld[0]][start_feld[1]]:
        felder = läufer_züge(board, start_feld)
    if "D" in board[start_feld[0]][start_feld[1]]:
        felder = dame_züge(board,start_feld)
    if "K" in board[start_feld[0]][start_feld[1]]:
        if start_feld == (7, 4) and ziel_feld == (7, 6):
            weiß_kurz_ausführen = True
        if start_feld == (7, 4) and ziel_feld == (7, 2):
            weiß_lang_ausführen = True
        if start_feld == (0, 4) and ziel_feld == (0, 6):
            schwarz_kurz_ausführen = True
        if start_feld == (0, 4) and ziel_feld == (0, 2):
            schwarz_lang_ausführen = True
        felder = könig_züge(board, start_feld)
    if ziel_feld in felder:
        figur = board[start_feld[0]][start_feld[1]]
        ziel_inhalt = board[ziel_feld[0]][ziel_feld[1]]
        board[ziel_feld[0]][ziel_feld[1]] = board[start_feld[0]][start_feld[1]]
        board[start_feld[0]][start_feld[1]] = "0"
        verursacht_schach = im_schach(board,farbe)
        if verursacht_schach == True:
            board[start_feld[0]][start_feld[1]] = figur
            board[ziel_feld[0]][ziel_feld[1]] = ziel_inhalt
        else:
            rochade_blockiert = False
            if weiß_kurz_ausführen == True:
                if rochade_schach(board, (7,4), "weiß") == True or rochade_schach(board, (7,5), "weiß") == True or rochade_schach(board, (7,6), "weiß") == True:
                    weiß_kurz_ausführen = False
                    board[start_feld[0]][start_feld[1]] = figur
                    board[ziel_feld[0]][ziel_feld[1]] = ziel_inhalt
                    rochade_blockiert = True
                    erfolg = False
                if weiß_kurz_ausführen == True:
                    board[7][5] ="T"
                    board[7][7] ="0"
                    weiß_kurz_ausführen = False
                    weiß_lang_ausführen = False
                    weiß_kurz = False
                    weiß_lang = False
            if weiß_lang_ausführen == True:
                if rochade_schach(board, (7, 4), "weiß") == True or rochade_schach(board, (7, 3),"weiß") == True or rochade_schach(board, (7, 2), "weiß") == True:
                    weiß_lang_ausführen = False
                    board[start_feld[0]][start_feld[1]] = figur
                    board[ziel_feld[0]][ziel_feld[1]] = ziel_inhalt
                    rochade_blockiert = True
                    erfolg = False
                if weiß_lang_ausführen == True:
                    board[7][3] ="T"
                    board[7][0] ="0"
                    weiß_lang_ausführen = False
                    weiß_kurz_ausführen = False
                    weiß_lang = False
                    weiß_kurz = False
            if schwarz_kurz_ausführen == True:
                if rochade_schach(board, (0, 4), "schwarz") == True or rochade_schach(board, (0, 5),"schwarz") == True or rochade_schach(board, (0, 6), "schwarz") == True:
                    schwarz_kurz_ausführen = False
                    board[start_feld[0]][start_feld[1]] = figur
                    board[ziel_feld[0]][ziel_feld[1]] = ziel_inhalt
                    rochade_blockiert = True
                    erfolg = False
                if schwarz_kurz_ausführen == True:
                    board[0][5] ="-T"
                    board[0][7] ="0"
                    schwarz_kurz_ausführen = False
                    schwarz_lang_ausführen = False
                    schwarz_kurz = False
                    schwarz_lang = False
            if schwarz_lang_ausführen == True:
                if rochade_schach(board,(0,4),"schwarz") == True or rochade_schach(board, (0, 3),"schwarz") == True or rochade_schach(board, (0, 2),"schwarz") == True:
                    schwarz_lang_ausführen = False
                    board[start_feld[0]][start_feld[1]] = figur
                    board[ziel_feld[0]][ziel_feld[1]] = ziel_inhalt
                    rochade_blockiert = True
                    erfolg = False
                if schwarz_lang_ausführen == True:
                    board[0][3] ="-T"
                    board[0][0] ="0"
                    schwarz_lang_ausführen = False
                    schwarz_kurz_ausführen = False
                    schwarz_lang = False
                    schwarz_kurz = False
            if rochade_blockiert == False:
                erfolg = True
            if erfolg == True:
                if board[0][ziel_feld[1]] == "B":
                    eingabePromotion = promotion_auswahl()
                    if eingabePromotion == "Dame":
                        board[0][ziel_feld[1]] = "D"
                    if eingabePromotion == "Turm":
                        board[0][ziel_feld[1]] = "T"
                    if eingabePromotion == "Springer":
                        board[0][ziel_feld[1]] = "S"
                    if eingabePromotion == "Läufer":
                        board[0][ziel_feld[1]] = "L"
                if board[7][ziel_feld[1]] == "-B":
                    board[7][ziel_feld[1]] = "-D"
                if figur == "B" and ziel_inhalt == "0" and start_feld[1] != ziel_feld[1]:
                    board[ziel_feld[0] + 1][ziel_feld[1]] = "0"
                if figur == "-B" and ziel_inhalt == "0" and start_feld[1] != ziel_feld[1]:
                    board[ziel_feld[0] - 1][ziel_feld[1]] = "0"
                if "K" in figur:
                    if farbe == "weiß":
                        weiß_kurz = False
                        weiß_lang = False
                    if farbe == "schwarz":
                        schwarz_kurz = False
                        schwarz_lang = False
                letzter_zug = (start_feld, ziel_feld, figur)
    return erfolg

def im_schach(board,farbe):
    König_angegriefen = False
    König = finde_König(board)
    if len(König) < 2:
        return False
    Position = None
    for k in König:
        if farbe == "weiß" and "-" not in board[k[0]][k[1]]:
            Position = k
        if farbe == "schwarz" and "-" in board[k[0]][k[1]]:
            Position = k
    if Position is None:
        return False
    position = Position
    for richtung in richtungen_gerade:
        aktuelle_reihe = position[0]
        aktuelle_spalte = position[1]
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
                    König_angegriefen = True
                if not board[neue_reihe][neue_spalte] == "0":
                    figur_gefunden = True
                    continue
                aktuelle_reihe = neue_reihe
                aktuelle_spalte = neue_spalte
            else:
                if board[neue_reihe][neue_spalte] == "T" or board[neue_reihe][neue_spalte] == "D":
                    figur_gefunden = True
                    König_angegriefen = True
                if not board[neue_reihe][neue_spalte] == "0":
                    figur_gefunden = True
                    continue
                aktuelle_reihe = neue_reihe
                aktuelle_spalte = neue_spalte

    for richtung in richtungen_diagonal:
        aktuelle_reihe = position[0]
        aktuelle_spalte = position[1]
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
                    König_angegriefen = True
                if not board[neue_reihe][neue_spalte] == "0":
                    figur_gefunden = True
                    continue
                aktuelle_reihe = neue_reihe
                aktuelle_spalte = neue_spalte
            else:
                if board[neue_reihe][neue_spalte] == "L" or board[neue_reihe][neue_spalte] == "D":
                    figur_gefunden = True
                    König_angegriefen = True
                if not board[neue_reihe][neue_spalte] == "0":
                    figur_gefunden = True
                    continue
                aktuelle_reihe = neue_reihe
                aktuelle_spalte = neue_spalte

    if farbe == "weiß":
        if Position[0] - 1 >= 0 and Position[1] + 1 <= 7:
            if board[Position[0] - 1][Position[1] + 1] == "-B":
                König_angegriefen = True
        if Position[0] - 1 >= 0 and Position[1] - 1 >= 0:
            if board[Position[0] - 1][Position[1] - 1] == "-B":
                König_angegriefen = True
    if farbe == "schwarz":
        if Position[0] + 1 <= 7 and Position[1] + 1 <= 7:
            if board[Position[0] + 1][Position[1] + 1] == "B":
                König_angegriefen = True
        if Position[0] + 1 <= 7 and Position[1] - 1 >= 0:
            if board[Position[0] + 1][Position[1] - 1] == "B":
                König_angegriefen = True

    for richtung in richtungen_Springer:
        neue_reihe = position[0] + richtung[0]
        neue_spalte = position[1] + richtung[1]
        if neue_reihe < 0 or neue_reihe > 7 or neue_spalte < 0 or neue_spalte > 7:
            continue
        if farbe == "weiß":
            if board[neue_reihe][neue_spalte] == "-S":
                König_angegriefen = True
        if farbe == "schwarz":
            if board[neue_reihe][neue_spalte] == "S":
                König_angegriefen = True

    for richtung in richtungen_König:
        neue_reihe = position[0] + richtung[0]
        neue_spalte = position[1] + richtung[1]
        if neue_reihe < 0 or neue_reihe > 7 or neue_spalte < 0 or neue_spalte > 7:
            continue
        if farbe == "weiß":
            if board[neue_reihe][neue_spalte] == "-K":
                König_angegriefen = True
        if farbe == "schwarz":
            if board[neue_reihe][neue_spalte] == "K":
                König_angegriefen = True
    return König_angegriefen

def rochade_schach(board,position,farbe):
    König_angegriefen = False
    for richtung in richtungen_gerade:
        aktuelle_reihe = position[0]
        aktuelle_spalte = position[1]
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
                    König_angegriefen = True
                if not board[neue_reihe][neue_spalte] == "0":
                    figur_gefunden = True
                    continue
                aktuelle_reihe = neue_reihe
                aktuelle_spalte = neue_spalte
            else:
                if board[neue_reihe][neue_spalte] == "T" or board[neue_reihe][neue_spalte] == "D":
                    figur_gefunden = True
                    König_angegriefen = True
                if not board[neue_reihe][neue_spalte] == "0":
                    figur_gefunden = True
                    continue
                aktuelle_reihe = neue_reihe
                aktuelle_spalte = neue_spalte

    for richtung in richtungen_diagonal:
        aktuelle_reihe = position[0]
        aktuelle_spalte = position[1]
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
                    König_angegriefen = True
                if not board[neue_reihe][neue_spalte] == "0":
                    figur_gefunden = True
                    continue
                aktuelle_reihe = neue_reihe
                aktuelle_spalte = neue_spalte
            else:
                if board[neue_reihe][neue_spalte] == "L" or board[neue_reihe][neue_spalte] == "D":
                    figur_gefunden = True
                    König_angegriefen = True
                if not board[neue_reihe][neue_spalte] == "0":
                    figur_gefunden = True
                    continue
                aktuelle_reihe = neue_reihe
                aktuelle_spalte = neue_spalte

    if farbe == "weiß":
        if position[0] + 1 <= 7 and position[1] + 1 <= 7:
            if board[position[0] - 1][position[1] + 1] == "-B":
                König_angegriefen = True
        if position[0] + 1 <= 7 and position[1] - 1 >= 0:
            if board[position[0] - 1][position[1] - 1] == "-B":
                König_angegriefen = True
    if farbe == "schwarz":
        if position[0] - 1 >= 0 and position[1] + 1 <= 7:
            if board[position[0] + 1][position[1] + 1] == "B":
                König_angegriefen = True
        if position[0] - 1 >= 0 and position[1] - 1 >= 0:
            if board[position[0] + 1][position[1] - 1] == "B":
                König_angegriefen = True

    for richtung in richtungen_Springer:
        neue_reihe = position[0] + richtung[0]
        neue_spalte = position[1] + richtung[1]
        if neue_reihe < 0 or neue_reihe > 7 or neue_spalte < 0 or neue_spalte > 7:
            continue
        if farbe == "weiß":
            if board[neue_reihe][neue_spalte] == "-S":
                König_angegriefen = True
        if farbe == "schwarz":
            if board[neue_reihe][neue_spalte] == "S":
                König_angegriefen = True

    return König_angegriefen

def promotion_auswahl():
    fenster_Tk = Tk()
    fenster_Tk.title("Chess Engine")
    fenster_Tk.geometry("100x100")
    global eingabePromotion
    eingabePromotion = None
    def promotion_Dame():
        global eingabePromotion
        eingabePromotion = "Dame"
        fenster_Tk.destroy()
    def promotion_Turm():
        global eingabePromotion
        eingabePromotion = "Turm"
        fenster_Tk.destroy()
    def promotion_Läufer():
        global eingabePromotion
        eingabePromotion = "Läufer"
        fenster_Tk.destroy()
    def promotion_Springer():
        global eingabePromotion
        eingabePromotion = "Springer"
        fenster_Tk.destroy()
    buttonDame = Button(fenster_Tk, text="Dame",command=promotion_Dame)
    buttonDame.grid()
    buttonTurm = Button(fenster_Tk, text="Turm",command=promotion_Turm)
    buttonTurm.grid()
    buttonLäufer = Button(fenster_Tk, text="Läufer", command=promotion_Läufer)
    buttonLäufer.grid()
    buttonSpringer = Button(fenster_Tk, text="Springer", command=promotion_Springer)
    buttonSpringer.grid()
    fenster_Tk.mainloop()
    return eingabePromotion
