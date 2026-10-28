# ### Arquivo principal do sofware ###
import os
import modulo_vendas as mv


def main():
    print("=" * 60)
    print(" SALESINSIGHT PY - Pipeline de Análise de Vendas")
    print("=" * 60)

    arquivo_dados = "vendas.csv"

    # 1. Cria uma base sintética caso o arquivo ainda não exista.
    if not os.path.exists(arquivo_dados):
        mv.gerar_dataset_sintetico(arquivo_dados, n_registros=150)

    # 2. Carrega e inspeciona os dados brutos.
    dados_brutos = mv.carregar_csv(arquivo_dados)
    mv.inspecionar_dados(dados_brutos)

    # 3. Limpa e transforma os registros.
    dados_limpos = mv.limpar_dados(dados_brutos)
    dados_transformados = mv.criar_campos_derivados(dados_limpos)

    # Exemplo de função de ordem superior com lambda.
    dados_com_tag = mv.processar_transformacao(
        dados_transformados,
        lambda x: {**x, "processado": True}
    )

    # 4. Calcula métricas e segmenta clientes.
    metricas = mv.calcular_metricas(dados_com_tag)
    segmentos = mv.segmentar_clientes(dados_com_tag)
    top_clientes = mv.obter_top_clientes(segmentos, top_n=5)

    # 5. Exibe um resumo executivo.
    print("\n=== RESUMO EXECUTIVO ===")
    print(f"Receita total da empresa: R$ {metricas['total_geral']:,.2f}")
    print("\nTop 5 clientes por gasto:")
    for cliente, info in top_clientes:
        print(
            f" - {cliente}: R$ 
            {info['total_gasto']:,.2f} "
            f"({info['segmento']})"
        )

    # 6. Exporta os relatórios.
    mv.exportar_resultados(metricas, segmentos)
    print("\n[CONCLUÍDO] Pipeline executado com sucesso!")


if __name__ == "__main__":
    main()
main.py 
