# Sergio Franco Pineda (202116614), Lina Maria Ojeda (202112324)

"""

ANOTACIONES:

- Los componentes del grafo están compuestos por arcos entre 
  cofres que se abren con la misma llave.

- Se debe tener en cuenta el rango que cubre cada MST en la
  matriz.

- El rango que cubre cada MST en la matriz se calcula como
  (fila del nodo con mayor posicion de fila)*(la columna del 
  nodo con mayor posicion de columna).

- Los cofres se deben ir abriendo desde el MST que más area
  ocupa hasta el MST que en la matriz ocupa hasta el que 
  menos ocupa.

ALGORITMO:
  
1. Armar el grafo, en este grafo cada vertice se conecta con
   sus adyacentes.

2. Encontrar el area ocupada en la matriz por cada tipo de 
   cofre.

3. Poppear el tipo de cofre que mas area ocupa de una lista areas por cofre.

4. Desde cualquier cofre del tipo de cofre seleccionado en el paso anterior, 
   realizar DFS para identificar todos los nodos que son alcanzables desde 
   ahí y que además están dentro del area cubierta por el  tipo de cofre.
   Ir abriendo los cofres que se encuentren del tipo de cofre seleccionado,
   pero si se encuentra un cofre que ya está abierto en esa área, no se
   puede descifrar el mensaje.

5. Si no se encontró ningún cofre ya abierto, añadir el paso a una lista de
   pasos.

6 Repetir los pasos 3, 4 y 5 hasta haber poppeado todos los tipos de cofres.

INPUT:  

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

OUTPUT:




"""

import heapq

def crearGrafo_obtenerTipoCofreCofres(
        matriz: list[list[int]]
    ) -> tuple[dict[str, list[str]], dict[int, list[str]]]:

    """
    Function to create a graph from a matrix, each element of the matrix is
    conected to its neighbors. Also, creates a dictionary that maps each
    type of safe to its list of safes of that type.

    Args:
        matriz (list[list[int]]): The matrix to create the graph from.

    Returns:
        tuple[dict[str, list[str]], dict[int, list[str]]]: The first element
        is the graph represented as an adjacency list, the keys are the
        nodes and the values are the neighbors. Nodes are identified by his
        poition ij in the matrix. The second element is a dictionary that
        maps each type of safe to its list of safes of that type.
    """

    tipoCofre_cofres = {}
    lista_adyacencia = {}
    for fila in range(len(matriz)):
        for columna in range(len(matriz[fila])):
            nodo_adyacetes = []
            if 0 <= fila-1 < len(matriz) and 0 <= columna < len(matriz[fila]):
                nodo_adyacetes.append(str(fila-1)+str(columna)) # Los nodos están identificados por sus coordenadas
            if 0 <= fila+1 < len(matriz) and 0 <= columna < len(matriz[fila]):
                nodo_adyacetes.append(str(fila+1)+str(columna))
            if 0 <= fila < len(matriz) and 0 <= columna-1 < len(matriz[fila]):
                nodo_adyacetes.append(str(fila)+str(columna-1))
            if 0 <= fila < len(matriz) and 0 <= columna+1 < len(matriz[fila]):
                nodo_adyacetes.append(str(fila)+str(columna+1))
            nodo_identificador = str(fila)+str(columna)
            if matriz[fila][columna] not in tipoCofre_cofres:
                tipoCofre_cofres[matriz[fila][columna]] = [nodo_identificador]
            else:
                tipoCofre_cofres[matriz[fila][columna]].append(nodo_identificador)
            lista_adyacencia[nodo_identificador] = nodo_adyacetes
    
    return lista_adyacencia, tipoCofre_cofres

def obtener_areas(grafo: dict[str, list[str]],
                  matriz: list[list[int]],
                  llaves_cantidad: int
                  ) -> list[tuple[int, int, int, int, int, int]]:

    """
	Calculates the areas that cover the different types of safes in the
    matrix.

	Parameters:
	    - grafo (dict[str, list[str]]): The graph represented as an adjacency
          list, the keys are the nodes and the
          values are the neighbors. Nodes are identified by his poition ij in
          the matrix.
	    - matriz (list[list[int]]): The input matrix.
	    - llaves_cantidad (int): The number of different types of safes.

	Returns:
	    - areas (list[tuple[int, int, int, int, int, int]]): A list of tuples
          containing the area of each type of safe and its min and max row
          and column.

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

    # Calcula los indices limites de cada tipo de cofre
    stack = ["00"]
    nodos_visitados = ["00"]
    while stack:
        nodo_actual = stack.pop()
        nodo_actual_tipo_cofre = matriz[int(nodo_actual[0])][int(nodo_actual[1])]
        filas_minimas[nodo_actual_tipo_cofre-1] = int(nodo_actual[0])+1 if int(nodo_actual[0])+1 < filas_minimas[nodo_actual_tipo_cofre-1] else filas_minimas[nodo_actual_tipo_cofre-1]
        columnas_minimas[nodo_actual_tipo_cofre-1] = int(nodo_actual[1])+1 if int(nodo_actual[1])+1 < columnas_minimas[nodo_actual_tipo_cofre-1] else columnas_minimas[nodo_actual_tipo_cofre-1]
        filas_maximas[nodo_actual_tipo_cofre-1] = int(nodo_actual[0])+1 if int(nodo_actual[0])+1 > filas_maximas[nodo_actual_tipo_cofre-1] else filas_maximas[nodo_actual_tipo_cofre-1]
        columnas_maximas[nodo_actual_tipo_cofre-1] = int(nodo_actual[1])+1 if int(nodo_actual[1])+1 > columnas_maximas[nodo_actual_tipo_cofre-1] else columnas_maximas[nodo_actual_tipo_cofre-1]
        for nodo_adyacente in grafo[nodo_actual]:
            if nodo_adyacente not in nodos_visitados:
                stack.append(nodo_adyacente)
                nodos_visitados.append(nodo_actual)

    # Calcula el area de cada tipo de cofre
    areas = []
    for i in range(llaves_cantidad):
        fila_maxima = filas_maximas[i]-filas_minimas[i]+1 if filas_maximas[i]!=filas_minimas[i] else 1
        columna_maxima = columnas_maximas[i]-columnas_minimas[i]+1 if columnas_maximas[i]!=columnas_minimas[i] else 1
        areas.append((-fila_maxima*columna_maxima, i+1, filas_minimas[i], columnas_minimas[i], filas_maximas[i], columnas_maximas[i]))
    areas.sort(reverse=False)

    return areas

def abrir_cofres(areas: list[tuple[int, int, int, int, int, int]],
                 tipoCofre_cofres: dict[int, list[str]],
                 matriz_filas: int,
                 matriz_columnas: int,
                 grafo: dict[str, list[str]]) -> list[str]:
    
    """
    Opens the safes in the matrix.
    
    Parameters:
        - areas (list[tuple[int, int, int, int, int, int]]): A list of tuples
          containing the area of each type of safe and its min and max row
          and column.
        - tipoCofre_cofres (dict[int, list[str]]): A dictionary that maps
          each type of safe to its list of safes of that type.
        - matriz_filas (int): The number of rows in the matrix.
        - matriz_columnas (int): The number of columns in the matrix.
        - grafo (dict[str, list[str]]): The graph represented as an adjacency
          list, the keys are the nodes and the values are the neighbors.
          Nodes are identified by his poition ij in the matrix.
    
    Returns:
        - pasos (list[str]): A list of strings representing the steps to
          correctly open the safes in the matrix.
    """

    cofres_abiertos = [[False for _ in range(matriz_columnas)] for _ in range(matriz_filas)]
    pasos = []
    #print(areas)
    #print("\n")
    #print(tipoCofre_cofres)
    #print("\n")
    #print(grafo)
    #print("\n")
    
    # Abre los cofres desde el tipo de cofre mas grande al mas pequeño recorriendo el area de cada tipo de cofre
    while areas:
        _, tipo_cofre, fila_minima, columna_minima, fila_maxima, columna_maxima = heapq.heappop(areas)
        cofres = tipoCofre_cofres[tipo_cofre]
        cofre_inicial = cofres[0]
        stack = [cofre_inicial]
        visitados = [cofre_inicial]
        while stack:
            nodo_actual = stack.pop()
            if cofres_abiertos[int(nodo_actual[0])][int(nodo_actual[1])]:
                return ["NO SE PUEDE"]
            if nodo_actual in cofres:
                cofres_abiertos[int(nodo_actual[0])][int(nodo_actual[1])] = True
            for nodo_adyacente in grafo[nodo_actual]:
                if nodo_adyacente not in visitados and fila_minima <= int(nodo_adyacente[0])+1 <= fila_maxima and columna_minima <= int(nodo_adyacente[1])+1 <= columna_maxima:
                    stack.append(nodo_adyacente)
                    visitados.append(nodo_adyacente)
        pasos.append("{} {} {} {} {}".format(tipo_cofre, fila_minima, fila_maxima, columna_minima, columna_maxima))

    return pasos

def problema_p2(matriz: list[list[int]], llaves_cantidad: int) -> list[str]:
    
    """
    Function to solve the problem P2.
    
    Parameters:
        - matriz (list[list[int]]): The input matrix.
        - llaves_cantidad (int): The number of keys.
    
    Returns:
        - pasos (list[str]): A list of strings representing the steps to
          correctly open the safes in the matrix.
    """
    #print(matriz[0])
    #print(matriz[1])
    #print(matriz[2])
    #print(matriz[3])
    #print()

    grafo, tipoCofre_cofres = crearGrafo_obtenerTipoCofreCofres(matriz)
    areas = obtener_areas(grafo, matriz, llaves_cantidad)
    pasos = abrir_cofres(areas, tipoCofre_cofres, len(matriz), len(matriz[0]), grafo)

    return pasos

def main() -> None:
    """
    Reads the number of test cases from the user input and for each one test
    case creates the matrix and calls the function problema_p2 to solve the
    problem.
    
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
        pasos = problema_p2(matriz, int(llaves_cantidad))
        for paso in pasos:
            print(paso)

if __name__ == "__main__":
    main()

#print(problema_p2([[2, 2, 2, 2, 1], [2, 3, 4, 4, 1], [2, 3, 4, 4, 1], [2, 3, 2, 2, 4]], 4))
#print(problema_p2([[4, 4, 4, 4, 4], [3, 3, 3, 4, 4], [2, 2, 3, 4, 4], [1, 2, 3, 4, 4]], 4))