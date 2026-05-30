# esse script gera os dados de exemplo pra testar o projeto
# ele simula preços de ações ao longo de 6 meses
# basta rodar uma vez antes de rodar o main.py

import pandas as pd
import numpy as np
import os

# semente aleatória pra os resultados serem sempre iguais
np.random.seed(10)

acoes = ["PETR4", "VALE3", "ITUB4", "MGLU3"]

# preços iniciais de cada ação (aproximados)
precos_iniciais = {
    "PETR4": 38.00,
    "VALE3": 70.00,
    "ITUB4": 28.00,
    "MGLU3": 4.50,
}

# gera datas úteis de 6 meses
datas = pd.bdate_range(start="2024-01-02", end="2024-06-28")

linhas = []

for acao in acoes:
    preco = precos_iniciais[acao]
    for data in datas:
        # simula variação diária aleatória de -3% a +3%
        variacao = np.random.uniform(-0.03, 0.03)
        preco = preco * (1 + variacao)
        preco = round(preco, 2)
        linhas.append({"Data": data.strftime("%Y-%m-%d"), "Ticker": acao, "Preco": preco})

df = pd.DataFrame(linhas)

# cria a pasta data se não existir
os.makedirs("data", exist_ok=True)
df.to_csv("data/acoes.csv", index=False)

print(f"Arquivo gerado: data/acoes.csv ({len(df)} linhas)")
