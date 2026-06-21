import collections
import heapq

# 0 = Libre, 1 = Pared
def obtener_laberinto_ejemplo():
    laberinto = [
        [0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 1, 0, 0],
        [0, 1, 1, 0, 1, 0, 1],
        [0, 0, 1, 0, 0, 0, 0],
        [1, 0, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0],
    ]
    return laberinto


def heuristica_manhattan(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


MOVIMIENTOS = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def obtener_vecinos(matriz, nodo):
    r, c = nodo
    filas = len(matriz)
    columnas = len(matriz[0])
    vecinos = []
    for dr, dc in MOVIMIENTOS:
        nr, nc = r + dr, c + dc
        if 0 <= nr < filas and 0 <= nc < columnas and matriz[nr][nc] == 0:
            vecinos.append((nr, nc))
    return vecinos


def bfs_laberinto(matriz, inicio, objetivo):
    cola = collections.deque([[inicio]])
    visitados = set()
    orden_visita = []

    while cola:
        camino = cola.popleft()
        actual = camino[-1]

        if actual not in visitados:
            visitados.add(actual)
            orden_visita.append(actual)

            if actual == objetivo:
                return camino, orden_visita

            for vecino in obtener_vecinos(matriz, actual):
                nuevo_camino = list(camino)
                nuevo_camino.append(vecino)
                cola.append(nuevo_camino)
    return None, orden_visita


def dfs_laberinto(matriz, inicio, objetivo):
    pila = [[inicio]]
    visitados = set()
    orden_visita = []

    while pila:
        camino = pila.pop()
        actual = camino[-1]

        if actual not in visitados:
            visitados.add(actual)
            orden_visita.append(actual)

            if actual == objetivo:
                return camino, orden_visita

            for vecino in obtener_vecinos(matriz, actual):
                nuevo_camino = list(camino)
                nuevo_camino.append(vecino)
                pila.append(nuevo_camino)
    return None, orden_visita


def ucs_laberinto(matriz, inicio, objetivo):
    cola_prioridad = [(0, [inicio])]
    visitados = set()
    orden_visita = []

    while cola_prioridad:
        costo, camino = heapq.heappop(cola_prioridad)
        actual = camino[-1]

        if actual in visitados:
            continue
        visitados.add(actual)
        orden_visita.append(actual)

        if actual == objetivo:
            return camino, orden_visita, costo

        for vecino in obtener_vecinos(matriz, actual):
            if vecino not in visitados:
                nuevo_camino = list(camino)
                nuevo_camino.append(vecino)
                heapq.heappush(cola_prioridad, (costo + 1, nuevo_camino))
    return None, orden_visita, float("inf")


def a_estrella_laberinto(matriz, inicio, objetivo):
    cola_prioridad = [(heuristica_manhattan(inicio, objetivo), 0, [inicio])]
    visitados = set()
    orden_visita = []

    while cola_prioridad:
        _, g_costo, camino = heapq.heappop(cola_prioridad)
        actual = camino[-1]

        if actual in visitados:
            continue
        visitados.add(actual)
        orden_visita.append(actual)

        if actual == objetivo:
            return camino, orden_visita, g_costo

        for vecino in obtener_vecinos(matriz, actual):
            if vecino not in visitados:
                nuevo_g = g_costo + 1
                nuevo_f = nuevo_g + heuristica_manhattan(vecino, objetivo)
                nuevo_camino = list(camino)
                nuevo_camino.append(vecino)
                heapq.heappush(cola_prioridad, (nuevo_f, nuevo_g, nuevo_camino))
    return None, orden_visita, float("inf")


def visualizar_laberinto_textual(
    matriz, camino_final, orden_visita, inicio, objetivo
):
    filas = len(matriz)
    columnas = len(matriz[0])

    camino_set = set(camino_final) if camino_final else set()
    visitados_set = set(orden_visita)

    print("\n==========================================")
    print("          MAPA DEL LABERINTO EN CONSOLA   ")
    print("==========================================")
    print("Leyenda: I=Inicio | O=Objetivo | █=Pared | *=Ruta | v=Visitado | ·=Vacio\n")

    print("   " + " ".join([str(c) for c in range(columnas)]))

    for r in range(filas):
        fila_str = f"{r}  "
        for c in range(columnas):
            coord = (r, c)
            if coord == inicio:
                fila_str += "I "
            elif coord == objetivo:
                fila_str += "O "
            elif coord in camino_set:
                fila_str += "* "
            elif coord in visitados_set:
                fila_str += "v "
            elif matriz[r][c] == 1:
                fila_str += "█ "
            else:
                fila_str += "· "
        print(fila_str)
    print("==========================================")


def ejecutar_busqueda_laberintos():
    matriz = obtener_laberinto_ejemplo()
    filas = len(matriz)
    columnas = len(matriz[0])

    print("\n--- BÚSQUEDA EN LABERINTOS (TEXTUAL) ---")
    print(f"Dimensiones del laberinto: {filas}x{columnas}")

    try:
        r_i = int(input(f"Fila inicial (0-{filas-1}): "))
        c_i = int(input(f"Columna inicial (0-{columnas-1}): "))
        r_f = int(input(f"Fila objetivo (0-{filas-1}): "))
        c_f = int(input(f"Columna objetivo (0-{columnas-1}): "))

        inicio = (r_i, c_i)
        objetivo = (r_f, c_f)
    except ValueError:
        print("Coordenadas no válidas.")
        return

    if not (0 <= r_i < filas and 0 <= c_i < columnas) or not (
        0 <= r_f < filas and 0 <= c_f < columnas
    ):
        print("Las coordenadas están fuera del rango del laberinto.")
        return

    if matriz[r_i][c_i] == 1 or matriz[r_f][c_f] == 1:
        print("¡El punto inicial o final chocan con una pared (1)!")
        return

    print("\nSeleccione algoritmo:")
    print("1. BFS\n2. DFS\n3. UCS\n4. A*")
    opc = input("Opción: ")

    camino, orden = None, []
    costo = "N/A"

    if opc == "1":
        camino, orden = bfs_laberinto(matriz, inicio, objetivo)
    elif opc == "2":
        camino, orden = dfs_laberinto(matriz, inicio, objetivo)
    elif opc == "3":
        camino, orden, costo = ucs_laberinto(matriz, inicio, objetivo)
    elif opc == "4":
        camino, orden, costo = a_estrella_laberinto(matriz, inicio, objetivo)
    else:
        print("Opción inválida.")
        return

    visualizar_laberinto_textual(matriz, camino, orden, inicio, objetivo)
    print(f"Orden de exploración de coordenadas:\n{orden}")
    print(f"\nCamino final (coordenadas): {camino}")
    print(f"Costo total (Número de pasos): {costo}")