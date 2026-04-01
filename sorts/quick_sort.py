# def partition(array, menor, maior):
#     pivo = array[maior]
#     i = menor-1

#     for j in range(menor,maior):
#         if array[j] <= pivo:
#             i += 1
#             array[i], array[j] = array[j], array[i]

#     array[i+1], array[maior] = array[maior], array[i+1]

#     return i+1

# def quicksort(array, menor=0, maior=None):
#     if maior is None:
#         maior = len(array)-1
    
#     if menor < maior:
#         index_pivo = partition(array, menor, maior)
#         quicksort(array, menor, index_pivo-1)
#         quicksort(array, index_pivo+1, maior)

# lista = [64, 34, 25, 5, 22, 11, 90, 12]
# quicksort(lista)
# print(lista)

from datadog import initialize, statsd
import time

options = {
    'statsd_host': '127.0.0.1',
    'statsd_port': 8125
}
initialize(**options)

def sort(arr, comparacoes=0, trocas=0):
    if len(arr) <= 1:
        return arr, comparacoes, trocas

    pivot = arr[len(arr) // 2]

    left = []
    middle = []
    right = []

    for x in arr:
        comparacoes += 1 
        if x < pivot:
            left.append(x)
            trocas += 1 
        else:
            comparacoes += 1  
            if x == pivot:
                middle.append(x)
                trocas += 1
            else:
                comparacoes += 1 
                right.append(x)
                trocas += 1

    left, comparacoes, trocas = sort(left, comparacoes, trocas)
    right, comparacoes, trocas = sort(right, comparacoes, trocas)

    return left + middle + right, comparacoes, trocas