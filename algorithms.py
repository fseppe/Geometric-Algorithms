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
