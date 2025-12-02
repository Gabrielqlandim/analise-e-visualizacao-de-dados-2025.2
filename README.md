# Pipeline de BI para Previsão de Umidade Relativa (INMET – Salgueiro/PE)

Este repositório contém um pipeline completo de Business Intelligence (BI) desenvolvido para a disciplina **Análise e Visualização de Dados – CESAR School (2025.2)**.  
O projeto integra *ingestão*, *armazenamento*, *processamento*, *modelagem preditiva* e *visualização* de dados meteorológicos reais fornecidos pelo **INMET**.

A variável prevista é a **Umidade Relativa (%)** da estação automática de **Salgueiro – Pernambuco**, utilizando como entradas:
- Temperatura do ar (°C)
- Pressão atmosférica (mb)
- Radiação solar (kJ/m²)

---

## Objetivos do Projeto

- Construir um pipeline completo de ponta a ponta usando Docker e serviços distribuídos.  
- Ingerir arquivos CSV do INMET por meio de uma API FastAPI.  
- Armazenar dados em um banco PostgreSQL (NeonDB).  
- Processar e modelar os dados usando Jupyter Notebook.  
- Treinar um modelo de **Regressão Linear (scikit-learn)** para prever Umidade Relativa.  
- Registrar experimentos no **MLflow**.  
- Visualizar resultados em dashboards do **ThingsBoard/Trendz**.

---

## Arquitetura Geral do Pipeline

O pipeline é composto pelos seguintes módulos:

### **1. Ingestão – FastAPI**
- Recebe arquivos CSV via endpoint `/Ingest-File`.
- Exibe documentação automática via Swagger:  
  ➜ http://localhost:8000/docs  
- Permite validações antes do envio ao armazenamento.

### **2. Armazenamento – PostgreSQL (NeonDB)**
- Armazena dados limpos e consultados pelo notebook.
- Conexão testada pelo script `neonDb_connection.py`.

### **3. Processamento – Python + Jupyter**
Scripts e notebooks realizam:
- Limpeza dos dados  
- Padronização de tipos  
- Seleção de variáveis  
- Treinamento do modelo  
- Avaliação  

Notebook principal:
analise_dados_do_bd.ipynb

### **4. Modelagem – MLflow**
- Versionamento do modelo (LinearRegression)
- Armazenamento de:
  - métricas (MAE, MSE, RMSE, R²)
  - parâmetros  
  - artefatos  

### **5. Visualização – ThingsBoard/Trendz**
Dashboards exibem:
- Série real de umidade  
- Série prevista pelo modelo  
- Indicadores  
- Comparativos de erro  
- Séries temporais das variáveis de entrada  

### **6. Orquestração – Docker Compose**
Contêineres principais:
- FastAPI  
- MLflow  
- MinIO (opcional)  
- Jupyter Notebook  

---

## Como Executar o Pipeline

### **1. Pré-requisitos**
Antes de tudo, execute:

docker pull ghcr.io/mlflow/mlflow:v3.6.0

E certifique-se de que:

Docker Desktop está aberto

Dependências Python instaladas:

pip install -r requirements.txt

2. Comandos utilizados 

python tratamento_inmet.py
docker compose logs fastapi
docker compose up -d --build
python neonDb_connection.py

3. Endereços dos serviços
Serviço	URL
FastAPI	http://localhost:8000
Swagger	http://localhost:8000/docs
MinIO	http://localhost:9001
MLflow	http://localhost:5000

4. Testando a API (Swagger)
Acesse:
➜ http://localhost:8000/docs

Clique em Try it Out → Execute

No endpoint POST /Ingest-File, envie o arquivo bruto:

INMET_NE_PE_A370_SALGUEIRO_01-01-2024_A_31-12-2024.CSV
Execute e verifique a resposta.

📊 Resultados do Modelo
O modelo usado foi LinearRegression, com as seguintes métricas reais:

MAE: 4.59

MSE: 38.92

RMSE: 6.24

R²: 0.72

Esses valores indicam que a regressão linear capturou 72% da variação da Umidade Relativa na estação de Salgueiro.

Estrutura do projeto 

|–– fastapi/ # API de ingestão
|–– notebooks/
|   |–– analise_dados_do_bd.ipynb
|–– Dados_Processados/
|–– docker-compose.yml
|–– tratamento_inmet.py
|–– neonDb_connection.py

Equipe
Felipe Matias

Felipe França

Gabriel Landim

Lucas Ferreira

Pedro Sampaio

Luis Gustavo

