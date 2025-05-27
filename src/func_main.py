import csv
import json
from typing import List, Dict
from pathlib import Path
import os

def carregar_arquivo(caminho_arquivo:str) -> List[Dict]:
    """
    Procura pelo arquivo, verifica se é um CSV ou JSON e por fim, retorna
    uma lista com dicionarios.
    """
    try:
        with open(caminho_arquivo, "r") as arquivo:
            if caminho_arquivo.endswith('.csv'):
                return list(csv.DictReader(arquivo))
            elif caminho_arquivo.endswith('.json'):
                return json.load(arquivo)
            else:
                raise ValueError("Formato de arquivo não suportado")
    except Exception as e:
        print(f"Erro ao carregar arquivo: {e}")
        return None

def processar_dados(dados:List[Dict]) -> dict:
    """
    Processa os dados e retorna estatísticas.

    Esse codigo pode ser moldado para sua necessidade, por exemplo aqui eu
    resolvi fazer o codigo pensando que estou manipulando um historico escolar, 
    com notas e media.

    O mais importante é seu retorno que deve ser uma dicionario(dict) para manter
    o funcionamento.
    """

    if not dados:
        return None

    #passo por cada item da lista e depois recupero chave[valor] do dicionario     
    for item in dados:
        for chave, valor in item.items():
            if isinstance(valor, str) and valor.replace('.', '').isdigit():
                #converto apenas as notas para float
                if chave == "nota":
                    item[chave] = float(valor)
                else:
                    item[chave] = int(valor)
    
    #separo os valores encontrados em variaveis para facilitar a manipulação 
    aprovados = [item for item in dados if item.get("nota",0)>=6]
    media = sum(item.get('nota', 0) for item in dados) / len(dados)
    nota_max = max(item.get('nota', 0) for item in dados)
    nota_min = min(item.get('nota', 0) for item in dados)

    #crio um dicionario e retorno o mesmo
    estatisticas = {
        'total_registros': len(dados),
        'media_notas': media,
        'max_nota': nota_max,
        'min_nota': nota_min,
        'aprovados': aprovados,
    }

    return estatisticas

def gerar_relatorio(resultados: dict, arquivo_saida:str ="relatorios") -> str:
    """
    Crio o relatorio com varias informações coletadas na função processar_dados(), dando
    uma visão mais geral.

    O relatorio pode apresentar diferentes dados, porem, isso vai depender do dicionario(dict)
    gerado pela função processar_dados(). Depois com os dados selecionados, é possivel alterar
    como é escrito e apresentado com "with open()".

    Por fim, é importante não alterar o seu retorno e manter do jeito que está.
    """
    if resultados is None:
        raise ValueError("Dados de entrada inválidos (None)")

    if not os.path.exists(arquivo_saida):
        os.makedirs(arquivo_saida, exist_ok=True)
    
    #crio o primeiro relatorio, e se ja tiver, crie um novo
    numero = 1
    while True:
        nome_arquivo = f"relatorio_{numero}.txt" 
        caminho_novo = Path(arquivo_saida)/nome_arquivo
        if not caminho_novo.exists():
            break
        numero += 1

    #escrevendo todas as informações no relatorio
    with open(caminho_novo, 'w', encoding='utf-8') as arquivo:
        arquivo.write("=== RELATÓRIO DE ANÁLISE ===\n\n")
        arquivo.write(f"Total de registros: {resultados['total_registros']}\n")
        arquivo.write(f"Média de notas: {resultados['media_notas']:.2f}\n")
        arquivo.write(f"Maior nota: {resultados['max_nota']}\n")
        arquivo.write(f"Menor nota: {resultados['min_nota']}\n\n")
        
        arquivo.write("=== APROVADOS (nota >= 7) ===\n")
        for aprovado in resultados['aprovados']:
            arquivo.write(f"{aprovado['nome']} - Nota: {aprovado['nota']}\n")

    #retorno o caminho desse novo relatorio
    return str(caminho_novo)