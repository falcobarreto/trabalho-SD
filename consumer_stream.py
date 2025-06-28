import rabbitmq_stream
import asyncio

# IP local
RABBITMQ_SERVER_IP = "192.168.1.21" # <-- MUDE AQUI para o seu IP ou 'localhost'

async def consumer():
    # Função que será chamada para cada mensagem recebida
    async def message_handler(message: rabbitmq_stream.Message):
        # A mensagem vem com offset, dados, etc. Pegamos o corpo (body).
        print(f" [<-] Recebido: {message.body.decode('utf-8')}")

    # Conecta ao sistema de streams do RabbitMQ
    stream_system = await rabbitmq_stream.connect(
        host=RABBITMQ_SERVER_IP, port=5552, user="guest", password="guest"
    )
    
    # Define de onde o consumidor começará a ler o fluxo.
    # OffsetSpecification.first() -> Começa do início do stream.
    offset = rabbitmq_stream.OffsetSpecification.first()

    print(" [*] Consumidor aguardando mensagens. Para sair, pressione CTRL+C.")
    
    # Cria um consumidor para o stream, definindo o ponto de partida e o handler
    consumer = await stream_system.create_consumer(
        "sensor-data", offset, message_handler
    )

    try:
        # Mantém o script rodando para receber mensagens
        await asyncio.sleep(3600) # Mantém ativo por 1 hora ou até ser interrompido
    except (KeyboardInterrupt, SystemExit):
        print(" [!] Consumidor encerrado.")
    finally:
        # Fecha o consumidor e a conexão
        await consumer.close()
        await stream_system.close()


if __name__ == "__main__":
    asyncio.run(consumer())