import asyncio
from rstream.producer import Producer
import time
import random

# IP local
RABBITMQ_SERVER_IP = "localhost"

async def main():
    producer = Producer(
        host=RABBITMQ_SERVER_IP,
        port=5552,
        username='usuario_rabbitmq',     
        password='senha_rabbitmq'  
    )

    async with producer:
        try:
            await producer.create_stream('sensor-data')
            print(" [i] Stream 'sensor-data' criado.")
        except Exception as e:
            if "StreamAlreadyExists" in str(e):
                 print(" [i] Stream 'sensor-data' já existe. Continuando.")
                 pass
            else:
                raise e

        print(" [x] Produtor conectado. Enviando leituras de sensor...")
        message_id = 1
        while True:
            temp = round(random.uniform(15.0, 30.0), 2)
            message_body = f"id:{message_id},sensor:temp01,value:{temp}°C"
            message = message_body.encode('utf-8')
            
            await producer.send('sensor-data', message)
            # --------------------

            print(f" [->] Enviado: {message_body}")
            message_id += 1
            await asyncio.sleep(1)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n [!] Programa interrompido pelo usuário.")
    except Exception as e:
        print(f"\n [!] Ocorreu um erro: {e}")
