from pymongo import MongoClient
from random import randint
import os

import re

def connect_to_mongo():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["SunCatcher"]  # Nome do banco
    return db

def get_number(prompt_text) -> int:
    choice = input(prompt_text)
    while True:
        try:
            return int(choice)
        except ValueError as e:
            choice = input('Entrada inválida. Digite um número: ')

def require_valid_option(prompt_text: str, lista_opcoes: tuple) -> int:
    while True:
        print(f'\n{prompt_text}')
        for i in range(len(lista_opcoes)):
            print(f"({i+1}){lista_opcoes[i]}")
        choice = get_number('Digite a opção escolhida: ')
        if choice in range(1, len(lista_opcoes)+1):
            return choice
        print('Opção inválida. Digite uma das opções listadas: ')

def try_again():
    choice = require_valid_option('Você deseja tentar novamente?', ('Sim', 'Não'))
    return bool(choice == 1)

def has_special_char(word: str) -> bool:
    return bool(re.search(r'[^a-zA-Z0-9_]', word))

def has_upper_lower(word: str) -> bool:
    has_upper = False
    has_lower = False
    for char in word:
        if char.isupper():
            has_upper = True
        elif char.islower():
            has_lower = True
    return bool(has_upper and has_lower)

def has_number(word: str) -> bool:
    for char in word:
        if char.isdigit():
            return True
    return False

def require_password():
    while True:
        password = input('Senha: ')
        if has_special_char(password) and has_upper_lower(password) and has_number(password):
            return password
        print(f'Sua senha deve ter ao menos 1 letra maiuscula, 1 letra minuscula, 1 caracter especial e 1 numero\n'
        f'Senha não aceita. Verifique os requisitos e tente novamente.')

def require_username(users_list):
    min_char_size = 7
    retry = True
    while retry:
        username = input('Nome de Usuário: ')
        if len(username) < min_char_size:
            print(f"Nome de usuário precisa ter pelo menos {min_char_size} caracteres.")
        elif ' ' in username:
            print("O nome de usuário não pode conter espaços.")
        elif any(user['username'] == username for user in users_list):
            print('Username já em uso. Tente novamente')
        else:
            return username
        retry = try_again()

def newUser(users_collection):
    while True:
        username = require_username(list(users_collection.find()))
        if username:
            password = require_password()
            if password:
                newUser = {
                    "username": username,
                    "password": password,
                    "devices": []
                }
                register_choice = require_valid_option('Escolha uma opção: ', ('Registrar', 'Sair'))
                if register_choice == 1:
                    users_collection.insert_one(newUser)
                    print('Cadastro Feito com Sucesso!')
                    return newUser
                else:
                    break
            else:
                break
        else:
            break
    return False

def login(users_collection):
    retry = True
    while retry:
        username = input('Digite seu nome: ')
        password = input('Digite sua senha: ')
        user = users_collection.find_one({"username": username, "password": password})
        if user:
            print('Login feito com sucesso!')
            return user
        print('Usuário não encontrado')
        retry = try_again()
    return False

def require_device_id(devices_list):
    retry = True
    while retry:
        device_id = get_number('Digite o ID do seu Sun Tracker: ')
        if any(device['id'] == str(device_id) for device in devices_list):
            return device_id
        print('Dispositivo não encontrado em nosso sistema. Tente novamente')
        retry = try_again()

def add_device(user, devices_collection, users_collection):
    retry = True
    while retry:
        device_id = require_device_id(list(devices_collection.find()))
        if device_id:
            device_nickname = input('Digite um apelido para seu dispositivo: ')
            if device_nickname:
                new_device = {
                    "id": device_id,
                    "nickname": device_nickname,
                    "dados": {}
                }
                user["devices"].append(new_device)
                users_collection.update_one(
                    {"_id": user["_id"]},
                    {"$set": {"devices": user["devices"]}}
                )
                input('Dispositivo cadastrado com sucesso! Pressione Enter para continuar...')
                return True
            else:
                print('Nome do dispositivo não pode ser vazio.')
        else:
            input('Dispositivo não cadastrado. Pressione Enter para continuar...')
        retry = try_again()

def generate_fake_data():
    data = {
        "sensores": {
            "superior_esquerdo": randint(0, 1000),
            "superior_direito": randint(0, 1000),
            "inferior_esquerdo": randint(0, 1000),
            "inferior_direito": randint(0, 1000)
        },
        "angulos": {
            "horizontal": randint(0, 180),
            "vertical": randint(0, 180)
        }
    }
    return data


def show_profile(user, all_devices_list, users_collection):
    while True:
        clear()
        menu = require_valid_option(f'O que você deseja visualizar {user["username"]}?', ('Meus dispositivos', 'Cadastrar dispositivo', 'Dados Cadastrais', 'Voltar'))
        match menu:
            case 1:
                while True:
                    clear()
                    if len(user['devices']) > 0:
                        devices_nicknames = [dispositivo['nickname'] for dispositivo in user['devices']]
                        device_choice = require_valid_option('Visualize dados do seu dispositivo', devices_nicknames + ['Voltar'])
                        if device_choice == len(user['devices'])+1:  #opcao voltar
                            break
                        device_index = device_choice-1 #para pegar o indice correto do dispositivo
                        device = user['devices'][device_index]
                        print(f"\nREGISTRO DO MEU DISPOSITIVO\n"
                            f"ID: {device['id']}\n"
                            f"Apelido: {device['nickname']}")
                        while True:
                            action = require_valid_option('O que deseja fazer?', ('Visualizar Dados (atualizados)', 'Voltar'))
                            if action == 1:
                                fake_data = generate_fake_data()
                                device['dados'] = fake_data
                                users_collection.update_one(
                                    {"_id": user["_id"]},
                                    {"$set": {"devices": user['devices']}}
                                )
                                input(f"\nDADOS DO MEU RASTREADOR\n"
                                      f"Sensor LDR Superior Esquerdo: {fake_data['sensores']['superior_esquerdo']}\n\n"
                                      f"Sensor LDR Superior Direito: {fake_data['sensores']['superior_direito']}\n\n"
                                      f"Sensor LDR Inferior Esquerdo: {fake_data['sensores']['inferior_esquerdo']}\n\n"
                                      f"Sensor LDR Inferior Direito: {fake_data['sensores']['inferior_direito']}\n\n"
                                      f"Ângulo Servo Motor Horizontal: {fake_data['angulos']['horizontal']}\n\n"
                                      f"Ângulo Servo Motor Vertical: {fake_data['angulos']['vertical']}\n"
                                      f"Pressione Enter para continuar...")
                            else:
                                break             
                    else:
                        input('Não há dispositivos cadastrados. Pressione Enter para continuar')
                        break
            case 2:
                register = add_device(user, all_devices_list, users_collection)
            case 3:
                clear()
                while True:
                    print(f'MEUS DADOS\n'
                    f'Username: {user["username"]}\n'
                    f'Password: {user["password"]}\n'
                    )
                    edit = require_valid_option(f'O que você deseja fazer?', ('Excluir conta', 'Editar Nome', 'Editar senha', 'Voltar'))
                    match edit:
                        case 1:
                            remove_user = users_collection.delete_one({"username": user["username"], "password": user["password"]})
                            if remove_user.deleted_count > 0:
                                input("Conta excluída com sucesso. Pressione enter para continuar...")
                                return False # Sai da função
                            else:
                                print("Falha ao excluir conta. Tente novamente.")
                        case 2:
                            print('Digite seu novo nome de usuário\n')
                            new_username = require_username(list(users_collection.find()))
                            if new_username:
                                try:
                                    edit_username = users_collection.update_one({"_id": user["_id"]}, {"$set": {"username": new_username}})
                                    user["username"] = new_username
                                    print('Username alterado com sucesso!')
                                except Exception as e:
                                    print('Falha ao editar username. Tente novamente.')
                        case 3:
                            print('Digite sua nova senha\n')
                            new_password = require_password()
                            if new_password:
                                try:
                                    edit_password = users_collection.update_one({"_id": user["_id"]}, {"$set": {"password": new_password}})
                                    user["password"] = new_password
                                    print('Senha alterada com sucesso!')
                                except Exception as e:
                                    print('Falha ao editar senha. Tente novamente.')
                        case 4:
                            break
            case 4:
                break

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def interface(users_collection, system_devices_list):
    home_text = f"""Bem-vindo(a) ao Sun Catcher! ☀️
                    O Sun Catcher é uma plataforma de monitoramento inteligente para dispositivos de rastreamento solar. 
                    Aqui, você pode:

                    Cadastrar e gerenciar seus dispositivos solares.
                    Monitorar dados em tempo real, como sensores e ângulos de captação.
                    Garantir a eficiência e o melhor aproveitamento da energia renovável.
                   💡 Dica: Faça login ou cadastre-se para acessar todas as funcionalidades da plataforma e acompanhar o desempenho do seu sistema solar.

                   🌍 Juntos por um futuro sustentável!
                """
    while True:
        clear()
        print(home_text)
        nav_choice = require_valid_option('Plataforma de Monitoramento Sun Catcher', ['Home', 'Cadastre-se', 'Login'])
        match nav_choice:
            case 1:
                login_check = False
                print(home_text)
            case 2:
                try:
                    clear()
                    print('CADASTRO DE USUÁRIO')
                    login_check = newUser(users_collection)
                except Exception as e:
                    print(f"Erro ao cadastrar usuário: {e}")
            case 3:
                try:
                    clear()
                    print('ÁREA DE LOGIN')
                    login_check = login(users_collection)
                except Exception as e:
                    print('Erro ao entrar na conta. Tente novamente.')
        if login_check:
            while True:
                nav_choice = require_valid_option('Plataforma de Monitoramento Sun Catcher', ['Home','Profile','Logout'])
                match nav_choice:
                    case 1:
                        clear()
                        print(home_text)
                    case 2:
                        profile = show_profile(login_check, system_devices_list, users_collection)
                        if not profile:
                            break
                    case 3:
                        login_check = False
                        input('Logout feito com sucesso! Pressione Enter para voltar ao Menu Principal...')
                        break



if __name__ == "__main__":
    db = connect_to_mongo()
    users_collection = db["users"]
    devices_collection = db["devices"]

    # Dados iniciais de dispositivos, para simulação
    if devices_collection.count_documents({}) == 0:
        devices_collection.insert_many([
            {"id": "1234"},
            {"id": "6969"},
            {"id": "5151"},
            {"id": "2424"}
        ])

    interface(users_collection, devices_collection)

    

    