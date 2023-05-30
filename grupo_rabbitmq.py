import pika
import threading
from __init__ import usuario
import requests as client
import time 

URL_DEFAULT = "http://127.0.0.1:5000/users"

def grupo_funcao():


    # Conectando ao RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Pedindo o nome do usuário
    name = usuario

    # Boas vindas ao chat em grupo
    print('\nBem-vindo ao chat em grupo.\n')

    # Pedindo o nome do canal
    channel_name = input('''Digite o nome do canal que deseja entrar 
ou 
Digite o nome do canal que deseja criar e aguardar à entrada de alguém: ''')


    # Criando a exchange e a fila para o canal
    channel.exchange_declare(exchange=channel_name, exchange_type='fanout')
    result = channel.queue_declare('', exclusive=True)
    queue_name = result.method.queue
    channel.queue_bind(exchange=channel_name, queue=queue_name)

    client.post(url=URL_DEFAULT, data=channel_name)

    users_size = client.get(URL_DEFAULT + "?chat=" + channel_name).text
    users_size = int(users_size)
    print("Verificando se existem membros suficientes para iniciar o chat...")

    while users_size < 3:
        time.sleep(2)
        users_size = client.get(URL_DEFAULT  + "?chat=" + channel_name).text
        users_size = int(users_size)
    

    # Função para enviar mensagens
    def send_message():
        while True:
            message = input()
            channel.basic_publish(exchange=channel_name, routing_key='', body=f'{name}: {message}')

    # Função para receber mensagens
    def receive_message(ch, method, properties, body):
        received_message = body.decode()
        sender_name, message = received_message.split(": ", 1)
        if sender_name != name:
            print(received_message)

    # Iniciando thread para enviar mensagens
    thread = threading.Thread(target=send_message)
    thread.start()

    print(f'Chat em grupo iniciado no grupo {channel_name}.')

    # Consumindo mensagens da fila
    channel.basic_consume(queue=queue_name, on_message_callback=receive_message, auto_ack=True)
    channel.start_consuming()