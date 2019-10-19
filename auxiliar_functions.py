# definindo x, y como 0 e 1 para melhor leitura do codigo
x, y = 0, 1

def dist(p1, p2):
    return ((p1[x]-p2[x])**2)+((p1[y]-p2[y]**2))


def sort_polar(points, p0):
    return sorted(points, key=lambda p1:  math.atan2(p1[y]-p0[y], p1[x]-p0[x]))


# orientacao < 0 = CCW
def orientation(p1, p2, p3):
    return (p2[y]-p1[y])*(p3[x]-p2[x]) - (p2[x]-p1[x])*(p3[y]-p2[y])


# giro relativo a segmento consecutivos, giro > 0 é a direita e < 0 é a esquerda
def orientation_consec(p0, p1, p2):
    a = (p1[x] - p0[x], p1[y] - p0[y])
    b = (p2[x] - p0[x], p2[y] - p0[y])
    return a[x]*b[y] - b[x]*a[y]


def swap(pontos, i, j):
    v = pontos[i]
    pontos[i] = pontos[j]
    pontos[j] = v
    return pontos
    

def getMinIndex(pontos):
    min_index = 0
    for i in range(1, len(pontos)):
        if pontos[i][y] < pontos[min_index][y]:
            min_index = i
        elif pontos[i][y] == pontos[min_index][y] and pontos[i][x] < pontos[min_index][x]:
            min_index = i
    return min_index


def generate_points(n, mu, std):
    x = np.random.normal(mu, std, n)
    y = np.random.normal(mu, std, n)
    points = []
    for i in range(len(x)):
        points.append((x[i], y[i]))
    points = list(set(points))
    return points
