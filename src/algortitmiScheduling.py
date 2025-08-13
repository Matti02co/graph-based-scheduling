import numpy as np
import time

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

#Simula un FCFS, dove i processi vengono allocati in base all'ordine dei dati
def fcfs(dati):

    Tlim = dati["Tlim"]  # Tempo massimo per ogni core
    processi = dati["processi"]  # Informazioni processi

    # Inizializzazione cores
    numeroCore = len(Tlim)
    tempiCores = [0] * numeroCore  # Tempo totale utilizzato su ciascun core
    core_allocation = [[] for _ in range(numeroCore)]  # Allocazione processi

    tempoInizio = time.perf_counter()    #Per calcolare il tempo di esecuzione

    # Allocazione FCFS
    for processo in processi:
        t_j = processo["t"]
        nome = processo["nome"]

        # Trova il primo core disponibile che può eseguire il processo
        for i in range(numeroCore):
            if tempiCores[i] + t_j <= Tlim[i]:
                core_allocation[i].append(nome)
                tempiCores[i] += t_j
                break

    tempoEsecuzione = time.perf_counter() - tempoInizio  # Calcolo tempo esecuzione
    print(f"Tempo di esecuzione FCFS: {tempoEsecuzione:.12f} seconds")


    #In altre parole il valore della funzione obbiettivo, senza contare la priorità
    processiEseguiti = sum(len(core) for core in core_allocation)  # Numero totale di processi eseguiti

    return {
        "allocation": core_allocation,
        "tempiCores": tempiCores,
        "processiEseguiti": processiEseguiti
    }

#Simula un SJF, dove vengono assegnati per primi i processi eseguibili nel minor tempo
def sjf(dati):

    Tlim = dati["Tlim"]  # Tempo massimo per ogni core
    processi = sorted(dati["processi"], key=lambda x: x["t"])  # Ordina per tempo di esecuzione crescente

    # Inizializzazione cores
    numeroCore = len(Tlim)
    tempiCores = [0] * numeroCore  # Tempo totale utilizzato su ciascun core
    core_allocation = [[] for _ in range(numeroCore)]  # Allocazione processi

    tempoInizio = time.perf_counter()  # Per calcolare il tempo di esecuzione

    # Allocazione SJF
    for processo in processi:
        t_j = processo["t"]
        nome = processo["nome"]

        # Trova il primo core disponibile che può eseguire il processo
        for i in range(numeroCore):
            if tempiCores[i] + t_j <= Tlim[i]:
                core_allocation[i].append(nome)
                tempiCores[i] += t_j
                break

    tempoEsecuzione = time.perf_counter() - tempoInizio  # Calcolo tempo esecuzione
    print(f"Tempo di esecuzione SJF: {tempoEsecuzione:.12f} seconds")

    # In altre parole il valore della funzione obbiettivo, senza contare la priorità
    processiEseguiti = sum(len(core) for core in core_allocation)  # Numero totale di processi eseguiti

    return {
        "allocation": core_allocation,
        "tempiCores": tempiCores,
        "processiEseguiti": processiEseguiti
    }

def fcfsPriorita(dati):
    Tlim = dati["Tlim"]
    processi = sorted(dati["processi"], key=lambda x: x["p"], reverse=True)  # Ordina per priorità decrescente

    numeroCore = len(Tlim)
    tempiCores = [0] * numeroCore  # Tempo totale utilizzato su ciascun core
    core_allocation = [[] for _ in range(numeroCore)]  # Allocazione dei processi
    prioritaTotale = 0  # Somma delle priorità dei processi eseguiti

    tempoInizio = time.perf_counter()  # Per calcolare il tempo di esecuzione

    for processo in processi:
        t_j = processo["t"]
        nome = processo["nome"]
        priorita = processo["p"]

        # Trova il primo core disponibile che può eseguire il processo
        for i in range(numeroCore):
            if tempiCores[i] + t_j <= Tlim[i]:
                core_allocation[i].append(nome)
                tempiCores[i] += t_j
                prioritaTotale += priorita
                break

    tempoEsecuzione = time.perf_counter() - tempoInizio  # Calcolo tempo esecuzione
    print(f"Tempo di esecuzione FCFS con Priorita': {tempoEsecuzione:.12f} seconds")

    processiEseguiti = sum(len(core) for core in core_allocation)  # Numero totale di processi eseguiti

    return {
        "allocation": core_allocation,
        "tempiCores": tempiCores,
        "processiEseguiti": processiEseguiti,
        "prioritaTotale": prioritaTotale
    }

def sjfPriorita(dati):
    Tlim = dati["Tlim"]
    # Ordina per tempo di esecuzione crescente, poi per priorità decrescente
    processi = sorted(dati["processi"], key=lambda x: (x["t"], -x["p"]))

    numeroCore = len(Tlim)
    tempiCores = [0] * numeroCore  # Tempo totale utilizzato su ciascun core
    core_allocation = [[] for _ in range(numeroCore)]  # Allocazione dei processi
    prioritaTotale = 0  # Somma delle priorità dei processi eseguiti

    tempoInizio = time.perf_counter()  # Per calcolare il tempo di esecuzione

    for processo in processi:
        t_j = processo["t"]
        nome = processo["nome"]
        priorita = processo["p"]

        # Trova il primo core disponibile che può eseguire il processo
        for i in range(numeroCore):
            if tempiCores[i] + t_j <= Tlim[i]:
                core_allocation[i].append(nome)
                tempiCores[i] += t_j
                prioritaTotale += priorita
                break

    tempoEsecuzione = time.perf_counter() - tempoInizio  # Calcolo tempo esecuzione
    print(f"Tempo di esecuzione SJF con Priorita': {tempoEsecuzione:.12f} seconds")

    processiEseguiti = sum(len(core) for core in core_allocation)  # Numero totale di processi eseguiti

    return {
        "allocation": core_allocation,
        "tempiCores": tempiCores,
        "processiEseguiti": processiEseguiti,
        "prioritaTotale": prioritaTotale,
        "tempoEsecuzione": tempoEsecuzione
    }




# SETTAGGIO PARAMETRI: utilizzare una sola modalità e commentare le altre

# Per generare dati casuali:
dati = generaDati(4, 250, 600, 45)

#Per inserire pochi dati per testare fast
#dati= datiProva()

# First-Come, First-Served
risultatiFcfs = fcfs(dati)
#print("FCFS Allocation:")
#print(risultatiFcfs)
print("Numero di Processi eseguiti con FCFS: ")
print(risultatiFcfs["processiEseguiti"])
print("\n")


# Shortest Job First
risultatiSjf = sjf(dati)
#print("SJF Allocation:")
#print(risultatiSjf)
print("Numero di Processi eseguiti con SJF: ")
print(risultatiSjf["processiEseguiti"])
print("\n")


# First-Come, First-Served con priority
fcfs2 = fcfsPriorita(dati)
#print("FCFS Allocation:")
#print(fcfs2)
print("Corrispondente valore funzione obbiettivo con FCFS-priority: ")
print(fcfs2["prioritaTotale"])
print("\n")

# Shortest Job First con priority
sjf2 = sjfPriorita(dati)
#print("SJF Allocation:")
#print(sjf2)
print("Corrispondente valore funzione obbiettivo con SJF-priority: ")
print(sjf2["prioritaTotale"])
print("\n")
