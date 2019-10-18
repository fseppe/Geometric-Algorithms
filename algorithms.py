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
