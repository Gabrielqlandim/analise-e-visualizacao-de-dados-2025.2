import psycopg2
import requests
import json

def enviar_telemetria(token):
    conn = psycopg2.connect(
        "postgresql://neondb_owner:npg_ZyDj34mdtqLu@"
        "ep-crimson-glitter-ac9d92fb-pooler.sa-east-1.aws.neon.tech/"
        "neondb?sslmode=require&channel_binding=require"
    )


    cursor = conn.cursor()


    cursor.execute("SELECT * FROM metrics;")
    registros = cursor.fetchall()

    
    colunas = [desc[0] for desc in cursor.description]

    url = f"http://localhost:8080/api/v1/{token}/telemetry"

    for row in registros:
        payload = dict(zip(colunas, row))

        try:
            resposta = requests.post(
                url,
                data=json.dumps(payload),
                headers={"Content-Type": "application/json"}
            )

            print("Status:", resposta.status_code)
            print("Retorno:", resposta.text)

        except Exception as e:
            print("Erro ao enviar linha:", e)

    cursor.close()
    conn.close()

token = "RmwpoMSt7SSKzBRej1hA"
enviar_telemetria(token)