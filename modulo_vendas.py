## Arquivo de módulo com as funções de vendas ###
# python
import csv
import json 
import os 
import random
import pandas as pd 

def gerar_dataset_sintetico(
    caminho_arquivo="vendas.csv",
    n_registros=150,
    seed=42
):
    """Gera um arquivo CSV contendo vendas fictícias."""

    random.seed(seed)

    produtos = [
        "Notebook",
        "Smartphone",
        "Tablet",
        "Monitor",
        "Teclado",
        "Mouse"
    ]

    categorias = {
        "Notebook": "Eletrônicos",
        "Smartphone": "Celulares",
        "Tablet": "Celulares",
        "Monitor": "Eletrônicos",
        "Teclado": "Acessórios",
        "Mouse": "Acessórios"
    }

    regioes = [
        "Sudeste",
        "Sul",
        "Nordeste",
        "Centro-Oeste",
        "Norte"
    ]

    cabecalho = [
        "id_venda",
        "data_venda",
        "cliente",
        "produto",
        "categoria",
        "regiao",
        "quantidade",
        "preco_unitario"
    ]

    dados = []

    for numero in range(1, n_registros + 1):
        produto = random.choice(produtos)

        # Em aproximadamente 5% das linhas, a quantidade ficará vazia.
        if random.random() > 0.05:
            quantidade = str(random.randint(1, 8))
        else:
            quantidade = ""

        # Em aproximadamente 5% das linhas, o preço ficará vazio.
        if random.random() > 0.05:
            preco = str(round(random.uniform(100, 3500), 2))
        else:
            preco = ""

        # Insere espaços em alguns produtos para testar a limpeza.
        if random.random() < 0.10:
            nome_produto = f"  {produto}  "
        else:
            nome_produto = produto

        linha = [
            numero,
            f"2024-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}",
            f"Cliente_{random.randint(1, 30):03d}",
            nome_produto,
            categorias[produto],
            random.choice(regioes),
            quantidade,
            preco
        ]

        dados.append(linha)

    with open(
        caminho_arquivo,
        mode="w",
        newline="",
        encoding="utf-8"
    ) as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerow(cabecalho)
        escritor.writerows(dados)

    print(f"[OK] Dataset gerado em: {caminho_arquivo}")


def carregar_csv(caminho_arquivo):
    """Lê o arquivo CSV e retorna uma lista de dicionários."""

    dados = []

    with open(
        caminho_arquivo,
        mode="r",
        newline="",
        encoding="utf-8"
    ) as arquivo:
        leitor = csv.DictReader(arquivo)

        for linha in leitor:
            dados.append(linha)

    return dados


def inspecionar_dados(dados):
    """Exibe informações gerais e conta registros incompletos."""

    print("\n=== INSPEÇÃO INICIAL DOS DADOS ===")
    print(f"Total de registros carregados: {len(dados)}")

    if not dados:
        print("O dataset está vazio.")
        return

    print(f"Campos disponíveis: {list(dados[0].keys())}")
    print(f"Exemplo do primeiro registro: {dados[0]}")

    incompletos = 0

    for linha in dados:
        quantidade = linha.get("quantidade", "").strip()
        preco = linha.get("preco_unitario", "").strip()

        if not quantidade or not preco:
            incompletos += 1

    print(f"Registros com quantidade ou preço vazio: {incompletos}")


def limpar_dados(dados_brutos):
    """Remove linhas inválidas, limpa textos e converte tipos."""

    dados_limpos = []
    removidos = 0

    for linha in dados_brutos:
        try:
            id_venda_texto = linha.get("id_venda", "").strip()
            quantidade_texto = linha.get("quantidade", "").strip()
            preco_texto = linha.get("preco_unitario", "").strip()

            # Se algum valor obrigatório estiver vazio, a linha é ignorada.
            if not id_venda_texto or not quantidade_texto or not preco_texto:
                removidos += 1
                continue

            id_venda = int(id_venda_texto)
            quantidade = int(quantidade_texto)
            preco = float(preco_texto)

            # Valores iguais ou menores que zero não representam venda válida.
            if quantidade <= 0 or preco <= 0:
                removidos += 1
                continue

            registro_limpo = {
                "id_venda": id_venda,
                "data_venda": linha.get("data_venda", "").strip(),
                "cliente": linha.get("cliente", "").strip(),
                "produto": linha.get("produto", "").strip(),
                "categoria": linha.get("categoria", "").strip(),
                "regiao": linha.get("regiao", "").strip(),
                "quantidade": quantidade,
                "preco_unitario": preco
            }

            # Confere se os principais textos estão preenchidos.
            if (
                not registro_limpo["cliente"]
                or not registro_limpo["produto"]
                or not registro_limpo["categoria"]
                or not registro_limpo["regiao"]
            ):
                removidos += 1
                continue

            dados_limpos.append(registro_limpo)

        except (ValueError, TypeError):
            removidos += 1

    print("\n=== RELATÓRIO DE LIMPEZA ===")
    print(f"Registros válidos: {len(dados_limpos)}")
    print(f"Registros removidos: {removidos}")

    return dados_limpos


def criar_campos_derivados(dados):
    """Adiciona receita_total e faixa_preco a cada venda."""

    for item in dados:
        receita = round(
            item["quantidade"] * item["preco_unitario"],
            2
        )

        item["receita_total"] = receita

        if receita < 500:
            item["faixa_preco"] = "Baixo"
        elif receita <= 2000:
            item["faixa_preco"] = "Médio"
        else:
            item["faixa_preco"] = "Alto"

    return dados


def processar_transformacao(dados, funcao_transformacao):
    """Aplica uma função recebida por parâmetro a todos os registros."""

    resultados = []

    for item in dados:
        item_transformado = funcao_transformacao(item)
        resultados.append(item_transformado)

    return resultados


def calcular_metricas(dados):
    """Calcula receitas por categoria, por região e o total geral."""

    receita_categoria = {}
    receita_regiao = {}
    total_geral = 0.0

    for item in dados:
        categoria = item["categoria"]
        regiao = item["regiao"]
        receita = item["receita_total"]

        receita_categoria[categoria] = (
            receita_categoria.get(categoria, 0.0) + receita
        )

        receita_regiao[regiao] = (
            receita_regiao.get(regiao, 0.0) + receita
        )

        total_geral += receita

    # Arredonda os resultados somente depois das somas.
    for categoria in receita_categoria:
        receita_categoria[categoria] = round(
            receita_categoria[categoria],
            2
        )

    for regiao in receita_regiao:
        receita_regiao[regiao] = round(
            receita_regiao[regiao],
            2
        )

    return {
        "total_geral": round(total_geral, 2),
        "por_categoria": receita_categoria,
        "por_regiao": receita_regiao
    }


def segmentar_clientes(dados):
    """Soma os gastos dos clientes e define seus segmentos."""

    gastos_cliente = {}

    for item in dados:
        cliente = item["cliente"]
        receita = item["receita_total"]

        gastos_cliente[cliente] = (
            gastos_cliente.get(cliente, 0.0) + receita
        )

    segmentos = {}

    for cliente, total in gastos_cliente.items():
        if total > 8000:
            segmento = "Ouro"
        elif total >= 3000:
            segmento = "Prata"
        else:
            segmento = "Bronze"

        segmentos[cliente] = {
            "total_gasto": round(total, 2),
            "segmento": segmento
        }

    return segmentos


def obter_top_clientes(clientes, top_n=5):
    """Retorna os clientes com os maiores gastos."""

    clientes_ordenados = sorted(
        clientes.items(),
        key=lambda item: item[1]["total_gasto"],
        reverse=True
    )

    return clientes_ordenados[:top_n]


def exportar_resultados(
    metricas,
    clientes,
    pasta_saida="outputs"
):
    """Exporta as métricas para arquivos JSON e CSV."""

    os.makedirs(pasta_saida, exist_ok=True)

    caminho_json = os.path.join(
        pasta_saida,
        "estatisticas.json"
    )

    conteudo_json = {
        "metricas_gerais": metricas,
        "clientes": clientes
    }

    with open(
        caminho_json,
        mode="w",
        encoding="utf-8"
    ) as arquivo:
        json.dump(
            conteudo_json,
            arquivo,
            indent=4,
            ensure_ascii=False
        )

    print(f"[OK] Arquivo JSON exportado em: {caminho_json}")

    caminho_csv = os.path.join(
        pasta_saida,
        "metricas_resumo.csv"
    )

    with open(
        caminho_csv,
        mode="w",
        newline="",
        encoding="utf-8"
    ) as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerow(["Categoria", "Receita Total"])

        for categoria, receita in metricas["por_categoria"].items():
            escritor.writerow([categoria, receita])

    print(f"[OK] Arquivo CSV exportado em: {caminho_csv}")