from src.func_main import carregar_arquivo, processar_dados, gerar_relatorio

def main():
    # Exemplo de uso
    dados = carregar_arquivo("data/input/dados_csv.csv")
    if dados:
        resultados = processar_dados(dados)
        caminho_relatorio = gerar_relatorio(resultados, "data/output")
        print(f"Relatório gerado em: {caminho_relatorio}")

if __name__ == "__main__":
    main()