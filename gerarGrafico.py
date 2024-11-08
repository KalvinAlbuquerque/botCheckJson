import pandas as pd
import matplotlib.pyplot as plt

# Carregar dados
df = pd.read_csv('relatorio.csv')

# Configuração de dados para barras empilhadas
sites = df['Site']
critical = df['Critical']
high = df['High']
medium = df['Medium']
low = df['Low']

# Somar o total de vulnerabilidades por site
df['Total Vulnerabilities'] = critical + high + medium + low

# Criar gráfico de barras empilhadas
plt.figure(figsize=(16, 10))

# Usar cores mais condizentes com o risco
plt.bar(sites, low, label='Low', color='#ADD8E6')  # Azul Claro
plt.bar(sites, medium, bottom=low, label='Medium', color='#FFEB3B')  # Amarelo Ouro
plt.bar(sites, high, bottom=low + medium, label='High', color='#FF9800')  # Laranja
plt.bar(sites, critical, bottom=low + medium + high, label='Critical', color='#F44336')  # Vermelho Escuro

# Adicionar números nas barras com fonte maior
for i, v in enumerate(low):
    plt.text(sites[i], v / 2, str(v), ha='center', va='center', fontsize=12, fontweight='bold', color='black')
for i, v in enumerate(medium):
    plt.text(sites[i], low[i] + v / 2, str(v), ha='center', va='center', fontsize=12, fontweight='bold', color='black')
for i, v in enumerate(high):
    plt.text(sites[i], low[i] + medium[i] + v / 2, str(v), ha='center', va='center', fontsize=12, fontweight='bold', color='black')
for i, v in enumerate(critical):
    plt.text(sites[i], low[i] + medium[i] + high[i] + v / 2, str(v), ha='center', va='center', fontsize=12, fontweight='bold', color='black')

# Configuração do gráfico
plt.xlabel('Sites', fontsize=14, fontweight='bold')
plt.ylabel('Número de Vulnerabilidades', fontsize=14, fontweight='bold')
plt.title('Vulnerabilidades por Site', fontsize=16, fontweight='bold')
plt.xticks(rotation=90)
plt.legend()
plt.tight_layout()

# Exibir gráfico
plt.show()

# Gerar gráfico do total de vulnerabilidades por site
plt.figure(figsize=(16, 10))
plt.bar(sites, df['Total Vulnerabilities'], color='#4CAF50')  # Cor sólida verde

# Adicionar números nas barras do total de vulnerabilidades com fonte maior
for i, v in enumerate(df['Total Vulnerabilities']):
    plt.text(sites[i], v + 0.2, str(v), ha='center', va='bottom', fontsize=14, fontweight='bold', color='black')

# Configuração do gráfico
plt.xlabel('Sites', fontsize=14, fontweight='bold')
plt.ylabel('Total de Vulnerabilidades', fontsize=14, fontweight='bold')
plt.title('Total de Vulnerabilidades por Site', fontsize=16, fontweight='bold')
plt.xticks(rotation=90)
plt.tight_layout()

# Exibir gráfico
plt.show()
