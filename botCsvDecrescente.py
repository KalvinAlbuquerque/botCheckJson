import csv
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Função para extrair os dados do arquivo .txt
def extrair_dados(txt_file):
    vulnerabilidades = []

    # Abre o arquivo de texto
    with open(txt_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Variáveis auxiliares
    vulnerabilidade = ""
    total_uri_afetadas = 0

    for line in lines:
        # Detecta a linha com a vulnerabilidade
        if line.startswith("Vulnerabilidade:"):
            if vulnerabilidade:  # Se já houver uma vulnerabilidade coletada
                vulnerabilidades.append((vulnerabilidade, total_uri_afetadas))

            vulnerabilidade = line.split(":", 1)[1].strip()

        # Detecta a linha com o total de URIs afetadas
        elif line.startswith("Total de URI Afetadas:"):
            total_uri_afetadas = int(line.split(":", 1)[1].strip())

    # Adiciona a última vulnerabilidade encontrada
    if vulnerabilidade:
        vulnerabilidades.append((vulnerabilidade, total_uri_afetadas))

    return vulnerabilidades

# Função para salvar os dados no formato CSV
def salvar_csv(dados, output_file):
    # Ordena os dados por total de URIs afetadas, em ordem decrescente
    dados_ordenados = sorted(dados, key=lambda x: x[1], reverse=True)

    # Escreve os dados em um arquivo CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Vulnerabilidade', 'Total de URI Afetadas'])  # Cabeçalho
        for vulnerabilidade, total in dados_ordenados:
            writer.writerow([vulnerabilidade, total])

# Função para plotar o gráfico das 10 vulnerabilidades mais frequentes
def plotar_vulnerabilidades(csv_file):
    # Lê o arquivo CSV com os dados de vulnerabilidade
    dados = pd.read_csv(csv_file)

    # Ordena os dados por 'Total de URI Afetadas' em ordem decrescente
    dados_ordenados = dados.sort_values(by='Total de URI Afetadas', ascending=False)

    # Seleciona as 10 vulnerabilidades mais frequentes
    top_10_vulnerabilidades = dados_ordenados.head(10)

    # Gerar um gradiente de cores personalizadas para as barras
    cores = plt.cm.Blues(np.linspace(0.3, 0.7, len(top_10_vulnerabilidades)))

    # Plotando o gráfico de barras horizontais
    plt.figure(figsize=(12, 7))
    barras = plt.barh(top_10_vulnerabilidades['Vulnerabilidade'], top_10_vulnerabilidades['Total de URI Afetadas'], color=cores, edgecolor='black')

    # Adiciona os valores nas barras
    for barra in barras:
        plt.text(barra.get_width(), barra.get_y() + barra.get_height() / 2, f'{barra.get_width()}', va='center', ha='left', color='white', fontweight='bold')

    # Título e rótulos
    plt.title('Top 10 Vulnerabilidades Mais Frequentes em Sites', fontsize=18, fontweight='bold', color='darkblue')
    plt.xlabel('Total de Sites Afetados', fontsize=14, fontweight='bold', color='darkblue')
    plt.ylabel('Vulnerabilidade', fontsize=14, fontweight='bold', color='darkblue')

    # Melhoria no layout
    plt.tight_layout()

    # Exibe o gráfico
    plt.show()

if __name__ == "__main__":
    # Caminho para o arquivo de entrada e saída
    arquivo_entrada = 'dados_extraidos.txt'  # Nome do arquivo .txt
    arquivo_saida = 'vulnerabilidades.csv'  # Nome do arquivo .csv

    # Extrai os dados do arquivo .txt
    dados = extrair_dados(arquivo_entrada)

    # Salva os dados no arquivo CSV
    salvar_csv(dados, arquivo_saida)

    print(f"Dados salvos em {arquivo_saida}")

    plotar_vulnerabilidades(arquivo_saida)
