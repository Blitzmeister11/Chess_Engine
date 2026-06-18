import pygame
from board import create_board, symbole
from moves import mache_zug, im_schach
import moves
from engine import wähle_zug, alle_züge, alle_züge_weiß
board = create_board()
pygame.init()
fenster = pygame.display.set_mode((700,700), pygame.RESIZABLE)
am_zug = "weiß"
hell = (222,185,126)
dunkel = (110,63,24)
font = pygame.font.SysFont("segoeuisymbol", 60)
font_klein = font_klein = pygame.font.SysFont("segoeuisymbol", 20)
buchstaben = ["a", "b", "c", "d", "e", "f", "g", "h"]
zahlen = ["1", "2", "3", "4", "5", "6", "7", "8"]
ausgewählt = None
pygame.display.set_caption("Chess Engine")
icon = pygame.image.load(r"C:\Users\Malte\Downloads\ChessEngine.png")
pygame.display.set_icon(icon)
def zeichne_brett():
    for reihe in range(8):
        for spalte in range(8):
            if (reihe + spalte) % 2 == 0:
                farbe = hell
            else:
                farbe = dunkel
            x = spalte * 80 + 30
            y = reihe * 80 + 30
            pygame.draw.rect(fenster,farbe,(x,y,80,80))
            if moves.letzter_zug is not None:
                if (reihe, spalte) == moves.letzter_zug[0] or (reihe, spalte) == moves.letzter_zug[1]:
                    pygame.draw.rect(fenster, (255, 255, 0), (x, y, 80, 80), 5)
            feld = board[reihe][spalte]
            symbol = symbole[feld]
            if feld !="0":
                text = font.render(symbol, True, (0, 0, 0))
                x = x + (80 - text.get_width()) // 2 + 7
                y = y + (80 - text.get_height()) // 2
                fenster.blit(text, (x, y))
    for i in range(8):
        x = i * 80 + 35 + 60
        y = 640
        text = font_klein.render(buchstaben[i], True, (0, 0, 0))
        fenster.blit(text, (x, y))
    for i in range(8):
        x = 30
        y =  i * 80 + 30
        zahl = 8-i
        text = font_klein.render(zahlen[zahl -1], True, (0, 0, 0))
        fenster.blit(text, (x, y))

while True:
    zeichne_brett()
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            event.pos
            feld_reihe = (event.pos[1]-30) // 80
            feld_spalte = (event.pos[0]-30) // 80
            if 0 <= feld_reihe <= 7 and 0 <= feld_spalte <= 7:
                if ausgewählt == None:
                    start_feld = (feld_reihe, feld_spalte)
                    if am_zug == "weiß":
                        if "-" not in board[feld_reihe][feld_spalte] and not board[feld_reihe][feld_spalte] == "0":
                            ausgewählt = start_feld
                    if am_zug == "schwarz":
                        if "-" in board[feld_reihe][feld_spalte] and not board[feld_reihe][feld_spalte] == "0":
                            ausgewählt = start_feld
                elif ausgewählt != None:
                    ziel_feld = (feld_reihe, feld_spalte)
                    ausgewählt = None
                    erfolg = mache_zug(board,start_feld, ziel_feld)
                    if erfolg == True:
                        erfolg = False
                        if am_zug == "weiß":
                            am_zug = "schwarz"
                            antwort_züge = alle_züge(board)
                            schach = im_schach(board, "schwarz")
                            if antwort_züge == [] and schach == True:
                                print("Schachmatt")
                                print("Weiß hat gewonnen")
                                pygame.quit()
                            elif antwort_züge == [] and schach == False:
                                print("Patt")
                                print("Unentschieden")
                                pygame.quit()
                        elif am_zug == "schwarz":
                            am_zug = "weiß"
                            antwort_züge = alle_züge_weiß(board)
                            schach = im_schach(board, "weiß")
                            if antwort_züge == [] and schach == True:
                                print("Schachmatt")
                                print("Schwarz hat gewonnen")
                                pygame.quit()
                            elif antwort_züge == [] and schach == False:
                                print("Patt")
                                print("Unentschieden")
                                pygame.quit()
                        if am_zug == "schwarz":
                            zeichne_brett()
                            pygame.display.flip()
                            engine_zug = wähle_zug(board)
                            if engine_zug is not None:
                                mache_zug(board, engine_zug[0], engine_zug[1])
                                am_zug = "weiß"
                                antwort_züge = alle_züge_weiß(board)
                                schach = im_schach(board, "weiß")
                                if antwort_züge == [] and schach == True:
                                    print("Schachmatt")
                                    print("Schwarz hat gewonnen")
                                elif antwort_züge == [] and schach == False:
                                    print("Patt")
                                    print("Unentschieden")
