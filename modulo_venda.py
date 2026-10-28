## Arquivo de módulo com as funções de vendas ###
# python
import csv
import random

def gerar_dataset_sintetico(
    caminho_arquivo="vendas.csv",
    n_registros=150,
    seed=42
):
    random.seed(seed)

    produtos = [
        "Notebook", "Smartphone", "Tablet",
        "Monitor", "Teclado", "Mouse"
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
        "Sudeste", "Sul", "Nordeste",
        "Centro-Oeste", "Norte"
    ]

    cabecalho = [
        "id_venda", "data_venda", "cliente",
        "produto", "categoria", "regiao",
        "quantidade", "preco_unitario"
    ]

    with open(
        caminho_arquivo,
        "w",
        newline="",
        encoding="utf-8"
    ) as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerow(cabecalho)

        for i in range(1, n_registros + 1):
            produto = random.choice(produtos)
            quantidade = (
                random.randint(1, 8)
                if random.random() > 0.05
                else ""
            )
            preco = (
                round(random.uniform(100, 3500), 2)
                if random.random() > 0.05
                else ""
            )

            nome_produto = (
                f"  {produto} "
                if random.random() < 0.1
                else produto
            )

            escritor.writerow([
                i,
                f"2024-{random.randint(1, 12):02d}-"
                f"{random.randint(1, 28):02d}",
                f"Cliente_{random.randint(1, 30):03d}",
                nome_produto,
                categorias[produto],
                random.choice(regioes),
                quantidade,
                preco
            ])

    print(f"Dataset criado: {caminho_arquivo}")
    