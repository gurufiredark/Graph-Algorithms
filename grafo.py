# Felipe Chatalov 118992
# Lucas Beluomini 120111
# Gabriel Rodrigues 118038

from re import X


class Vertice():
    def __init__(self, id):
        self.id = id
        self.conexoes = []
        self.visited = False
        
        # bfs
        self.bfs_pai = None

        # dfs   
        self.dfs_pai = None

        # bellmanFord
        self.bf_pai = None
        self.bf_distancia = float('inf')

        # dijkstra
        self.dj_pai = None
        self.dj_distancia = float('inf')

        # prim 
        self.pm_pai = None
        self.pm_distancia = float('inf')

        # ford_fulkerson
        self.ff_pai = None


    def __str__(self):
        return f'id: {self.id}'

    def addAresta(self, dst, weight):
        self.conexoes.append(Aresta(dst, weight))

    def getArestaFromVertice(self, dst):
        for aresta in self.conexoes:
            if aresta.dst == dst:
                return aresta
    def getArestaMenorCusto(self):
        menor = self.conexoes[0]
        for aresta in self.conexoes:
            if aresta.weight < menor.weight:
                menor = aresta
        return menor

class Aresta():
    def __init__(self, dst, w, **kwargs):
        self.dst = dst
        self.w = w
        self.capacity = kwargs.get('capacity', float('inf'))
        self.flow = 0



def bfs(g, pai):
    print("BFS")
    for v in g:
        v.visited = False
        v.bfs_pai = None

    q = []
    seq = []

    q.append(pai)
    seq.append(pai)

    print(f'Comecou em {pai.id}')

    while q != []:
        pai = q.pop(0)
        pai.visited = True  

        for ar in pai.conexoes:
            if not ar.dst.visited:
                ar.dst.bfs_pai = pai
                q.append(ar.dst)
                seq.append(ar.dst)
                ar.dst.visited = True
                print(f'-> {ar.dst.id} ', end='')
        if q == []:
            for v in g:
                if v.visited == False:
                    q.append(v)
                    break

    print(f'\nSequencia de visita em lista: ')
    for v in seq:
        print(v.id, end=" ") 
    print('\n')
    return seq
def dfs(g, pai):
    print("DFS")
    for v in g:
        v.visited = False
        v.dfs_pai = None
    
    q = []
    seq = []

    q.append(pai)
    seq.append(pai)

    print(f'Comecou em {pai.id}')

    while q != []:
        pai = q.pop(0)
        pai.visited = True  

        for ar in pai.conexoes:
            if not ar.dst.visited:
                q = [ar.dst] + q
                ar.dst.dfs_pai = pai
                seq.append(ar.dst)
                ar.dst.visited = True
                print(f'-> {ar.dst.id} ', end='')
        if q == []:
            for v in g:
                if v.visited == False:
                    q.append(v)
                    break

    print(f'\nSequencia de visita em lista: ')
    for v in seq:
        print(v.id, end=" ") 
    print('\n')
    return seq

def relax(p, f):
    # print(f'\n relaxando {p.id} -> {f.id}')
    if p.bf_distancia + p.getArestaFromVertice(f).w < f.bf_distancia:
        f.bf_distancia = p.bf_distancia + p.getArestaFromVertice(f).w
        # nao eh usado no algoritmo mas pode se usado para retorna do 
        # node atual até o pai pelo melhor caminho (menor custo)
        f.bf_pai = p
def bellman_ford(vertices, pai):
    print("Bellman-Ford")
    # reset node configs
    for v in vertices:
        v.bf_distancia = float('inf')
        v.bf_pai = None

    pai.bf_distancia = 0
    for v in vertices[:-1]:
        for ar in v.conexoes:
            relax(v, ar.dst)
    for v in vertices:
        print(f'{v.id} -> {v.bf_distancia if v.bf_distancia != float("inf") else f"SEM CAMINHO PARTINDO DE {pai.id}"}')
    print('\n')

def dijkstra(vertices, pai):
    print("Dijkstra")
    # reset node configs

    for v in vertices:
        v.dj_distancia = float('inf')
        v.dj_pai = None
        v.visited = False

    print(f'Comecou em {pai.id}')
    pai.dj_distancia = 0
    q = []
    q.append(pai)
    while q != []:
        p = q.pop(0)
        p.visited = True
        for ar in p.conexoes:
            if ar.dst.visited == False:
                q.append(ar.dst)
                ar.dst.visited = True
            if p.dj_distancia + ar.w < ar.dst.dj_distancia:
                ar.dst.dj_distancia = p.dj_distancia + ar.w
                ar.dst.dj_pai = p
    
    for v in vertices:
        print(f'{v.id} -> {v.dj_distancia if v.dj_distancia != float("inf") else f"SEM CAMINHO PARTINDO DE {pai.id}"}')
    print()

# funciona com grafo orientado com valores negativos
def floyd_warshall(vertices):
    print("Floyd-Warshall")
    d = [[float('inf') for i in range(len(vertices))] for j in range(len(vertices))]
    pred = [[float('inf') for i in range(len(vertices))] for j in range(len(vertices))]
    for i in range(len(vertices)):
        for j in range(len(vertices)):
            if i == j:
                d[i][j] = 0
            elif vertices[i].getArestaFromVertice(vertices[j]):
                d[i][j] = vertices[i].getArestaFromVertice(vertices[j]).w
            pred[i][j] = i

    # for i in range(len(vertices)):
    #     for j in range(len(vertices)):
    #         print(f'{d[i][j]}\t', end='')
    #     print()

    for i in range(len(vertices)):
        for j in range(len(vertices)):
            for k in range(len(vertices)):
                if d[i][j] > d[i][k] + d[k][j]:
                    d[i][j] = d[i][k] + d[k][j]
                    pred[i][j] = pred[k][j]

    for i in range(len(vertices)):
        for j in range(len(vertices)):
            print(f'{d[i][j]}\t', end='')
        print()

    print()
    for i in range(len(vertices)):
        for j in range(len(vertices)):
            print(f'{pred[i][j]}\t', end='')
        print()
    print()
    # pred funciona assim:
    # caso vc queria saber o caminho de menor distancia do vertice 0 ao 6
    # vc olha pred[0][6] e ve que o valor eh 2,
    # entao vc olha o menor caminho de 0 a 2, ou seja, pred[0][2] e ve que o valor eh 1,
    # entao vc olha pred[0][1] e ve que o valor eh 0, que eh o vertice que queremos comecar
    # logo temos o menor caminho de 0 ate 6, 0->1->2->6
    # neste caso, menor caminho == menor custo

    return d, pred

def prim(vertices, pai):
    print("Prim")
    for v in vertices:
        v.pm_distancia = float('inf')
        v.pm_pai = None
        v.visited = False

    v = len(vertices)
    noEdge = 0
    selected = [0]*v
    selected[0] = True
    
    l = []

    while noEdge < v-1:
        minimum = float('inf')
        x, y = 0, 0
        for i in range(v):
            if selected[i] == True:
                for j in range(v):
                    if not selected[j] and vertices[i].getArestaFromVertice(vertices[j]):
                        if vertices[i].getArestaFromVertice(vertices[j]).w < minimum:
                            minimum = vertices[i].getArestaFromVertice(vertices[j]).w
                            x = i
                            y = j


        print(f'{vertices[x].id} -> {vertices[y].id}')
        selected[y] = True
        if vertices[x] not in l:
            l.append(vertices[x])
        if vertices[y] not in l:
            l.append(vertices[y])
        noEdge+=1
    for i in range(len(l)):
        print(f'{l[i].id} ', end='')
    print()
    return l

def ff_bfs(g, pai, dst):
    print("FF-BFS")
    for v in g:
        v.visited = False
        v.ff_pai = None

    q = []
    seq = []

    q.append(pai)
    seq.append(pai)

    # print(f'Comecou em {pai.id}')

    while q != []:
        p = q.pop(0)
        p.visited = True  

        for ar in p.conexoes:
            if not ar.dst.visited and ar.capacity > 0:
                ar.dst.ff_pai = p
                print(f'{p.id} -> {ar.dst.id}')
                q.append(ar.dst)
                seq.append(ar.dst)
                ar.dst.visited = True
                # print(f'-> {ar.dst.id} ', end='')
        # if q == []:
        #     for v in g:
        #         if v.visited == False:
        #             q.append(v)
        #             break

    
    if pai not in seq or dst not in seq:
        print(f"sem caminho de {pai.id} ate {dst.id}")
        return None

    # print(f'\nSequencia de visita em lista: ')
    # for v in seq:
    #     print(v.id, end=" ") 
    # print('\n')
    return seq
# update_flow recebe a lista de arestas de s a t no grafo
# para cada aresta na lista, atualiza o fluxo de s a t
# acha a aresta com menor capacidade e atualiza o fluxo das outros baseadas nesse vaor
# por fim retorna o valor subtraido 
def update_flow(arestas):
    menor = arestas[0]
    for ar in arestas:
        if ar.capacity < menor.capacity:
            menor = ar
    temp = menor.capacity
    for ar in arestas:
        # print(f' -> {ar.dst.id}  cap of {ar.capacity}')
        ar.capacity -= temp
    return temp
def ford_fulkerson(vertices, s, t):
    print("Ford-Fulkerson")
    print(f'comeco: {s.id}   fim: {t.id}')

    for v in vertices:
        v.ff_pai = None
        v.visited = False

    # printa as arestas e a capacidade de cada uma
    # for v in vertices:
    #     for ar in v.conexoes:
    #         print(f'{v.id} -> {ar.dst.id} with {ar.capacity}')

    max_flow = 0
    
    # ff_bfs para encontrar o caminho de s a t
    # caso nao exista um caminho de s a t retorna None
    # para percorer pelo caminnho comecamos de t e voltamos a s, 
    # usnado o atributo ff_pai para saber o pai do vertice
    vef = ff_bfs(vertices, s, t)
    while vef != None:

        # c guarda as arestas que estao no caminho de s a t
        c = []
        
        # percore o caminho reverso, de t ate s, adicionando
        # as arestas no caminho para 'c'        
        p = t
        while p.ff_pai != None:
                c.append(p.ff_pai.getArestaFromVertice(p))
                p = p.ff_pai
        
        x = update_flow(c)
        print(f"passando mais {x} de fluxo")
        max_flow += x

        # for v in vertices:
        #     for ar in v.conexoes:
        #         print(f'{v.id} -> {ar.dst.id} with {ar.capacity}')

        vef = ff_bfs(vertices, s, t)
    print(f'flow maximo = {max_flow}')
    return max_flow


def main():
    # vertices ficao guardados como ponteiros dentro de 'vertices'
    vertices = []
   
    # para implementacao de um novo grafo, basta colocar as arestas no formato:
    # lista de tuplas com os seguintes valores: (origem, destino, peso), peso pode ser
    # substituido por "capacidade", caso queira usar grafo para ford-fulkerson.
    
    # O nome da variavel precisa ser 'Arestas', assim como a variavel 'lenv' precisa
    # conter o numero de vertices totais do grafo.
    
    # apos escolher o grafo desejado no formato de lista de tuplas, descendo o codigo
    # temos que escolher se queremos usar no formato de grafo nao orientado ou orientado
    # alem disso temos um modo especifico para o algoritmo de ford-fulkerson, onde trocamos
    # peso por capacidade da aresta.

    lenv = 8
    
    # arestas determina quais conexoes entre os nos sao feitas
    # grafo equivalente a imagem 'grafo.png'
    arestas = [(1,2, 2), (1,4, 2), 
               (2,3, -3), (2,4, -1), 
               (3,7, -2), 
               (4,8, 2), (4,1, -1),
               (5,7, 1), (5,6, 2),
               (6,5, 2), 
               (8,7, 4)]

    # grafo equivalente a imagem 'grafo2.png'
    # grafo nao orientado
    # arestas = [(1,2, 1), (1,5, 1), (2,3, 2), (2,4, 2), (2,5, 2), (3,5, 3), (4,6, 4), (5,6, 3)]
    
    # para ford_fulkerson
    # grafo equivalente a imagem 'grafo.png' porem com capacidade diferente
    # arestas = [(1,2, 20), (1,4, 15), 
    #            (2,3, 7), (2,4, 8), 
    #            (3,7, 18), 
    #            (4,8, 33), (4,1, 6),
    #            (5,7, 9), (5,6, 17),
    #            (6,5, 33), 
    #            (8,7, 20)]

    

    for i in range(lenv):
        v = Vertice(i+1)
        vertices.append(v)
   
    #para ford_fulkerson
    # for src, dst, c in arestas:
        # vertices[src-1].conexoes.append(Aresta(vertices[dst-1], 1, capacity=c))

    # orientado
    for src, dst, w in arestas:
        vertices[src-1].addAresta(vertices[dst-1], w)
    
    # nao orientado
    # for src, dst, w, in arestas:
    #     vertices[src-1].addAresta(vertices[dst-1], w)
    #     vertices[dst-1].addAresta(vertices[src-1], w)




    # trab 1
    bfs(vertices, vertices[0])
    dfs(vertices, vertices[0])
    bellman_ford(vertices, vertices[0])
    dijkstra(vertices, vertices[0])

    # trab 2
    floyd_warshall(vertices)
    prim(vertices, vertices[0])
    ford_fulkerson(vertices, vertices[0], vertices[6])

if __name__ == "__main__":
    main()