# rabbitmq-python
Chat com RabbitMQ

Para que funcione todas as aplicações com python, certifique-se que todos os dados estão corretos.

Instale a biblioteca "pika", "threading", "requests" e "time" 

Ter uma instalação padrão do RabbitMQ, como por exemplo um docker:
 docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.11-management

Execute primeiro o script: users_control.py e depois o main.py
