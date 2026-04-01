from datadog import initialize, statsd
import time

options = {
    'statsd_host': '127.0.0.1',
    'statsd_port': 8125
}
initialize(**options)

def sort(lista):
    comparacoes = 0
    trocas = 0
    elementos = len(lista)-1
    ordenado = False
    while not ordenado:
        ordenado = True
        for i in range(elementos):
            comparacoes += 1
            if lista[i] > lista[i+1]:
                lista[i], lista[i+1] = lista[i+1], lista[i]
                trocas += 1
                ordenado = False
    return lista, comparacoes, trocas