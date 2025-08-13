import numpy as np
import time
from collections import defaultdict, deque

#Genera dati casuali con seme per permettere la ripetibilità, dati il numero di core e processi e i tempi
def generaDati(numeroCore, numeroProcessi, tempoCore, tempoMaxProcessi):

    np.random.seed(93)
    Tlim= [tempoCore] * numeroCore
    t = np.random.randint(1, tempoMaxProcessi, numeroProcessi)  # Tempi di esecuzione dei processi
    p = np.random.randint(1, 10, numeroProcessi)  #Priorita dei processi
    nomi = [f'processo_{i}' for i in range(numeroProcessi)]

    dati = {
        "Tlim": Tlim,
        "processi": [
            {"nome": nomi[i], "t": t[i], "p": p[i]} for i in range(numeroProcessi)
        ]
    }

    return dati

#Inserisce un micro set di dati fissati per testare
def datiProva():
    dati = {
        "Tlim": [70],  # Tempo limite per ciascun core
        "processi": [
            {"nome": "processo_0", "t": 15, "p": 8},  # Processo 1: tempo 15, priorità 8
            {"nome": "processo_1", "t": 20, "p": 6},  # Processo 2: tempo 20, priorità 5
            {"nome": "processo_2", "t": 10, "p": 2},  # E cosi via
            {"nome": "processo_3", "t": 25, "p": 7},
            {"nome": "processo_4", "t": 30, "p": 6},
            {"nome": "processo_5", "t": 3, "p": 8},
            {"nome": "processo_6", "t": 18, "p": 5},
            {"nome": "processo_7", "t": 40, "p": 10},
            {"nome": "processo_8", "t": 25, "p": 3},
            {"nome": "processo_9", "t": 30, "p": 9}
        ]
    }

    return dati


#Crea il grafo dai dati generati
def generaGrafo(processi, T):

    n = len(processi)
    archi = []

    for i in range(n):
        for k in range(T + 1):
            proc = processi[i]
            name = proc["nome"]
            t = proc["t"]
            p = proc["p"]

            #Arco corrispondente esecuzione
            archi.append({
                "from": (i, k),
                "to": (i + 1, k),
                "cost": 0,
                "label": f"no_{name}"
            })

            #Arco non eseguire
            if k + t <= T:
                archi.append({
                    "from": (i, k),
                    "to": (i + 1, k + t),
                    "cost": -p,  # costo negativo rispetto alla priorita
                    "label": f"yes_{name}"
                })

    # Aggiungi sorgente e archi iniziali
    archi.append({
        "from": "s",
        "to": (0, 0),
        "cost": 0,
        "label": "start"
    })

    #Archi da ogni stato finale verso sink
    for k in range(T + 1):
        archi.append({
            "from": (n, k),
            "to": "t",
            "cost": 0,
            "label": f"end_{k}"
        })

    return archi

# Funzione per risalire al cammino
def reconstructPath(pred, source, sink):
    path = []
    node = sink
    while node != source:
        prev = pred.get(node)
        if prev is None:
            return []  # nessun cammino trovato
        path.append((prev, node))
        node = prev
    path.reverse()
    return path

#estrae informazioni dal cammino
def extractInfo(path, edges):
    edge_dict = {(e["from"], e["to"]): e for e in edges}
    return [edge_dict[(u, v)] for u, v in path if (u, v) in edge_dict]

#LC modificato normale
def lcModificato(archi, source, sink):


    #Costruzione
    A = defaultdict(list)
    N = set()
    for u, v, cost in archi:
        A[u].append((v, cost))
        N.update([u, v])

    #Inizializza
    d = {nodo: float('inf') for nodo in N}
    pred = {nodo: None for nodo in N}
    d[source] = 0

    LIST = [source]

    while LIST:
        i = LIST.pop()
        for j, cij in A[i]:
            if d[j] > d[i] + cij:
                d[j] = d[i] + cij
                pred[j] = i
                if j not in LIST:
                    LIST.append(j)

    return d[sink], pred


#con dequeue
def lcModificatoDeque(archi, source, sink):

    # costruzione grafo
    A = defaultdict(list)
    N = set()
    for u, v, c in archi:
        A[u].append((v, c))
        N.update([u, v])

    #Inizializza
    d = {nodo: float('inf') for nodo in N}
    pred = {nodo: None for nodo in N}
    d[source] = 0

    LIST = deque([source])

    while LIST:
        i = LIST.popleft()
        for j, cij in A[i]:
            if d[j] > d[i] + cij:
                d[j] = d[i] + cij
                pred[j] = i
                if j not in LIST:
                    LIST.append(j)

    return d[sink], pred


def reachingMethod(archi, source, sink):

    #Costruzione
    A = defaultdict(list)
    N = set()
    for i, j, cij in archi:
        A[i].append((j, cij))
        N.update([i, j])

    # Calcolo indegree
    inDegree = defaultdict(int)
    for i in A:
        for j, _ in A[i]:
            inDegree[j] += 1
        if i not in inDegree:
            inDegree[i] = 0  # anche nodi senza archi entranti

    #ordinamento topologico
    LIST = [node for node in N if inDegree[node] == 0]
    order = []

    while LIST:
        i = LIST.pop(0)
        order.append(i)
        for j, _ in A[i]:
            inDegree[j] -= 1
            if inDegree[j] == 0:
                LIST.append(j)

    #inizializza
    d = {node: float('inf') for node in N}
    pred = {node: None for node in N}
    d[source] = 0

    #Reaching method effettivo
    for i in order:
        for j, cij in A[i]:
            if d[j] > d[i] + cij:
                d[j] = d[i] + cij
                pred[j] = i

    return d[sink], pred



#SETTAGGIO PARAMETRI

# Per generare dati casuali:
dati = generaDati(1, 250, 700, 11)

#Per inserire pochi dati per testare fast
#dati= datiProva()

#dati in variabili
T = dati["Tlim"][0]
processi = dati["processi"]

#Costruzione SPP
edges = generaGrafo(processi, T)

# Converti in formato (nodo1, nodo2, costo)
archiNuovi = [(e["from"], e["to"], e["cost"]) for e in edges]

#Algoritmi e calcolo tempo
start_time = time.perf_counter()
#val, pred = lcModificatoDeque(archiNuovi, "s", "t")
#val, pred = lcModificato(archiNuovi, "s", "t")
val, pred = reachingMethod(archiNuovi, "s", "t")
elapsed = time.perf_counter() - start_time
path = reconstructPath(pred, "s", "t")
info = extractInfo(path, edges)

print(f"\nPriorità totale ottima: {-val}")
print("Processi selezionati:")
for arc in info:
    if arc["label"].startswith("yes_"):
        print(f" - {arc['label'][4:]} (priorità {-arc['cost']}, durata implicita)")

print(f"valore: {-val} ottenuto in {elapsed:.6f} secondi")