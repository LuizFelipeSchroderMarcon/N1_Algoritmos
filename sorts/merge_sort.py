from datadog import initialize, statsd
import time

options = {
    'statsd_host': '127.0.0.1',
    'statsd_port': 8125
}
initialize(**options)

def sort(arr):
    comparacoes = 0 
    trocas = 0
    if len(arr) > 1:
        meio = len(arr) // 2
        esquerda = arr[:meio]
        direita = arr[meio:]

        sort(esquerda)
        sort(direita)
        i = j = k = 0

        while i < len(esquerda) and j < len(direita):
            comparacoes += 1
            if esquerda[i] < direita[j]:
                arr[k] = esquerda[i]
                i += 1
            else:
                arr[k] = direita[j]
                j += 1
                trocas += 1
            k += 1

        while i < len(esquerda):
            arr[k] = esquerda[i]
            i += 1
            k += 1
            trocas += 1

        while j < len(direita):
            arr[k] = direita[j]
            j += 1
            k += 1
            trocas += 1
    return arr, comparacoes, trocas
