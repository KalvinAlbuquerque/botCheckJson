import json
import glob
import os
import pandas as pd

JSON_PATH = "arquivos_json"
CSV_PATH = "relatorio.csv"

# Função para carregar todos os arquivos JSON do diretório especificado
def carregarArquivos(file_path) -> list:
    json_files = glob.glob(f'{JSON_PATH}/*.json') 
    return json_files

# Função para extrair os dados de cada arquivo JSON e adicionar ao CSV
def extrair_dados(files, output_file):
    new_rows = []
    for file in files:
        with open(file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Extrair o site (target) do JSON
        target = data.get('scan', {}).get('target', 'Não disponível')
        if target != 'Não disponível':
            risk_factor_counts = {'High': 0, 'Critical': 0, 'Low': 0, 'Medium': 0}
            for finding in data.get('findings', []):
                risk_factor = finding.get('risk_factor', 'Não disponível')
                if "info" not in risk_factor:
                    if risk_factor.lower() == 'high':
                        risk_factor_counts['High'] += 1
                    elif risk_factor.lower() == 'critical':
                        risk_factor_counts['Critical'] += 1
                    elif risk_factor.lower() == 'low':
                        risk_factor_counts['Low'] += 1
                    elif risk_factor.lower() == 'medium':
                        risk_factor_counts['Medium'] += 1
        
            #Extrai apenas o nome do site
            cleaned_target = target.replace('http://', '').replace('https://', '').split('.saude')[0]

             # Adiciona a nova linha à lista
            new_rows.append({
                'Site': cleaned_target,
                'Critical': risk_factor_counts['Critical'],
                'High': risk_factor_counts['High'],
                'Medium': risk_factor_counts['Medium'],
                'Low': risk_factor_counts['Low']
            })
            
    add_lines_csv(new_rows)


def create_csv() -> None:
    # Cria o CSV com as colunas desejadas e apaga o conteúdo anterior (se existir)
    if not os.path.exists(CSV_PATH):
        df = pd.DataFrame(columns=['Site', 'Critical', 'High', 'Medium', 'Low'])
        df.to_csv(CSV_PATH, index=False)
    else:
        # Se o arquivo CSV já existir, apaga o conteúdo para começar de novo
        open(CSV_PATH, 'w').close()
        df = pd.DataFrame(columns=['Site', 'Critical', 'High', 'Medium', 'Low'])
        df.to_csv(CSV_PATH, index=False)


def add_lines_csv(new_rows: list) -> None:
        
        # Lê o CSV existente
        df = pd.read_csv(CSV_PATH)

        # Cria um DataFrame a partir das novas linhas
        new_df = pd.DataFrame(new_rows)

         # Concatena os DataFrames (adiciona as novas linhas)
        df = pd.concat([df, new_df], ignore_index=True)

        # Salva o DataFrame atualizado de volta no CSV
        df.to_csv(CSV_PATH, index=False)


if __name__ == "__main__":
    # Carrega os arquivos JSON
    files = carregarArquivos(JSON_PATH)

    # Cria o arquivo CSV caso ele não exista
    create_csv()

    # Extrai os dados dos arquivos JSON e adiciona ao CSV
    extrair_dados(files, CSV_PATH)
    print(f"Dados extraídos e salvos com sucesso no arquivo: {CSV_PATH}")
