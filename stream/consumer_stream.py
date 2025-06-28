import asyncio
from rstream.consumer import Consumer
import rstream.exceptions

# IP local
RABBITMQ_SERVER_IP = "localhost" 

async def message_handler(message, context):
    print(f" [<-] RECEBIDO: offset={context.offset}, body='{message.decode('utf-8')}'")

async def main():
    consumer = Consumer(
        host=RABBITMQ_SERVER_IP,
        port=5552,
        username='usuario_rabbitmq',     
        password='senha_rabbitmq'  
    )

    try:
        async with consumer:
            try:
                await consumer.create_stream('sensor-data')
                print(" [i] Stream 'sensor-data' criado pelo consumidor.")
            except rstream.exceptions.StreamAlreadyExists:
                print(" [i] Stream 'sensor-data' já existe. Conectando...")
                pass

            await consumer.subscribe(
                'sensor-data',
                message_handler
            )
            # -------------------------

            print("\n [*] CONSUMIDOR FUNCIONANDO! Aguardando mensagens... (Pressione CTRL+C para sair)")
            await asyncio.Event().wait()

    except asyncio.CancelledError:
        print("\n [!] Consumidor encerrado.")
    except Exception as e:
        print(f"\n [!] Ocorreu um erro: {e}")

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n [!] Programa interrompido pelo usuário.")
