import math
import numpy as np

## ----------------------------------------------------------------- ##
# ----------------- FUNCOES AUXLIARES E PRIMITIVAS ----------------- ##

# definindo x, y como 0 e 1 para melhor leitura do codigo
x, y = 0, 1

# retorna a distancia entre dois pontos
def dist(p1, p2):
    return ((p1[x]-p2[x])**2)+((p1[y]-p2[y]**2))


# ordena o vetor com base nas suas coordenadas polares
def sort_polar(points, p0):
    return sorted(points, key=lambda p1:  math.atan2(p1[y]-p0[y], p1[x]-p0[x]))


# orientacao < 0 = CCW
def orientation(p1, p2, p3):
    v = (p2[y]-p1[y])*(p3[x]-p2[x]) - (p2[x]-p1[x])*(p3[y]-p2[y])
    if v < 0:
        return 'left'
    elif v > 0:
        return 'right'
    else:
        return 'colienar'


# giro relativo a segmento consecutivos, giro > 0 é a direita e < 0 é a esquerda
def orientation_consec(p0, p1, p2):
    a = (p1[x] - p0[x], p1[y] - p0[y])
    b = (p2[x] - p0[x], p2[y] - p0[y])
    v = a[x]*b[y] - b[x]*a[y]
    if v < 0:
        return 'left'
    elif v > 0:
        return 'right'
    else:
        return 'colienar'

# retorna o indice do menor valor do vetor
def getMinIndex(pontos):
    min_index = 0
    for i in range(1, len(pontos)):
        if pontos[i][y] < pontos[min_index][y]:
            min_index = i
        elif pontos[i][y] == pontos[min_index][y] and pontos[i][x] < pontos[min_index][x]:
            min_index = i
    return min_index

# gera n pontos aleatorios (x, y) dado uma media um desvio padrao
def generate_points(n, mu, std):
    x = np.random.normal(mu, std, n)
    y = np.random.normal(mu, std, n)
    points = []
    for i in range(len(x)):
        points.append((x[i], y[i]))
    points = list(set(points))
    return points

## ----------------------------------------------------------------- ##

## ----------------------------------------------------------------- ##
# --------------------- FUNCOES DOS ALGORITMOS --------------------- ##

def graham_scan(points):
    x, y = 0, 1
    
    # escolhe o point com menor coordenada Y
    min_index = getMinIndex(points)
    
    # colocando o menor valor no inicio da lista
    v = points[min_index]
    points[min_index] = points[0]
    points[0] = v
    
    # ordenamos de acordo com a coordenada polar
    sorted_points = sort_polar(points[1:], points[0])
    
    stack = []
    
    stack.append(points[0])
    stack.append(sorted_points[0])
    stack.append(sorted_points[1])
    
    for point in sorted_points[2:]:
        while orientation(stack[-2], stack[-1], point) != 'left':
            stack.pop()
            
        stack.append(point)
        
    return stack


def jarvis_march(points):
    x, y = 0, 1
    
    hull = []
    min_index = getMinIndex(points)

    i = min_index
    hull.append(points[i])

    while True:
        # o ponto atual sera o mod do nº de pontos, para q na ultima iteracao nao verifique um ponto inexistente
        curr_p = (i + 1) % len(points)
        
        for j in range(len(points)):
            if i != j:
                turn = orientation(points[i], points[j], points[curr_p])
                
                if turn == 'right':
                    curr_p = j
                    
                # caso sejam colineares, deixe apenas com a maior distancia
                elif turn == 'colinear' and dist(points[j], points[i]) > dist(points[curr_p], points[i]):
                    curr_p = j
                    
        i = curr_p
        
        if i == min_index:
            break
            
        hull.append(points[i])
        
    return hull

def incremental(points):
    x, y = 0, 1
    
    # ordenamos em relaço ao eixo X
    s = sorted(points)
    
    l = {} # vetor q guarda os indices dos pontos abaixo (em relacao ao eixo y) do ponto mais a direita
    u = {} # vetor q guarda os indices dos pontos acima (em relacao ao eixo y)
    
    l[0], u[0], l[1], u[1] = 1, 1, 0, 0
    
    hull = []
    hull.append(s[0])
    hull.append(s[1])

    # s é o vetor ordenado em relação ao eixo X
    for i in range(2, len(s)):
        hull.append(s[i])

        # verificamos se o ponto a ser inserido est acima ou abaixo do mais a direita
        if s[i][y] > s[i-1][y]:
            l[i] = i-1
            u[i] = u[i-1]
        else:
            l[i] = l[i-1]
            u[i] = i-1
        
        l[u[i]] = i
        u[l[i]] = i
        
        # primeiro atualizamos a borda inferior
        # calculamos P -> Pi -> Pi-1
        l_1, l_2 = l[i], l[l[i]]
        while orientation_consec(s[i], s[l_1], s[l_2]) == 'right':
            l[i] = l_2
            u[l_2] = i
            
            # removemos Pi 
            hull = [p for p in hull if p != s[l_1]]
            
            l_1 = l_2
            l_2 = l[l_1]
            
        # agora atualizamos a borda superior
        # calculamos P -> Pi+2 -> Pi+1
        u_1, u_2 = u[i], u[u[i]]
        while orientation_consec(s[i], s[u_2], s[u_1]) == 'right':
            u[i] = u_2
            l[u_2] = i
            
            # removemos Pi 
            hull = [p for p in hull if p != s[u_1]]
            
            u_1 = u_2
            u_2 = u[u_1]

    return hull
