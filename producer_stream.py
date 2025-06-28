import rabbitmq_stream
import asyncio
import time
import random

# IP local
RABBITMQ_SERVER_IP = "192.168.1.21" # <-- MUDE AQUI para o seu IP ou 'localhost'

async def producer():
    # Conecta ao sistema de streams do RabbitMQ
    stream_system = await rabbitmq_stream.connect(
        host=RABBITMQ_SERVER_IP, port=5552, user="guest", password="guest"
    )

    # Cria o stream (se não existir)
    await stream_system.create_stream("sensor-data")

    # Cria um produtor para o stream específico
    producer = await stream_system.create_producer("sensor-data")

    print(" [x] Produtor iniciado. Enviando leituras de sensor...")
    message_id = 1
    while True:
        try:
            temp = round(random.uniform(15.0, 30.0), 2)
            message_body = f"id:{message_id},sensor:temp01,value:{temp}°C"
            
            # Converte a mensagem para bytes e a envia
            message = message_body.encode('utf-8')
            await producer.send(message)
            
            print(f" [->] Enviado: {message_body}")
            
            message_id += 1
            time.sleep(1) # Aguarda 1 segundo
        except (KeyboardInterrupt, SystemExit):
            print(" [!] Produtor encerrado.")
            break
        except Exception as e:
            print(f"Erro: {e}")
            break

    # Fecha o produtor e a conexão
    await producer.close()
    await stream_system.close()


if __name__ == "__main__":
    asyncio.run(producer())