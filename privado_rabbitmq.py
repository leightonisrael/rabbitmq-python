def privado_funcao():
    import pika
    import threading
    from __init__ import  usuario

    # Conexão com o RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Criação da exchange
    channel.exchange_declare(exchange='private_chat_exchange', exchange_type='direct')

    # Função para criar uma conversa privada
    def create_private_chat(user1, user2):
        # Criação da queue para o usuário 1
        result1 = channel.queue_declare(queue='', exclusive=True)
        queue1_name = result1.method.queue
        channel.queue_bind(exchange='private_chat_exchange', queue=queue1_name, routing_key=user1)

        # Criação da queue para o usuário 2
        result2 = channel.queue_declare(queue='', exclusive=True)
        queue2_name = result2.method.queue
        channel.queue_bind(exchange='private_chat_exchange', queue=queue2_name, routing_key=user2)

        return queue1_name, queue2_name

    # Função para enviar mensagens
    def send_message(sender, recipient, message):
        channel.basic_publish(exchange='private_chat_exchange', routing_key=recipient, body=f'{sender}: {message}')

    # Função para receber mensagens
    def receive_message(ch, method, properties, body):
        print(body.decode())

    # Função para iniciar o chat
    def start_chat():
        print('\nBem vindo ao chat privado.\n')
        user1 = usuario
        user2 = input("Digite o nome da pessoa que você deseja iniciar o chat privado: ")

        # Criação da conversa privada
        queue1_name, queue2_name = create_private_chat(user1, user2)

        # Iniciar a escuta de mensagens na queue do usuário 1
        channel.basic_consume(queue=queue1_name, on_message_callback=receive_message, auto_ack=True)

        # Thread para receber mensagens
        def receive_messages():
            channel.start_consuming()

        # Iniciar thread para receber mensagens
        receive_thread = threading.Thread(target=receive_messages)
        receive_thread.start()

        # Aviso de chat privado iniciado
        print(f'Chat privado iniciado com {user2}')

        # Loop para enviar mensagens
        while True:
            message = input("")
            if message == 'sair':
                break
            send_message(user1, user2, message)

        # Parar de receber mensagens e fechar a conexão com o RabbitMQ
        channel.stop_consuming()
        connection.close()

    # Iniciar o chat
    start_chat()
