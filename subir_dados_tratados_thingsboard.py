import csv
import json
import requests
from datetime import datetime

THINGSBOARD_URL = "http://localhost:8080/api/v1"
TOKEN = "T1_TEST_TOKEN"  
CSV_PATH = "data/dados_tratados.csv"  


def enviar_csv_para_thingsboard():
    url = f"{THINGSBOARD_URL}/{TOKEN}/telemetry"

    with open(CSV_PATH, newline='', encoding='utf-8') as csvfile:
        leitor = csv.DictReader(csvfile)

        for linha in leitor:
            
            dt_str = linha["data_hora_utc"]  
            dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
            timestamp_ms = int(dt.timestamp() * 1000)

            payload = {
                "ts": timestamp_ms,
                "values": {
                    "temperatura_c": float(linha["temperatura_c"]),
                    "pressao_mb": float(linha["pressao_mb"]),
                    "radiacao_kj_m2": float(linha["radiacao_kj_m2"]),
                    "umidade_relativa_pct": float(linha["umidade_relativa_pct"])
                }
            }

            

            resposta = requests.post(
                url,
                data=json.dumps(payload),
                headers={"Content-Type": "application/json"}
            )

            



enviar_csv_para_thingsboard()