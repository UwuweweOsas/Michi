import pygame
import random
import sys

# Inicializa Pygame
pygame.init()

# Configuración de la pantalla
ANCHO, ALTO = 300, 300
GROSOR_LINEA = 15
GROSOR_LINEA_VICTORIA = 10
FILAS_TABLERO = 3
COLUMNAS_TABLERO = 3
TAMAÑO_CASILLA = ANCHO // COLUMNAS_TABLERO
RADIO_CIRCULO = TAMAÑO_CASILLA // 3
GROSOR_CIRCULO = 15
GROSOR_CRUZ = 25
ESPACIO = TAMAÑO_CASILLA // 4
ROJO = (255, 0, 0)
COLOR_FONDO = (28, 170, 156)
COLOR_LINEA = (23, 145, 135)
COLOR_CIRCULO = (239, 231, 200)
COLOR_CRUZ = (66, 66, 66)

# Crear la pantalla
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption('3 en Raya')
pantalla.fill(COLOR_FONDO)

# Tablero
tablero = [[None for _ in range(COLUMNAS_TABLERO)] for _ in range(FILAS_TABLERO)]

# Dibujar líneas en el tablero
def dibujar_lineas():
    pygame.draw.line(pantalla, COLOR_LINEA, (0, TAMAÑO_CASILLA), (ANCHO, TAMAÑO_CASILLA), GROSOR_LINEA)
    pygame.draw.line(pantalla, COLOR_LINEA, (0, 2 * TAMAÑO_CASILLA), (ANCHO, 2 * TAMAÑO_CASILLA), GROSOR_LINEA)
    pygame.draw.line(pantalla, COLOR_LINEA, (TAMAÑO_CASILLA, 0), (TAMAÑO_CASILLA, ALTO), GROSOR_LINEA)
    pygame.draw.line(pantalla, COLOR_LINEA, (2 * TAMAÑO_CASILLA, 0), (2 * TAMAÑO_CASILLA, ALTO), GROSOR_LINEA)

# Dibujar las figuras en el tablero
def dibujar_figuras():
    for fila in range(FILAS_TABLERO):
        for col in range(COLUMNAS_TABLERO):
            if tablero[fila][col] == 'O':
                pygame.draw.circle(pantalla, COLOR_CIRCULO, (int(col * TAMAÑO_CASILLA + TAMAÑO_CASILLA // 2), int(fila * TAMAÑO_CASILLA + TAMAÑO_CASILLA // 2)), RADIO_CIRCULO, GROSOR_CIRCULO)
            elif tablero[fila][col] == 'X':
                pygame.draw.line(pantalla, COLOR_CRUZ, (col * TAMAÑO_CASILLA + ESPACIO, fila * TAMAÑO_CASILLA + TAMAÑO_CASILLA - ESPACIO), (col * TAMAÑO_CASILLA + TAMAÑO_CASILLA - ESPACIO, fila * TAMAÑO_CASILLA + ESPACIO), GROSOR_CRUZ)
                pygame.draw.line(pantalla, COLOR_CRUZ, (col * TAMAÑO_CASILLA + ESPACIO, fila * TAMAÑO_CASILLA + ESPACIO), (col * TAMAÑO_CASILLA + TAMAÑO_CASILLA - ESPACIO, fila * TAMAÑO_CASILLA + TAMAÑO_CASILLA - ESPACIO), GROSOR_CRUZ)

# Verificar si hay ganador
def verificar_ganador():
    for fila in range(FILAS_TABLERO):
        if tablero[fila][0] == tablero[fila][1] == tablero[fila][2] and tablero[fila][0] is not None:
            return tablero[fila][0]
    for col in range(COLUMNAS_TABLERO):
        if tablero[0][col] == tablero[1][col] == tablero[2][col] and tablero[0][col] is not None:
            return tablero[0][col]
    if tablero[0][0] == tablero[1][1] == tablero[2][2] and tablero[0][0] is not None:
        return tablero[0][0]
    if tablero[0][2] == tablero[1][1] == tablero[2][0] and tablero[0][2] is not None:
        return tablero[0][2]
    return None

# Verificar si hay empate
def verificar_empate():
    for fila in range(FILAS_TABLERO):
        for col in range(COLUMNAS_TABLERO):
            if tablero[fila][col] is None:
                return False
    return True

# Movimiento de la IA utilizando Minimax
def minimax(tablero, profundidad, es_maximizador):
    ganador = verificar_ganador()
    if ganador == 'O':
        return 1
    elif ganador == 'X':
        return -1
    elif verificar_empate():
        return 0

    if es_maximizador:
        mejor_puntaje = -float('inf')
        for fila in range(FILAS_TABLERO):
            for col in range(COLUMNAS_TABLERO):
                if tablero[fila][col] is None:
                    tablero[fila][col] = 'O'
                    puntaje = minimax(tablero, profundidad + 1, False)
                    tablero[fila][col] = None
                    mejor_puntaje = max(puntaje, mejor_puntaje)
        return mejor_puntaje
    else:
        mejor_puntaje = float('inf')
        for fila in range(FILAS_TABLERO):
            for col in range(COLUMNAS_TABLERO):
                if tablero[fila][col] is None:
                    tablero[fila][col] = 'X'
                    puntaje = minimax(tablero, profundidad + 1, True)
                    tablero[fila][col] = None
                    mejor_puntaje = min(puntaje, mejor_puntaje)
        return mejor_puntaje

# Elegir el mejor movimiento para la IA
def mejor_movimiento():
    mejor_puntaje = -float('inf')
    movimiento = None
    for fila in range(FILAS_TABLERO):
        for col in range(COLUMNAS_TABLERO):
            if tablero[fila][col] is None:
                tablero[fila][col] = 'O'
                puntaje = minimax(tablero, 0, False)
                tablero[fila][col] = None
                if puntaje > mejor_puntaje:
                    mejor_puntaje = puntaje
                    movimiento = (fila, col)
    return movimiento

# Reiniciar el tablero
def reiniciar():
    global tablero, jugador
    tablero = [[None for _ in range(COLUMNAS_TABLERO)] for _ in range(FILAS_TABLERO)]
    jugador = random.choice(['X', 'O'])
    pantalla.fill(COLOR_FONDO)
    dibujar_lineas()

# Inicialización del juego
jugador = random.choice(['X', 'O'])
juego_terminado = False
dibujar_lineas()

# Loop del juego
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if evento.type == pygame.MOUSEBUTTONDOWN and not juego_terminado:
            mouseX = evento.pos[0] // TAMAÑO_CASILLA
            mouseY = evento.pos[1] // TAMAÑO_CASILLA

            if tablero[mouseY][mouseX] is None and jugador == 'X':
                tablero[mouseY][mouseX] = jugador
                if verificar_ganador() or verificar_empate():
                    juego_terminado = True
                jugador = 'O'

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_r:
                reiniciar()
                juego_terminado = False

    if jugador == 'O' and not juego_terminado:
        movimiento = mejor_movimiento()
        if movimiento:
            tablero[movimiento[0]][movimiento[1]] = 'O'
            if verificar_ganador() or verificar_empate():
                juego_terminado = True
            jugador = 'X'

    dibujar_figuras()

    if verificar_ganador():
        pygame.display.set_caption(f'Ganador: {verificar_ganador()}')
    elif verificar_empate():
        pygame.display.set_caption('Empate')

    pygame.display.update()
r