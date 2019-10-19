def graham_scan(pontos):
    # escolhe o ponto com menor coordenada Y
    min_index = getIndexMin(pontos)
    
    pontos = swap(pontos, min_index, 0)
    
    # ordenamos de acordo com a coordenada polar
    sorted_pontos = sorted(pontos[1:], key = lambda p1: math.atan2(p1[y]-pontos[0][y], p1[x]-pontos[0][x]))
    pilha = []
    
    pilha.append(pontos[0])
    pilha.append(sorted_pontos[0])        
    pilha.append(sorted_pontos[1])
    
    for ponto in sorted_pontos[2:]:
        while len(pilha) > 1 and calc_orientacao(pilha[-2], pilha[-1], ponto) >= 0:
            pilha.pop()
            
        pilha.append(ponto)
    
    return pilha


def jarvis_march(pontos):
    
    convex_hull = []
    
    min_index = getIndexMin(pontos)
    
    i = min_index
    convex_hull.append(pontos[i])
    
    while True:
        curr_p = (i + 1) % len(pontos)
        
        for j in range(len(pontos)):
            if i != j:
                angulo = calc_orientacao(pontos[i], pontos[j], pontos[curr_p])
              
                if angulo > 0:
                    curr_p = j
                elif angulo == 0 and calc_dist(pontos[j], pontos[i]) > calc_dist(pontos[curr_p], pontos[i]):
                    curr_p = j
        i = curr_p
        if i == min_index:
            break
        convex_hull.append(pontos[curr_p])
    
    return convex_hull

def incremental(points):
    s = sorted(points, key = lambda p: p[0])
    
    n = {} # vetor q guarda os indices dos pontos acima (em relacao ao eixo y) do ponto mais a direita
    p = {} # vetor q guarda os indices dos pontos abaixo (em relacao ao eixo y)
    
    n[0], p[0], n[1], p[1] = 1, 1, 0, 0
    
    hull = []
    hull.append(s[0])
    hull.append(s[1])
    
    for i in range(2, len(s)):
        hull.append(s[i])
        
        if s[i][y] > s[i-1][y]:
            n[i] = i-1
            p[i] = p[i-1]
        else:
            n[i] = n[i-1]
            p[i] = i-1
        
        n[p[i]] = i
        p[n[i]] = i
        
        n_1, n_2 = n[i], n[n[i]]
        while orientation_consec(s[i], s[n_1], s[n_2]) > 0:
            n[i] = n_2
            p[n_2] = i
            
            hull = [p for p in hull if p != s[n_1]]
            
            n_1 = n_2
            n_2 = p[n_1]
            
        p_1, p_2 = p[i], p[p[i]]
        while orientation_consec(s[i], s[p_2], s[p_1]) > 0:
            p[i] = p_2
            n[p_2] = i
            
            hull = [p for p in hull if p != s[p_1]]
            
            p_1 = p_2
            p_2 = n[p_1]
            
    return hull
