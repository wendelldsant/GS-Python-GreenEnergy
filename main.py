import re

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

def require_password() -> str:
    while True:
        password = input('Senha: ')
        if has_special_char(password) and has_upper_lower(password) and has_number(password):
            return password
        print(f'Sua senha deve ter ao menos 1 letra maiuscula, 1 letra minuscula, 1 caracter especial e 1 numero\n'
        f'Senha não aceita. Verifique os requisitos e tente novamente.')

def require_username(users_list: list) -> str:
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

def newUser(users_list):
    while True:
        username = require_username(users_list)
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
                    users_list.append(newUser)
                    return newUser
                else:
                    break
            else:
                break
        else:
            break
    return False

def login(users_list):
    retry = True
    while retry:
        username = input('Digite seu nome: ')
        password = input('Digite sua senha: ')
        for user in users_list:
            if user['username'] == username:
                if user['password'] == password:
                    print('Login feito com sucesso!')
                    return user
        print('Usuário não encontrado')
    retry = try_again()
    return False

users_list = []

def require_device_id(devices_list):
    retry = True
    while retry:
        device_id = get_number('Digite o ID do seu Sun Tracker: ')
        if str(device_id) in devices_list:
            return device_id
        print('Dispositivo não encontrado em nosso sistema. Tente novamente')
        retry = try_again()

def add_device(user, devices_list):
    retry = True
    while retry:
        device_id = require_device_id(devices_list)
        if device_id:
            device_nickname = input('Digite um apelido para seu dispositivo: ')
            if device_nickname:
                new_device = {
                    "id": device_id,
                    "nickname": device_nickname,
                    "dados": []
                }
                user['devices'].append(new_device)
                print('Dispositivo cadastrado com sucesso!')
                return True
            else:
                print('Nome do dispositivo não pode ser vazio.')
        else:
            print('Dispositivo não cadastrado.')
        retry = try_again()

        

def show_profile(user, all_devices_list):
    username = user['username']
    password = user['password']
    dispositivos = user['devices']
    while True:
        menu = require_valid_option(f'O que você deseja visualizar {username}?', ('Meus dispositivos', 'Cadastrar dispositivo', 'Dados Cadastrais', 'Voltar'))
        match menu:
            case 1:
                while True:
                    if len(dispositivos) > 0:
                        devices_nicknames = [dispositivo['nickname'] for dispositivo in dispositivos]
                        device_choice = require_valid_option('Visualize dados do seu dispositivo', [devices_nicknames, 'Voltar'])
                        if device_choice == len(dispositivos)+1:  #opcao voltar
                            break
                        device_index = device_choice-1 #para pegar o indice correto do dispositivo
                        device = user['devices'][device_index]
                        while True:
                            print(f"ID: {device['id']}\n"
                                f"Apelido: {device['nickname']}\n"
                                f"Dados: {device['dados']}\n")
                            choice = require_valid_option(f'O que você deseja fazer?', ('Atualizar', 'Voltar'))
                            if choice == 2:
                                break                
                    else:
                        print('Não há dispositivos cadastrados.')
                        break
            case 2:
                register = add_device(user, all_devices_list)
            case 3:
                print(f'Meus Dados\n'
                    f'Username: {user['username']}\n'
                    f'Password: {user['password']}\n'
                )
            case 4:
                break


def interface(users_list, system_devices_list):

    while True:
        nav_choice = require_valid_option('Plataforma de Monitoramento Sun Catcher', ['Home', 'Cadastre-se', 'Login'])
        match nav_choice:
            case 1:
                login_check = False
                print('Home')
            case 2:
                login_check = newUser(users_list)
            case 3:
                login_check = login(users_list)
        if login_check:
            while True:
                nav_choice = require_valid_option('Plataforma de Monitoramento Sun Catcher', ['Home','Profile','Logout'])
                match nav_choice:
                    case 1:
                        print('Home')
                    case 2:
                        show_profile(login_check, system_devices_list)
                    case 3:
                        login_check = False
                        print('Logout feito com sucesso!')
                        break
users_list = []
system_devices_list = ['1234', '4531']

while True:
    interface(users_list, system_devices_list)

    

    