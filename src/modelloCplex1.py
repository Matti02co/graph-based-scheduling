import json
from docplex.mp.model import Model
import numpy as np

#Genera dati casuali con seme per permettere la ripetibilità, dati il numero di core e processi e i tempi
def generaDati(numeroCore, numeroProcessi, tempoCore, tempoMaxProcessi):

    np.random.seed(88)
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
        "Tlim": [40, 40, 40, 40],  # Tempo limite per ciascun core
        "processi": [
            {"nome": "processo_1", "t": 15, "p": 8},  # Processo 1: tempo 15, priorità 8
            {"nome": "processo_2", "t": 20, "p": 5},  # Processo 2: tempo 20, priorità 5
            {"nome": "processo_3", "t": 10, "p": 2},  # E cosi via
            {"nome": "processo_4", "t": 25, "p": 7},
            {"nome": "processo_5", "t": 30, "p": 6},
            {"nome": "processo_6", "t": 3, "p": 8},
            {"nome": "processo_7", "t": 18, "p": 5},
            {"nome": "processo_8", "t": 40, "p": 10},
            {"nome": "processo_9", "t": 25, "p": 3},
            {"nome": "processo_10", "t": 30, "p": 9}
        ]
    }

    return dati

#Prende i dati e crea il modello con Docplex
def create_model(dati):

    Tlim = dati["Tlim"]  # Tempo massimo per ogni core
    processi = dati["processi"]  # Dati processi

    numeroCore = len(Tlim)
    numeroProcessi = len(processi)

    t = np.array([p["t"] for p in processi])  # Tempi di esecuzione
    p = np.array([p["p"] for p in processi])  # Priorità
    nomi = [p["nome"] for p in processi]  # Nomi processi

    # Creazione modello
    model = Model("process_scheduling")

    # Variabili binarie: 1 se il processo j è assegnato al core i, 0 altrimenti
    x = model.binary_var_matrix(numeroCore, numeroProcessi, name="x")

#ATTENZIONE: in seguito ci sono 2 funzioni obbiettivo, lasciarne solo 1 non commentata

    # Funzione obiettivo per massimizzare il valore totale delle priorità dei processi eseguiti
    #model.maximize(model.sum(p[j] * x[i, j] for i in range(numeroCore) for j in range(numeroProcessi)))

    # Funzione obiettivo per massimizzare il numero di processi eseguiti
    model.maximize(model.sum(x[i, j] for i in range(numeroCore) for j in range(numeroProcessi)))


    # Vincolo 1: Ogni processo può essere assegnato a un solo core
    for j in range(numeroProcessi):
        model.add_constraint(model.sum(x[i, j] for i in range(numeroCore)) <= 1, f"process_assignment_{j}")

    # Vincolo 2: Tempo totale per core non deve superare il limite
    for i in range(numeroCore):
        model.add_constraint(model.sum(t[j] * x[i, j] for j in range(numeroProcessi)) <= Tlim[i], f"core_time_limit_{i}")

    return model


# SETTAGGIO PARAMETRI: utilizzare una sola modalità e commentare l'altra

# Per generare dati casuali:
dati = generaDati(4, 250, 600, 45)

#Per inserire pochi dati per testare fast
#dati= datiProva()

# Creazione del modello
model = create_model(dati)
model.print_information()
model.prettyprint()

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