"""
Gera dados de exemplo simulando preços de ações brasileiras.
Usado automaticamente quando nenhum CSV real é fornecido.
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta


def gerar_csv_exemplo(caminho: str = os.path.join("data", "acoes_exemplo.csv")):
    """Simula 1 ano de histórico para 4 ações com passeio aleatório."""
    np.random.seed(42)

    ativos = {
        "PETR4": {"preco_inicial": 38.50, "drift": 0.0003, "vol": 0.022},
        "VALE3": {"preco_inicial": 68.00, "drift": 0.0005, "vol": 0.025},
        "ITUB4": {"preco_inicial": 27.80, "drift": 0.0002, "vol": 0.018},
        "MGLU3": {"preco_inicial": 4.20,  "drift": -0.001,  "vol": 0.040},
    }

    data_inicio = datetime(2024, 1, 2)
    dias_uteis  = pd.bdate_range(start=data_inicio, periods=252)  # ~1 ano

    registros = []
    for ticker, params in ativos.items():
        preco = params["preco_inicial"]
        for data in dias_uteis:
            retorno = np.random.normal(params["drift"], params["vol"])
            preco   = max(preco * (1 + retorno), 0.50)
            volume  = int(np.random.lognormal(mean=14, sigma=0.8))
            registros.append({
                "Data":             data.strftime("%Y-%m-%d"),
                "Ticker":           ticker,
                "Preco_Fechamento": round(preco, 2),
                "Volume":           volume,
            })

    df = pd.DataFrame(registros)
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    df.to_csv(caminho, index=False)
    print(f"  ✅ Dados de exemplo gerados: {caminho}  ({len(df)} linhas)")
    return df


if __name__ == "__main__":
    gerar_csv_exemplo()
