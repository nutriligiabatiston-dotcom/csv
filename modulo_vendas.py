import csv
import json
import os
import random


def gerar_dataset_sintetico(caminho_arquivo="vendas.csv", n_registros=150, seed=42):
    """Cria uma base sintética reproduzível para praticar o pipeline."""
    random.seed(seed)
    produtos = ["Notebook", "Smartphone", "Tablet", "Monitor", "Teclado", "Mouse"]
    categorias = {
        "Notebook": "Eletrônicos",
        "Smartphone": "Celulares",
        "Tablet": "Celulares",
        "Monitor": "Eletrônicos",
        "Teclado": "Acessórios",
        "Mouse": "Acessórios",
    }
    regioes = ["Sudeste", "Sul", "Nordeste", "Centro-Oeste", "Norte"]
    cabecalho = [
        "id_venda", "data_venda", "cliente", "produto", "categoria",
        "regiao", "quantidade", "preco_unitario"
    ]
    with open(caminho_arquivo, "w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerow(cabecalho)
        for i in range(1, n_registros + 1):
            produto = random.choice(produtos)
            quantidade = str(random.randint(1, 8)) if random.random() > 0.05 else ""
            preco = (
                str(round(random.uniform(100, 3500), 2))
                if random.random() > 0.05 else ""
            )
            nome_produto = f"  {produto} " if random.random() < 0.1 else produto
            escritor.writerow([
                i,
                f"2024-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}",
                f"Cliente_{random.randint(1, 30):03d}",
                nome_produto,
                categorias[produto],
                random.choice(regioes),
                quantidade,
                preco,
            ])
    print(f"[OK] Dataset gerado: {caminho_arquivo}")


def carregar_csv(caminho_arquivo):
    """Lê o CSV e devolve uma lista de dicionários."""
    with open(caminho_arquivo, "r", newline="", encoding="utf-8") as arquivo:
        return list(csv.DictReader(arquivo))


def inspecionar_dados(dados):
    print("\n=== INSPEÇÃO INICIAL DOS DADOS ===")
    print(f"Total de registros carregados: {len(dados)}")
    if dados:
        print(f"Campos disponíveis: {list(dados[0].keys())}")
        print(f"Exemplo do primeiro registro: {dados[0]}")
        incompletos = sum(
            1 for linha in dados
            if any(valor is None or str(valor).strip() == "" for valor in linha.values())
        )
        print(f"Registros com pelo menos um campo vazio: {incompletos}")


def limpar_dados(dados_brutos):
    """Remove registros sem quantidade/preço ou com valores numéricos inválidos."""
    dados_limpos = []
    removidos = 0
    for linha in dados_brutos:
        try:
            produto = linha["produto"].strip()
            categoria = linha["categoria"].strip()
            regiao = linha["regiao"].strip()
            cliente = linha["cliente"].strip()
            data_venda = linha["data_venda"].strip()
            quantidade_txt = linha["quantidade"].strip()
            preco_txt = linha["preco_unitario"].strip()

            if not all([produto, categoria, regiao, cliente, data_venda,
                        quantidade_txt, preco_txt]):
                removidos += 1
                continue

            quantidade = int(quantidade_txt)
            preco = float(preco_txt)
            if quantidade <= 0 or preco < 0:
                removidos += 1
                continue

            dados_limpos.append({
                "id_venda": int(linha["id_venda"]),
                "data_venda": data_venda,
                "cliente": cliente,
                "produto": produto,
                "categoria": categoria,
                "regiao": regiao,
                "quantidade": quantidade,
                "preco_unitario": preco,
            })
        except (ValueError, KeyError, AttributeError):
            removidos += 1

    print("\n=== RELATÓRIO DE LIMPEZA ===")
    print(f"Registros válidos: {len(dados_limpos)} | Registros removidos: {removidos}")
    return dados_limpos


def criar_campos_derivados(dados):
    for item in dados:
        receita = round(item["quantidade"] * item["preco_unitario"], 2)
        item["receita_total"] = receita
        # Faixa de preço conforme o enunciado: valor da receita calculada.
        if receita < 500:
            item["faixa_preco"] = "Baixo"
        elif receita <= 2000:
            item["faixa_preco"] = "Médio"
        else:
            item["faixa_preco"] = "Alto"
    return dados


def processar_transformacao(dados, funcao):
    """Aplica uma função recebida a cada registro (exemplo de ordem superior)."""
    return [funcao(item) for item in dados]


def calcular_metricas(dados):
    receita_categoria = {}
    receita_regiao = {}
    total_geral = 0.0
    for item in dados:
        categoria = item["categoria"]
        regiao = item["regiao"]
        receita = item["receita_total"]
        receita_categoria[categoria] = round(
            receita_categoria.get(categoria, 0.0) + receita, 2
        )
        receita_regiao[regiao] = round(
            receita_regiao.get(regiao, 0.0) + receita, 2
        )
        total_geral += receita
    return {
        "total_geral": round(total_geral, 2),
        "por_categoria": receita_categoria,
        "por_regiao": receita_regiao,
    }


def segmentar_clientes(dados):
    gastos_cliente = {}
    for item in dados:
        cliente = item["cliente"]
        gastos_cliente[cliente] = (
            gastos_cliente.get(cliente, 0.0) + item["receita_total"]
        )

    segmentos = {}
    for cliente, total in gastos_cliente.items():
        if total > 8000:
            categoria = "Ouro"
        elif total >= 3000:
            categoria = "Prata"
        else:
            categoria = "Bronze"
        segmentos[cliente] = {
            "total_gasto": round(total, 2),
            "segmento": categoria,
        }
    return segmentos


def obter_top_clientes(segmentos, top_n=5):
    return sorted(
        segmentos.items(),
        key=lambda par: par[1]["total_gasto"],
        reverse=True,
    )[:top_n]


def exportar_resultados(metricas, clientes, pasta_saida="outputs"):
    os.makedirs(pasta_saida, exist_ok=True)
    caminho_json = os.path.join(pasta_saida, "estatisticas.json")
    with open(caminho_json, "w", encoding="utf-8") as arquivo:
        json.dump(
            {"metricas_gerais": metricas, "clientes": clientes},
            arquivo, indent=4, ensure_ascii=False
        )

    caminho_csv = os.path.join(pasta_saida, "metricas_resumo.csv")
    with open(caminho_csv, "w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerow(["Categoria", "Receita Total"])
        for categoria, receita in metricas["por_categoria"].items():
            escritor.writerow([categoria, receita])

    print(f"[OK] JSON exportado: {caminho_json}")
    print(f"[OK] CSV exportado: {caminho_csv}")
