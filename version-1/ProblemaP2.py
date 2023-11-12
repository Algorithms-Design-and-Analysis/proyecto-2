# Sergio Franco Pineda (202116614), Lina Maria Ojeda (202112324)

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
                  ) -> tuple[list[tuple[int, int, int, int, int, int]], dict[int, int]]:

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
        - tuple[list[tuple[int, int, int, int, int, int]], dict[int, int]]: A
          tuple containing two elements. The first element is a list of tuples
          containing the area of each type of safe and its min and max row and
          column and the second element is a dictionary that maps each type of
          safe to its area.

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
    tipoCofre_area = {}
    for i in range(llaves_cantidad):
        fila_maxima = filas_maximas[i]-filas_minimas[i]+1 if filas_maximas[i]!=filas_minimas[i] else 1
        columna_maxima = columnas_maximas[i]-columnas_minimas[i]+1 if columnas_maximas[i]!=columnas_minimas[i] else 1
        areas.append((-fila_maxima*columna_maxima, i+1, filas_minimas[i], columnas_minimas[i], filas_maximas[i], columnas_maximas[i]))
        tipoCofre_area[i+1] = (-fila_maxima*columna_maxima, i+1, filas_minimas[i], columnas_minimas[i], filas_maximas[i], columnas_maximas[i])
    areas.sort(reverse=False)

    return areas, tipoCofre_area

def cerrar_cofres(tipo_cofre_cerrar:int,
                  cofres_abiertos:list[list[bool]],
                  tipoCofre_cofres:dict[int, list[str]]
                  )->list[list[bool]]:
    
    """
    Closes the safes in the matrix.
    
    Parameters:
        - tipo_cofre_cerrar (int): The type of cofre to be closed.
        - cofres_abiertos (list[list[bool]]): A list of lists that represents
          the status of each cofre in the matrix.
        - tipoCofre_cofres (dict[int, list[str]]): A dictionary that maps
          each type of safe to its list of safes of that type.
    
    Returns:
        - cofres_abiertos (list[list[bool]]): A list of lists that represents
          the status of each cofre in the matrix.
    """
    
    for cofre in tipoCofre_cofres[tipo_cofre_cerrar]:
        cofres_abiertos[int(cofre[0])][int(cofre[1])] = False
        
    return cofres_abiertos

def abrir_cofres(areas: list[tuple[int, int, int, int, int, int]],
                 tipoCofre_cofres: dict[int, list[str]],
                 matriz: list[list[int]],
                 matriz_filas: int,
                 matriz_columnas: int,
                 grafo: dict[str, list[str]],
                 tipoCofre_area: dict[int, int]) -> list[str]:
    
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
    
    while areas:
        area, tipo_cofre, fila_minima, columna_minima, fila_maxima, columna_maxima = heapq.heappop(areas)
        cofres = tipoCofre_cofres[tipo_cofre]
        cofre_inicial = cofres[0]
        stack = [cofre_inicial]
        visitados = [cofre_inicial]
        retroceder = False
        # En general, se tratan de abrir los cofres del mas grande al mas pequeño a excepción de un caso especial
        while stack:
            nodo_actual = stack.pop()
            nodo_actual_tipo = matriz[int(nodo_actual[0])][int(nodo_actual[1])]
            # Si el area del tipo de cofre que se enucuentra en el área es mayor al area del tipo de cofre que se está recorriendo en el momento se vuelven a cerrar los cofres de ese tipo de cofre para poder abrir el que se está abriendo ahora primero
            if cofres_abiertos[int(nodo_actual[0])][int(nodo_actual[1])] and -tipoCofre_area[nodo_actual_tipo][0] > -area and tipoCofre_area[nodo_actual_tipo] not in areas:
                cofres_abiertos = cerrar_cofres(nodo_actual_tipo, cofres_abiertos, tipoCofre_cofres)
                heapq.heappush(areas, tipoCofre_area[nodo_actual_tipo])
                retroceder = True
            # Si se encuentra un cofre en el area que ya esta abierto y es de un tipo de cofre que tiene un area menor o igual a la area del tipo de cofre que se esta recorriendo en el momento
            if not retroceder and cofres_abiertos[int(nodo_actual[0])][int(nodo_actual[1])]:
                return ["NO SE PUEDE"]
            # Si se pueden abrir los cofres sin problemas
            if nodo_actual in cofres:
                cofres_abiertos[int(nodo_actual[0])][int(nodo_actual[1])] = True
            for nodo_adyacente in grafo[nodo_actual]:
                if nodo_adyacente not in visitados and fila_minima <= int(nodo_adyacente[0])+1 <= fila_maxima and columna_minima <= int(nodo_adyacente[1])+1 <= columna_maxima:
                    stack.append(nodo_adyacente)
                    visitados.append(nodo_adyacente)
                    
        paso = "{} {} {} {} {}".format(tipo_cofre, fila_minima, fila_maxima, columna_minima, columna_maxima)
        # Si el paso de abir un tipo de cofre ya se encontraba pero se volvio a cerrar por el caso especial, se elimna el que ya estaba y se vuelve añadir de último para mantener el orden de la lista de pasos
        if paso in pasos:
            pasos.remove(paso)
        pasos.append(paso)

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

    grafo, tipoCofre_cofres = crearGrafo_obtenerTipoCofreCofres(matriz)
    areas, tipoCofre_area = obtener_areas(grafo, matriz, llaves_cantidad)
    pasos = abrir_cofres(areas, tipoCofre_cofres, matriz, len(matriz), len(matriz[0]), grafo, tipoCofre_area)

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