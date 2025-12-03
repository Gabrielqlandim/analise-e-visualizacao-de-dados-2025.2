import pandas as pd
import requests
from datetime import datetime
import numpy as np

def send_inmet_csv_to_thingsboard(csv_path: str, thingsboard_url: str, token: str):
    """
    Lê um CSV do INMET e envia cada linha como telemetria para o ThingsBoard,
    seguindo o mesmo padrão do arquivo do seu amigo.
    """

    #Encontrar automaticamente a linha do cabeçalho ("Data;")
    with open(csv_path, "r", encoding="latin1") as f:
        lines = f.readlines()

    header_row = None
    for i, line in enumerate(lines):
        if line.startswith("Data;"):
            header_row = i
            break

    if header_row is None:
        raise ValueError("Não encontrei linha de cabeçalho começando com 'Data;'")

    #Ler o CSV com pandas
    df = pd.read_csv(
        csv_path,
        sep=";",
        header=header_row,
        encoding="latin1"
    )

    #Formatação dos dados
    def sanitize_col(col: str) -> str:
        return (
            col.strip()
            .lower()
            .replace(" ", "_")
            .replace("(", "")
            .replace(")", "")
            .replace("/", "_")
            .replace("%", "pct")
            .replace("º", "")
            .replace("°", "")
        )

    df = df.rename(columns={c: sanitize_col(c) for c in df.columns})

    # remove linhas completamente vazias
    df = df.dropna(how="all")

    #Enviar cada linha como telemetria
    tb_url = f"{thingsboard_url}/api/v1/{token}/telemetry"
    enviados = 0

    for _, row in df.iterrows():

        row_dict = row.to_dict()
        payload = {
            "ts": 0,
            "values": {}
        }

        data_csv = None

        #montar payload
        for k, v in row_dict.items():

            # limpar NaN
            if pd.isna(v):
                v = None

            #detectar a coluna de data
            if k == "data":
                data_csv = v

            #montar timestamp quando chegar na hora_utc
            elif k == "hora_utc" and data_csv is not None:
                #data: "2024/01/01"
                #hora_utc: "0000 UTC"
                #criar "2024/01/01 00:00"

                hora_str = str(v).replace(" UTC", "")
                data_hora = f"{data_csv} {hora_str}"

                #parse no formato correto
                dt = datetime.strptime(data_hora, "%Y/%m/%d %H%M")
                timestamp = int(dt.timestamp() * 1000)

                payload["ts"] = timestamp

            #demais colunas vão para values
            else:
                #trocar vírgula decimal
                if isinstance(v, str) and "," in v:
                    v = v.replace(",", ".")
                    try:
                        v = float(v)
                    except:
                        pass

                payload["values"][k] = v

        # Enviar para ThingsBoard
        r = requests.post(tb_url, json=payload)
        if r.status_code != 200:
            print("ERRO:", r.status_code, r.text)

        enviados += 1

    return {
        "status": "ok",
        "linhas_enviadas": enviados,
        "arquivo": csv_path,
    }

print(send_inmet_csv_to_thingsboard("data\INMET_NE_PE_A370_SALGUEIRO_01-01-2024_A_31-12-2024.CSV", "http://localhost:8080/", "T2_TEST_TOKEN"))