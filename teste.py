import json

# Carrega o arquivo JSON
with open('WAS_http___educacao_nti_saude_salvador_ba_gov_br.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Conta o total de vulnerabilidades
total_vulnerabilities = len(data.get('findings', []))
print(f'Total de vulnerabilidades: {total_vulnerabilities}')
