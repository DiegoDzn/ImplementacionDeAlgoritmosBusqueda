import grafoBusqueda
import laberintoBusqueda


def menu():
    while True:
        print("   IMPLEMENTACIÓN DE ALGORITMOS DE BÚSQUEDA   ")
        print("")
        print("1. Ejecutar en Grafos / Árboles (Parte 1)")
        print("2. Ejecutar en Laberinto de Matrices (Parte 2)")
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            grafoBusqueda.ejecutar_busqueda_grafos()
        elif opcion == "2":
            laberintoBusqueda.ejecutar_busqueda_laberintos()


if __name__ == "__main__":
    menu()