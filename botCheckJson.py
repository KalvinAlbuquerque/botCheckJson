import json
import os
from collections import defaultdict
from urllib.parse import urlparse, urljoin

# Função para extrair o domínio raiz do target
def extrair_dominio(target):
    parsed_url = urlparse(target)
    return f"{parsed_url.scheme}://{parsed_url.netloc}"

# Função para formatar a URI conforme o target
def formatar_uri(target, uri):
    target_domain = extrair_dominio(target)
    parsed_uri = urlparse(uri)
    
    if not parsed_uri.netloc:
        return urljoin(target_domain, uri)
    else:
        return target_domain

# Função para ler múltiplos arquivos JSON, contar vulnerabilidades e salvar as informações em um arquivo
def extrair_dados(json_files, output_file):
    try:
        risk_factor_counts = {'High': 0, 'Critical': 0, 'Low': 0, 'Medium': 0}
        common_vulnerabilities = defaultdict(list)
        targets = []

        for json_file in json_files:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            target = data.get('scan', {}).get('target', 'Não disponível')
            if target != 'Não disponível' and target not in targets:
                targets.append(target)
            
            for finding in data.get('findings', []):
                risk_factor = finding.get('risk_factor', 'Não disponível')
                uri = finding.get('uri', 'Não disponível')
                name = finding.get('name', 'Não disponível')
                plugin_id = finding.get('plugin_id', 'Não disponível')
                
                if "info" not in risk_factor:
                    if risk_factor.lower() == 'high':
                        risk_factor_counts['High'] += 1
                    elif risk_factor.lower() == 'critical':
                        risk_factor_counts['Critical'] += 1
                    elif risk_factor.lower() == 'low':
                        risk_factor_counts['Low'] += 1
                    elif risk_factor.lower() == 'medium':
                        risk_factor_counts['Medium'] += 1
                    
                    formatted_uri = formatar_uri(target, uri)
                    common_vulnerabilities[(name,plugin_id)].append(formatted_uri)

        with open(output_file, 'w', encoding='utf-8') as output:
            output.write("Resumo das Vulnerabilidades por Risk Factor:\n\n")
            output.write(f"High: {risk_factor_counts['High']}\n")
            output.write(f"Critical: {risk_factor_counts['Critical']}\n")
            output.write(f"Low: {risk_factor_counts['Low']}\n")
            output.write(f"Medium: {risk_factor_counts['Medium']}\n\n")
            
            output.write("Vulnerabilidades em comum, entre os sites/URI:\n\n")
            for (name,plugin_id), uris in common_vulnerabilities.items():
                if len(uris) > 1:
                    unique_uris = set(uris)
                    output.write(f"{name}\n")
                    output.write(f"Plugin ID:{plugin_id}\n")
                    output.write(f"URI Afetadas: {', '.join(unique_uris)}\n\n")

            output.write("Domínios analisados:\n")
            output.write("\n".join(targets))
        
        print(f"Dados extraídos e salvos com sucesso no arquivo: {output_file}")

    except FileNotFoundError:
        print(f"Erro: Um dos arquivos JSON não foi encontrado.")
    except json.JSONDecodeError:
        print("Erro: Um dos arquivos não é um JSON válido.")
    except Exception as e:
        print(f"Erro inesperado: {e}")

# Usando glob ou os para obter os arquivos JSON automaticamente:
import glob

# Caminho para o diretório onde estão os arquivos JSON
diretorio_json = 'arquivos_json' # Substitua pelo caminho correto

# Encontrar todos os arquivos JSON no diretório
json_files = glob.glob(f'{diretorio_json}/*.json')  # Ou use os.listdir() se preferir

# Arquivo de saída
output_file = 'dados_extraidos.txt'

# Executar a função com os arquivos encontrados
extrair_dados(json_files, output_file)
