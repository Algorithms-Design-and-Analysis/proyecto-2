# Sergio Franco Pineda (202116614), Lina Maria Ojeda (202112324)

"""

- Los componentes del grafo están compuestos por arcos entre cofres que se abren con la misma llave.
- Se debe tener en cuenta el rango que cubre cada MST en la matriz.
- El rango que cubre cada MST en la matriz se calcula como (fila del nodo con mayor posicion de fila)*(la columna del 
  nodo con mayor posicion de columna).
- Los cofres se deben ir abriendo desde el MST que más area ocupa hasta el MST que en la matriz ocupa hasta el que 
  menos ocupa.

1. Armar el grafo, en este grafo cada vertice se conecta con sus adyacentes con arcos de peso 1
2. Encontrar un MST donde por cada componente del grafo.
3. Empezar a abrir los cofres desde el MST que mas area ocupa hasta el MST que menos ocupa.
    3.1 Poppear el MST que mas area ocupa de una lista de MSTs.
    3.2 Desde cualquier nodos presente en el MST realizar DFS para identificar todos los nodos que son alcanzables 
        desde ahí y que además están dentro del area cubierta por el MST, pero que no han sidos ya abiertos con otra
        llave, en caso de que en el area se enccuentre uno que ya fue abierto, se retorna "NO SE PUEDE".

3
4 5 5
2 2 2 2 1
2 3 5 5 1
2 3 5 5 1
2 3 4 4 5
4 5 4
2 2 2 2 1
2 3 4 4 1
2 3 4 4 1
2 3 1 3 4
2 2 2
1 1
1 2

1
4 5 5
2 2 2 2 1
2 3 5 5 1
2 3 5 5 1
2 3 4 4 5

"""

import heapq

def crear_grafo(matriz: list[list[int]]) -> dict[str, list[str]]:
    
    """
    Function to create a graph from a matrix, each element of the matrix is conected to its neighbors.

    Args:
        matriz (list[list[int]]): The matrix to create the graph from.

    Returns:
        dict[str, list[str]]: The graph represented as an adjacency list, the keys are the nodes and the values are 
        the neighbors. Nodes are identified by his poition ij in the matrix.
    """

    lista_adyacencia = {}
    for fila in range(len(matriz)):
        for columna in range(len(matriz[fila])):
            nodo_adyacetes = []
            if 0 <= fila-1 < len(matriz) and 0 <= columna < len(matriz[fila]):
                nodo_adyacetes.append(str(fila-1)+str(columna))
            if 0 <= fila+1 < len(matriz) and 0 <= columna < len(matriz[fila]):
                nodo_adyacetes.append(str(fila+1)+str(columna))
            if 0 <= fila < len(matriz) and 0 <= columna-1 < len(matriz[fila]):
                nodo_adyacetes.append(str(fila)+str(columna-1))
            if 0 <= fila < len(matriz) and 0 <= columna+1 < len(matriz[fila]):
                nodo_adyacetes.append(str(fila)+str(columna+1))
            nodo_identificador = str(fila)+str(columna)
            lista_adyacencia[nodo_identificador] = nodo_adyacetes
    
    return lista_adyacencia

def obtener_areas(grafo, matriz: list[list[int]], llaves_cantidad: int) -> list[tuple[int, int]]:

    """
	Calculates the areas that cover the different types of safes in the matrix.

	Parameters:
	    - grafo (dict[str, list[str]]): The graph represented as an adjacency list, the keys are the nodes and the
          values are the neighbors. Nodes are identified by his poition ij in the matrix.
	    - matriz: The input matrix.
	    - llaves_cantidad: The number of different types of safes.

	Returns:
	    - areas: A list of tuples containing the area of each type of safe.

	"""
    
    # La posición i-1 corresponde al tipo de cofre i
    filas_minimas = []
    columnas_minimas = []
    filas_maximas = []
    columnas_maximas = []
    for i in range(llaves_cantidad):
        filas_minimas.append(float('inf'))
        columnas_minimas.append(float('inf'))
        filas_maximas.append(0)
        columnas_maximas.append(0)

    stack = ["00"]
    nodos_visitados = ["00"]
    while len(stack) > 0:
        nodo_actual = stack.pop()
        tipo_cofre = matriz[int(nodo_actual[0])][int(nodo_actual[1])]
        filas_minimas[tipo_cofre-1] = int(nodo_actual[0])+1 if int(nodo_actual[0])+1 < filas_minimas[tipo_cofre-1] else filas_minimas[tipo_cofre-1]
        columnas_minimas[tipo_cofre-1] = int(nodo_actual[1])+1 if int(nodo_actual[1])+1 < columnas_minimas[tipo_cofre-1] else columnas_minimas[tipo_cofre-1]
        filas_maximas[tipo_cofre-1] = int(nodo_actual[0])+1 if int(nodo_actual[0])+1 > filas_maximas[tipo_cofre-1] else filas_maximas[tipo_cofre-1]
        columnas_maximas[tipo_cofre-1] = int(nodo_actual[1])+1 if int(nodo_actual[1])+1 > columnas_maximas[tipo_cofre-1] else columnas_maximas[tipo_cofre-1]
        for nodo_adyacente in grafo[nodo_actual]:
            if nodo_adyacente not in nodos_visitados:
                stack.append(nodo_adyacente)
                nodos_visitados.append(nodo_actual)

    areas = []
    for i in range(llaves_cantidad):
        fila_maxima = filas_maximas[i]-filas_minimas[i]+1 if filas_maximas[i]!=filas_minimas[i] else 1
        columna_maxima = columnas_maximas[i]-columnas_minimas[i]+1 if columnas_maximas[i]!=columnas_minimas[i] else 1
        areas.append((fila_maxima*columna_maxima, i+1))
    areas.sort(reverse=True)

    return areas

def problema_p2(matriz: list[list[int]], llaves_cantidad: int) -> list[str]:

    grafo = crear_grafo(matriz)
    areas = obtener_areas(grafo, matriz, llaves_cantidad)

    return areas

def main() -> None:
    """
    Reads the number of test cases from the user input and for each one test case creates the matrix 
    and calls the function problema_p2 to solve the problem.
    
    Parameters:
        None
    
    Returns:
        None
    """
    casos_numero = int(input())
    for _ in range(casos_numero):
        filas_cantidad, _, llaves_cantidad = input().split(" ")
        matriz = []
        for _ in range(int(filas_cantidad)):
            fila = input().split(" ")
            fila = list(map(int, fila))
            matriz.append(fila)
        print(problema_p2(matriz, int(llaves_cantidad)))

if __name__ == "__main__":
    main()
#print(problema_p2([[2, 2, 2, 2, 1], [2, 3, 5, 5, 1], [2, 3, 5, 5, 1], [2, 3, 4, 4, 5]], 5))
