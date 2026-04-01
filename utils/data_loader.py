import random
import json
import os

def gerar_dados(tamanho):
    return [random.randint(0, 100000) for _ in range(tamanho)]

def salvar_dados(nome_arquivo, dados):
    with open(nome_arquivo, "w") as f:
        json.dump(dados, f)

def carregar_dados(nome_arquivo): 
    with open(nome_arquivo, "r") as f:
        return json.load(f)

if __name__ == "__main__":
    tamanhos = [1000, 5000, 10000, 50000]

    os.makedirs("data", exist_ok=True)

    for t in tamanhos:
        dados = gerar_dados(t)
        salvar_dados(f"data/dados_{t}.json", dados)