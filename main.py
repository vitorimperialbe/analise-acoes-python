# Projeto Final - Análise de Ações com Python
# Disciplina: Programação Orientada a Objetos / Introdução à Programação
# Aluno: Seu Nome Aqui
# RA: 123456

import pandas as pd
import matplotlib.pyplot as plt

# carrega o arquivo csv com os dados das ações
df = pd.read_csv("data/acoes.csv")

# converte a coluna de data pra formato de data mesmo
df["Data"] = pd.to_datetime(df["Data"])

# ordena pelo mais antigo primeiro
df = df.sort_values("Data")

print("=== Análise de Ações ===")
print(f"Total de registros: {len(df)}")
print(f"Período: {df['Data'].min().date()} até {df['Data'].max().date()}")
print()

# pega os nomes das ações únicas
acoes = df["Ticker"].unique()
print(f"Ações analisadas: {', '.join(acoes)}")
print()

# calcula o retorno de cada ação (quanto subiu ou caiu em %)
print("=== Resumo por Ação ===")
for acao in acoes:
    dados_acao = df[df["Ticker"] == acao]
    preco_inicial = dados_acao["Preco"].iloc[0]
    preco_final   = dados_acao["Preco"].iloc[-1]
    retorno       = ((preco_final - preco_inicial) / preco_inicial) * 100

    print(f"{acao}:")
    print(f"  Preço inicial: R$ {preco_inicial:.2f}")
    print(f"  Preço final:   R$ {preco_final:.2f}")
    print(f"  Retorno:       {retorno:+.2f}%")
    print()

# ---- Gráfico 1: evolução do preço de cada ação ----
plt.figure(figsize=(10, 5))

for acao in acoes:
    dados_acao = df[df["Ticker"] == acao]
    plt.plot(dados_acao["Data"], dados_acao["Preco"], label=acao)

plt.title("Evolução do Preço das Ações")
plt.xlabel("Data")
plt.ylabel("Preço (R$)")
plt.legend()
plt.tight_layout()
plt.savefig("grafico_precos.png")
plt.show()
print("Gráfico salvo como grafico_precos.png")

# ---- Gráfico 2: comparar retorno total de cada ação ----
retornos = []
nomes    = []

for acao in acoes:
    dados_acao = df[df["Ticker"] == acao]
    p_inicial  = dados_acao["Preco"].iloc[0]
    p_final    = dados_acao["Preco"].iloc[-1]
    retorno    = ((p_final - p_inicial) / p_inicial) * 100
    retornos.append(retorno)
    nomes.append(acao)

# define cor verde pra quem subiu e vermelho pra quem caiu
cores = ["green" if r > 0 else "red" for r in retornos]

plt.figure(figsize=(8, 5))
plt.bar(nomes, retornos, color=cores)
plt.title("Retorno Total por Ação (%)")
plt.xlabel("Ação")
plt.ylabel("Retorno (%)")
plt.axhline(0, color="black", linewidth=0.8)  # linha no zero pra facilitar visualização
plt.tight_layout()
plt.savefig("grafico_retorno.png")
plt.show()
print("Gráfico salvo como grafico_retorno.png")
