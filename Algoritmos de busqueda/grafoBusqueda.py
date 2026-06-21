import collections
import heapq

def obtener_grafo_ejemplo():
    # Formato: nodo: {vecino: costo}
    grafo = {
        "A": {"B": 1, "C": 4},
        "B": {"A": 1, "D": 5, "E": 2},
        "C": {"A": 4, "F": 3},
        "D": {"B": 5, "G": 2},
        "E": {"B": 2, "G": 6},
        "F": {"C": 3, "G": 1},
        "G": {"D": 2, "E": 6, "F": 1},
    }

    # Heurística aproximada hacia el nodo objetivo 'G'
    heuristica_g = {
        "A": 6,
        "B": 4,
        "C": 4,
        "D": 2,
        "E": 3,
        "F": 1,
        "G": 0,
    }

    return grafo, heuristica_g


def bfs_grafo(grafo, inicio, objetivo):
    cola = collections.deque([[inicio]])
    visitados = set()
    orden_visita = []

    while cola:
        camino = cola.popleft()
        nodo = camino[-1]

        if nodo not in visitados:
            visitados.add(nodo)
            orden_visita.append(nodo)

            if nodo == objetivo:
                return camino, orden_visita

            for vecino in grafo.get(nodo, {}):
                nuevo_camino = list(camino)
                nuevo_camino.append(vecino)
                cola.append(nuevo_camino)
    return None, orden_visita


def dfs_grafo(grafo, inicio, objetivo):
    pila = [[inicio]]
    visitados = set()
    orden_visita = []

    while pila:
        camino = pila.pop()
        nodo = camino[-1]

        if nodo not in visitados:
            visitados.add(nodo)
            orden_visita.append(nodo)

            if nodo == objetivo:
                return camino, orden_visita

            for vecino in reversed(list(grafo.get(nodo, {}).keys())):
                nuevo_camino = list(camino)
                nuevo_camino.append(vecino)
                pila.append(nuevo_camino)
    return None, orden_visita


def ucs_grafo(grafo, inicio, objetivo):
    cola_prioridad = [(0, [inicio])]
    visitados = set()
    orden_visita = []

    while cola_prioridad:
        costo, camino = heapq.heappop(cola_prioridad)
        nodo = camino[-1]

        if nodo in visitados:
            continue

        visitados.add(nodo)
        orden_visita.append(nodo)

        if nodo == objetivo:
            return camino, orden_visita, costo

        for vecino, peso in grafo.get(nodo, {}).items():
            if vecino not in visitados:
                nuevo_camino = list(camino)
                nuevo_camino.append(vecino)
                heapq.heappush(cola_prioridad, (costo + peso, nuevo_camino))

    return None, orden_visita, float("inf")


def a_estrella_grafo(grafo, inicio, objetivo, heuristica):
    cola_prioridad = [(heuristica.get(inicio, 0), 0, [inicio])]
    visitados = set()
    orden_visita = []

    while cola_prioridad:
        _, g_costo, camino = heapq.heappop(cola_prioridad)
        nodo = camino[-1]

        if nodo in visitados:
            continue

        visitados.add(nodo)
        orden_visita.append(nodo)

        if nodo == objetivo:
            return camino, orden_visita, g_costo

        for vecino, peso in grafo.get(nodo, {}).items():
            if vecino not in visitados:
                nuevo_g = g_costo + peso
                nuevo_f = nuevo_g + heuristica.get(vecino, 0)
                nuevo_camino = list(camino)
                nuevo_camino.append(vecino)
                heapq.heappush(cola_prioridad, (nuevo_f, nuevo_g, nuevo_camino))

    return None, orden_visita, float("inf")

def visualizar_grafo_textual(grafo, camino_final, orden_visita):
    print("\n==========================================")
    print("         VISUALIZACIÓN DEL RECORRIDO       ")
    print("==========================================")
    print(f"Orden de exploración: {' -> '.join(orden_visita)}")

    if camino_final:
        print(f"Camino encontrado   : {' -> '.join(camino_final)}")
    else:
        print("Camino encontrado   : No se encontró ruta.")
    print("------------------------------------------")

    print("\nEstructura del Grafo (Aristas y costos):")
    for nodo, vecinos in grafo.items():
        conexiones = ", ".join([f"{v}(peso:{c})" for v, c in vecinos.items()])
        marcador = ""
        if camino_final and nodo in camino_final:
            marcador = " [Camino]"
        elif nodo in orden_visita:
            marcador = " [Visitado]"

        print(f"  Nodo {nodo}{marcador} -> {conexiones}")


def ejecutar_busqueda_grafos():
    grafo, heuristica = obtener_grafo_ejemplo()
    print("\n--- BÚSQUEDA EN GRAFOS (TEXTUAL) ---")
    print(f"Nodos disponibles: {list(grafo.keys())}")
    inicio = input("Nodo inicial (Ej: A): ").strip().upper()
    objetivo = input("Nodo objetivo (Ej: G): ").strip().upper()

    if inicio not in grafo or objetivo not in grafo:
        print("Nodos inválidos.")
        return

    print("\nSeleccione algoritmo:")
    print("1. BFS\n2. DFS\n3. UCS\n4. A*")
    opc = input("Opción: ")

    camino, orden = None, []
    costo = "N/A"

    if opc == "1":
        camino, orden = bfs_grafo(grafo, inicio, objetivo)
    elif opc == "2":
        camino, orden = dfs_grafo(grafo, inicio, objetivo)
    elif opc == "3":
        camino, orden, costo = ucs_grafo(grafo, inicio, objetivo)
    elif opc == "4":
        camino, orden, costo = a_estrella_grafo(
            grafo, inicio, objetivo, heuristica
        )
    else:
        print("Opción inválida.")
        return

    visualizar_grafo_textual(grafo, camino, orden)
    print(f"\nCosto total del camino: {costo}")