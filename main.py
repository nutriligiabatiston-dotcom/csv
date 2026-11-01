import os
import pandas as pd
import modulo_vendas as mv

#Gerar o Dataset CSV
#vendas.gerar_dataset_sintetico()

#Faz a leitura do CSV e cria nosso DataFrame Pandas

def main():

    # 1. Verificar se o arquivo existe
    arquivo = "vendas.csv"

    if not os.path.exists(arquivo):
        print("Arquivo não encontrado. Gerando dados...")
        mv.gerar_dataset_sintetico(arquivo)

    # 2. Carregar os dados com Pandas
    df = pd.read_csv(arquivo)

    print("\n--- DADOS CARREGADOS ---")
    print(df.head())

    # 3. Inspecionar os dados
    print("\n--- INSPEÇÃO DOS DADOS ---")
    print("Quantidade de registros:", len(df))
    print("Valores ausentes por coluna:")
    print(df.isnull().sum())

    # 4. Limpar os dados
    df.columns = df.columns.str.strip()

    # Remover espaços dos campos de texto
    colunas_texto = df.select_dtypes(include="object").columns

    for coluna in colunas_texto:
        df[coluna] = df[coluna].str.strip()

    # Converter quantidade e preço para números
    df["quantidade"] = pd.to_numeric(
        df["quantidade"], errors="coerce"
    )

    df["preco_unitario"] = pd.to_numeric(
        df["preco_unitario"], errors="coerce"
    )

    # Remover linhas inválidas
    df = df.dropna(
        subset=["quantidade", "preco_unitario"]
    )

    df = df[
        (df["quantidade"] > 0) &
        (df["preco_unitario"] > 0)
    ].copy()

    df["quantidade"] = df["quantidade"].astype(int)

    # 5. Criar campos derivados
    df["receita_total"] = (
        df["quantidade"] * df["preco_unitario"]
    )

    # Classificar faixa de preço
    df["faixa_preco"] = pd.cut(
        df["preco_unitario"],
        bins=[-float("inf"), 500, 2000, float("inf")],
        labels=["Baixo", "Médio", "Alto"],
        right=True
    )

    # 6. Calcular receita por categoria
    receita_categoria = (
        df.groupby("categoria")["receita_total"]
        .sum()
    )

    print("\n--- RECEITA POR CATEGORIA ---")
    print(receita_categoria)

    # 7. Calcular receita por região
    receita_regiao = (
        df.groupby("regiao")["receita_total"]
        .sum()
    )

    print("\n--- RECEITA POR REGIÃO ---")
    print(receita_regiao)

    # 8. Calcular receita total
    receita_geral = df["receita_total"].sum()

    print("\nReceita total:", receita_geral)

    # 9. Segmentar clientes pelo valor acumulado
    gasto_cliente = (
        df.groupby("cliente")["receita_total"]
        .sum()
        .reset_index()
    )

    gasto_cliente["segmento"] = pd.cut(
        gasto_cliente["receita_total"],
        bins=[-float("inf"), 3000, 8000, float("inf")],
        labels=["Bronze", "Prata", "Ouro"],
        right=True
    )

    print("\n--- SEGMENTAÇÃO DE CLIENTES ---")
    print(gasto_cliente)

    # 10. Identificar os cinco maiores clientes
    top_clientes = gasto_cliente.sort_values(
        by="receita_total",
        ascending=False
    ).head(5)

    print("\n--- TOP 5 CLIENTES ---")
    print(top_clientes)

    # 11. Exportar resultados
    os.makedirs("outputs", exist_ok=True)

    receita_categoria.to_csv(
        "outputs/metricas_resumo.csv"
    )

    estatisticas = {
        "quantidade_registros": int(len(df)),
        "receita_total": float(receita_geral),
        "ticket_medio": float(df["receita_total"].mean()),
        "quantidade_clientes": int(df["cliente"].nunique())
    }

    import json

    with open(
        "outputs/estatisticas.json",
        "w",
        encoding="utf-8"
    ) as arquivo_json:
        json.dump(
            estatisticas,
            arquivo_json,
            indent=4,
            ensure_ascii=False
        )

    print("\nRelatórios exportados com sucesso!")


if __name__ == "__main__":
    main()
