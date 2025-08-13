import json
from docplex.mp.model import Model
import numpy as np
import time


#Genera dati casuali con seme per permettere la ripetibilità, dati il numero di core e processi e i tempi
def generaDati(numeroCore, numeroProcessi, tempoCore, tempoMaxProcessi):

    np.random.seed(23)
    Tlim= [tempoCore] * numeroCore
    t = np.random.randint(1, tempoMaxProcessi, numeroProcessi)  # Tempi di esecuzione dei processi
    p = np.random.randint(1, 10, numeroProcessi)  # Priorità dei processi
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
        "Tlim": [70],  # Tempo limite per il core
        "processi": [
            {"nome": "processo_0", "t": 15, "p": 8},  # Processo 1: tempo 15, priorità 8
            {"nome": "processo_1", "t": 20, "p": 6},  # ecc
            {"nome": "processo_2", "t": 10, "p": 2},
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


#Costruzione modello CPLEX
def build_model(processes, T):

    model = Model("LPP")
    n = len(processes)

    #prova tempo generazione grafo
    start_time = time.perf_counter()

    #Crea il grafo a partire dai dati del problema di scheduling
    archi = []
    for i in range(n ):        #tanti strati quanti processi per adesso
        for k in range(T + 1):        #nodi per strato, rappresentanti k istanti consumati
            if i < n:                     #creazione nodi
                dur = processes[i]["t"]
                pr = processes[i]["p"]
                nm = processes[i]["nome"]

                #arco scelta di non eseguire il processo
                archi.append({"from": (i, k), "to": (i + 1, k), "priority": 0, "dec": f"no_{nm}"})

                #arco scelta di eseguire il processo, se il tempo residuo lo permette
                if k + dur <= T:
                    archi.append({
                        "from": (i, k), "to": (i+1, k + dur),
                        "priority": pr, "dec": f"yes_{nm}"
                    })

    # aggiunge source e sink e li collega ai nodi opportuni
    source, sink = "s", "t"
    archi.append({"from": source, "to": (0, 0), "priority": 0, "dec": "start"})
    for k in range(T + 1):
        archi.append({"from": (n, k), "to": sink, "priority": 0, "dec": f"end_{k}"})

    #prova
    elapsed = time.perf_counter() - start_time
    print(f"tempo generazione grafo: {elapsed:.6f} secondi")

    # prova tempo costruzione modello
    start_timem = time.perf_counter()

    #Variabili binarie per arco
    x = {}
    for e in archi:
        key = (e["from"], e["to"], e["dec"])
        x[key] = model.binary_var(name=f"x_{e['dec']}_{e['from']}_{e['to']}")

    #Obiettivo: massimizza la somma delle priorità
    model.maximize(model.sum(e["priority"] * x[(e["from"], e["to"], e["dec"])] for e in archi))

    #Vincoli di flow conservation
    # uscita da source
    model.add_constraint(sum(x[k] for k in x if k[0] == source) == 1)

    # ingresso a sink
    model.add_constraint(sum(x[k] for k in x if k[1] == sink) == 1)

    # ogni altro nodo
    nodes = set([e["from"] for e in archi] + [e["to"] for e in archi])
    nodes.discard(source)
    nodes.discard(sink)         #senza contare source e sink
    for node in nodes:
        model.add_constraint(
            sum(x[k] for k in x if k[1] == node) == sum(x[k] for k in x if k[0] == node),
            f"flow_{node}"
        )

    # prova
    elapsedm = time.perf_counter() - start_timem
    print(f"tempo costruzione modello: {elapsedm:.6f} secondi")

    return model, x, archi




#SETTAGGIO PARAMETRI

# Per generare dati casuali:
dati = generaDati(1, 20, 60, 15)

#Per inserire pochi dati per testare fast
#dati= datiProva()

#Inserisce i dati generati in due variabili per comodita
T = dati["Tlim"][0]
processi = dati["processi"]


#Costruzione modello
model, vars, edges = build_model(processi, T)

#model.prettyprint()

# Risoluzione del modello
if model.solve():
    model.print_solution()
    print("\nSlack:")
    for c in model.iter_constraints():
        print(f"{c.name}: {c.slack_value}")

    tempoEsecuzione = model.solve_details.time
    print(f"Tempo di esecuzione: {tempoEsecuzione}")
else:
    print("Nessuna soluzione trovata.")