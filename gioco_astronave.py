import pygame
import random
import os
import time

pygame.init()

# COSTANTI PER LA CREAZIONE DELLO SCHERMO
BARBO=0
LARGHEZZA_SCHERMO = 1000
ALTEZZA_SCHERMO = 800
COLORE_SFONDO = (19, 19, 70)

#COSTANTI GIOCATORE
DIMENSIONE_GIOCATORE = 20
posizione_giocatore_x = 400
posizione_giocatore_y = 520
VELOCITA_GIOCATORE = 10

#COSTANTI OGGETTI
DIMENSIONE_OGGETTO = 15 #⚠️1° bug: sistemare hitbox⚠️
lista_oggetti = []
VELOCITA_OGGETTI = 9

#COSTANTI PER IL PUNTEGGIO
punteggio = 0
prossimo_aumento = 10
probabilita_generazione = 15

#VARIABILI PER LA GENERAZIONE FINESTRA E ELEMENTI 
schermo = pygame.display.set_mode((LARGHEZZA_SCHERMO, ALTEZZA_SCHERMO))
pygame.display.set_caption("Avventura nello spazio!")

font = pygame.font.SysFont(None, 36)

base = os.path.dirname(__file__)

#CARICAMENTO IMMAGINI
immagine_astronave = pygame.image.load(os.path.join(base, "astronave.jpg"))
immagine_oggetto = pygame.image.load(os.path.join(base, "meteorite.jpg"))

def disegna():
    schermo.fill(COLORE_SFONDO)

    schermo.blit(immagine_astronave, (posizione_giocatore_x, posizione_giocatore_y))

    for o in lista_oggetti:
        schermo.blit(immagine_oggetto, (o[0], o[1]))

    testo = font.render(f"Punteggio: {punteggio}", True, (255, 255, 255))
    schermo.blit(testo, (10, 10))

    pygame.display.update()

#SISTEMA GENERAZIONE METEOTITI
def genera():
    global probabilita_generazione

    if random.randint(1, probabilita_generazione) == 1:
        x = random.randint(0, LARGHEZZA_SCHERMO - DIMENSIONE_OGGETTO)
        lista_oggetti.append([x, 0])

#FUNZIONE PER SCORRERE GLI OGGETTI E AUMENTARE IL PUNTEGGIO
def aggiorna():
    global lista_oggetti, punteggio, VELOCITA_OGGETTI
    global prossimo_aumento, probabilita_generazione

    nuovi = []

    for o in lista_oggetti:
        o[1] += VELOCITA_OGGETTI

        if o[1] < ALTEZZA_SCHERMO:
            nuovi.append(o)
        else:
            punteggio += 1

    lista_oggetti = nuovi

#FUNZIONE COLLISIONE PER VERIFICARE SE L'ASTRONAVE HA COLPITO UN OGGETTO, IN CASO AFFERMATIVO IL GIOCO FINISCE 
def collisione():
    global running

    player = pygame.Rect(posizione_giocatore_x, posizione_giocatore_y,
                         DIMENSIONE_GIOCATORE, DIMENSIONE_GIOCATORE)

    for o in lista_oggetti:
        obj = pygame.Rect(o[0], o[1],
                          DIMENSIONE_OGGETTO, DIMENSIONE_OGGETTO)

        if player.colliderect(obj):
            running = False


running = True
clock = pygame.time.Clock()

#FUNZIONI MOVIMENTO GIOCATORE
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        posizione_giocatore_x -= VELOCITA_GIOCATORE

    if keys[pygame.K_RIGHT]:
        posizione_giocatore_x += VELOCITA_GIOCATORE

    genera()
    aggiorna()
    collisione()
    disegna()

    clock.tick(30)

pygame.quit()