from grupo_rabbitmq import *
from privado_rabbitmq import *
from __init__ import *

def opcoes():
    print(f'Olá, {usuario}!')
    print('''Opções que estão disponíveis no chat:
    1. Mensagem privada ou
    2. Mensagem em grupo.
    apenas digite a opção, ex.: 1''')
    opcao = input('Você deseja usar qual opção de chat? ')
    
    if opcao == '1':
        privado_funcao()
    elif opcao == '2':
        grupo_funcao()
    else:
        print('\nVocê digitou um valor que não é uma opção.')
        print('Tente novamente.\n')
        opcoes()
opcoes()