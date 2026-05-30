# Análise de Ações com Python

Projeto final da disciplina de Programação. O objetivo foi usar Python pra analisar o histórico de preços de ações e gerar gráficos mostrando a evolução e o retorno de cada uma.

## O que o projeto faz

- Lê um arquivo CSV com histórico de preços
- Calcula o retorno de cada ação no período
- Gera um gráfico com a evolução dos preços
- Gera um gráfico de barras comparando o retorno de cada ação

## Como rodar

Primeiro instala as bibliotecas necessárias:

```
pip install -r requirements.txt
```

Depois gera os dados de exemplo:

```
python gerar_dados.py
```

E por fim roda a análise:

```
python main.py
```

## Bibliotecas usadas

- **pandas** - pra ler e manipular os dados do CSV
- **matplotlib** - pra gerar os gráficos

## Formato do CSV

O arquivo precisa ter as colunas: `Data`, `Ticker` e `Preco`

Exemplo:
```
Data,Ticker,Preco
2024-01-02,PETR4,38.00
2024-01-02,VALE3,70.00
```

## Resultado

O programa imprime no terminal um resumo com preço inicial, preço final e retorno de cada ação, e salva dois gráficos em PNG na pasta do projeto.
