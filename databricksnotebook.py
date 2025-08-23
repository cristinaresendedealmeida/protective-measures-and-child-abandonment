# Importar bibliotecas necessárias
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from azure.storage.blob import BlobServiceClient

# Credenciais e informações do container
ACCOUNT_NAME = "storage-name-here"
SAS_TOKEN = "sas-token-here"
CONTAINER_RAW = "container-name-here"
BLOB_BASE_URL = f"https://storage-name-here.blob.core.windows.net"

# Nome do arquivo
arquivo_csv = "qt_protetiva_criancas_casas_acolhimento_2025.csv"

# Conectar e baixar o arquivo
def baixar_csv(container_name, blob_name):
    svc = BlobServiceClient(account_url=BLOB_BASE_URL, credential=SAS_TOKEN)
    cont = svc.get_container_client(container_name)
    blob_data = cont.download_blob(blob_name)
    return pd.read_csv(blob_data, thousands='.') 

# Ler o arquivo diretamente para o DataFrame
df = baixar_csv(CONTAINER_RAW, arquivo_csv)

# Exibir as primeiras linhas para confirmar a leitura correta
print("DataFrame antes do processamento:")
print(df.head())

# Limpeza e preparação dos dados
# Reordenar o DataFrame pela quantidade de medidas protetivas, do maior para o menor
# Usamos .sort_values() diretamente no DataFrame lido
df_ordenado = df.sort_values(by='Quantidade de Medidas Protetivas', ascending=False)

# Adicionar o estilo ao gráfico (opcional)
sns.set_theme(style="whitegrid")

# Criar o gráfico
plt.figure(figsize=(20, 10))
ax = df_ordenado.plot(x='UF', y=['Quantidade de Medidas Protetivas', 'Criancas em Casas de Acolhimento'], kind='bar', figsize=(20, 10))

# Ajustar o layout e adicionar títulos
plt.title('Comparativo de Medidas Protetivas vs. Crianças em Casas de Acolhimento por UF', fontsize=18, pad=20)
plt.ylabel('Quantidade', fontsize=14)
plt.xlabel('UF', fontsize=14)
plt.xticks(rotation=90)
plt.legend(title='Tipo de Dado', fontsize=12)
plt.tight_layout()

# Mostrar o gráfico
plt.show()
