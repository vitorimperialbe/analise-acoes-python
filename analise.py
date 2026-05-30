"""
Módulo de análise de investimentos.
Contém funções para calcular métricas financeiras e gerar gráficos.
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import os

# ── Cores para os gráficos ──────────────────────────────────────────────────
COR_POSITIVO = "#2ecc71"
COR_NEGATIVO = "#e74c3c"
COR_NEUTRO   = "#3498db"
COR_FUNDO    = "#1a1a2e"
COR_TEXTO    = "#eaeaea"


def carregar_dados(caminho: str) -> pd.DataFrame:
    """Carrega e valida o CSV de histórico de preços."""
    df = pd.read_csv(caminho, parse_dates=["Data"])
    df = df.sort_values("Data").reset_index(drop=True)
    colunas_necessarias = {"Data", "Ticker", "Preco_Fechamento", "Volume"}
    if not colunas_necessarias.issubset(df.columns):
        raise ValueError(f"O CSV precisa ter as colunas: {colunas_necessarias}")
    return df


def calcular_retorno(df: pd.DataFrame) -> pd.DataFrame:
    """Calcula retorno diário e acumulado por ticker."""
    df = df.copy()
    df["Retorno_Diario"] = df.groupby("Ticker")["Preco_Fechamento"].pct_change()
    df["Retorno_Acumulado"] = df.groupby("Ticker")["Retorno_Diario"].transform(
        lambda x: (1 + x).cumprod() - 1
    )
    return df


def calcular_media_movel(df: pd.DataFrame, janelas: list[int] = [7, 21]) -> pd.DataFrame:
    """Adiciona médias móveis ao DataFrame."""
    df = df.copy()
    for janela in janelas:
        df[f"MM_{janela}"] = df.groupby("Ticker")["Preco_Fechamento"].transform(
            lambda x: x.rolling(window=janela).mean()
        )
    return df


def resumo_estatistico(df: pd.DataFrame) -> pd.DataFrame:
    """Gera tabela resumo com métricas por ativo."""
    grp = df.groupby("Ticker")
    resumo = pd.DataFrame({
        "Preço Atual (R$)":  grp["Preco_Fechamento"].last().round(2),
        "Retorno Total (%)": (grp["Retorno_Acumulado"].last() * 100).round(2),
        "Volatilidade (%)":  (grp["Retorno_Diario"].std() * 100).round(2),
        "Máximo (R$)":       grp["Preco_Fechamento"].max().round(2),
        "Mínimo (R$)":       grp["Preco_Fechamento"].min().round(2),
        "Vol. Médio":        grp["Volume"].mean().astype(int),
    })
    resumo["Risco/Retorno"] = (resumo["Retorno Total (%)"] / resumo["Volatilidade (%)"]).round(2)
    return resumo.sort_values("Retorno Total (%)", ascending=False)


def _configurar_estilo():
    """Aplica tema escuro nos gráficos."""
    plt.rcParams.update({
        "figure.facecolor":  COR_FUNDO,
        "axes.facecolor":    "#16213e",
        "axes.edgecolor":    "#444",
        "axes.labelcolor":   COR_TEXTO,
        "xtick.color":       COR_TEXTO,
        "ytick.color":       COR_TEXTO,
        "text.color":        COR_TEXTO,
        "grid.color":        "#2a2a4a",
        "grid.linestyle":    "--",
        "grid.alpha":        0.6,
        "legend.facecolor":  "#16213e",
        "legend.edgecolor":  "#444",
        "font.family":       "DejaVu Sans",
    })


def plotar_precos(df: pd.DataFrame, salvar_em: str = "graficos"):
    """Gráfico de preços com médias móveis para cada ticker."""
    _configurar_estilo()
    os.makedirs(salvar_em, exist_ok=True)
    cores = [COR_NEUTRO, COR_POSITIVO, "#f39c12", "#9b59b6", "#e67e22"]

    for i, (ticker, grupo) in enumerate(df.groupby("Ticker")):
        fig, ax = plt.subplots(figsize=(12, 5))
        cor = cores[i % len(cores)]

        ax.plot(grupo["Data"], grupo["Preco_Fechamento"],
                color=cor, linewidth=1.8, label="Preço", zorder=3)

        if "MM_7" in grupo.columns:
            ax.plot(grupo["Data"], grupo["MM_7"],
                    color="#f39c12", linewidth=1, linestyle="--", label="MM 7d", alpha=0.8)
        if "MM_21" in grupo.columns:
            ax.plot(grupo["Data"], grupo["MM_21"],
                    color="#e74c3c", linewidth=1, linestyle="--", label="MM 21d", alpha=0.8)

        ax.fill_between(grupo["Data"], grupo["Preco_Fechamento"],
                        alpha=0.08, color=cor)
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%b/%y"))
        ax.xaxis.set_major_locator(mdates.MonthLocator())
        plt.xticks(rotation=30)
        ax.set_title(f"Histórico de Preços — {ticker}", fontsize=14, pad=12)
        ax.set_ylabel("Preço de Fechamento (R$)")
        ax.legend()
        ax.grid(True)
        plt.tight_layout()
        caminho = os.path.join(salvar_em, f"preco_{ticker}.png")
        plt.savefig(caminho, dpi=150)
        plt.close()
        print(f"  ✅ Gráfico salvo: {caminho}")


def plotar_retorno_acumulado(df: pd.DataFrame, salvar_em: str = "graficos"):
    """Compara retorno acumulado de todos os ativos no mesmo gráfico."""
    _configurar_estilo()
    os.makedirs(salvar_em, exist_ok=True)
    cores = [COR_NEUTRO, COR_POSITIVO, "#f39c12", "#9b59b6", "#e67e22"]

    fig, ax = plt.subplots(figsize=(13, 6))
    for i, (ticker, grupo) in enumerate(df.groupby("Ticker")):
        ax.plot(grupo["Data"], grupo["Retorno_Acumulado"] * 100,
                label=ticker, linewidth=2, color=cores[i % len(cores)])

    ax.axhline(0, color="#666", linewidth=0.8, linestyle="--")
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b/%y"))
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    plt.xticks(rotation=30)
    ax.set_title("Retorno Acumulado Comparativo (%)", fontsize=14, pad=12)
    ax.set_ylabel("Retorno (%)")
    ax.legend(loc="upper left")
    ax.grid(True)
    plt.tight_layout()
    caminho = os.path.join(salvar_em, "retorno_acumulado.png")
    plt.savefig(caminho, dpi=150)
    plt.close()
    print(f"  ✅ Gráfico salvo: {caminho}")


def plotar_correlacao(df: pd.DataFrame, salvar_em: str = "graficos"):
    """Mapa de calor de correlação entre os ativos."""
    _configurar_estilo()
    os.makedirs(salvar_em, exist_ok=True)

    pivot = df.pivot_table(index="Data", columns="Ticker", values="Retorno_Diario")
    corr  = pivot.corr()

    fig, ax = plt.subplots(figsize=(8, 6))
    im = ax.imshow(corr.values, cmap="RdYlGn", vmin=-1, vmax=1, aspect="auto")
    plt.colorbar(im, ax=ax, label="Correlação")
    tickers = corr.columns.tolist()
    ax.set_xticks(range(len(tickers)))
    ax.set_yticks(range(len(tickers)))
    ax.set_xticklabels(tickers, rotation=45, ha="right")
    ax.set_yticklabels(tickers)

    for r in range(len(tickers)):
        for c in range(len(tickers)):
            ax.text(c, r, f"{corr.values[r, c]:.2f}",
                    ha="center", va="center", fontsize=10,
                    color="black" if abs(corr.values[r, c]) < 0.5 else "white")

    ax.set_title("Mapa de Correlação entre Ativos", fontsize=13, pad=12)
    plt.tight_layout()
    caminho = os.path.join(salvar_em, "correlacao.png")
    plt.savefig(caminho, dpi=150)
    plt.close()
    print(f"  ✅ Gráfico salvo: {caminho}")
