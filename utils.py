import os
import re

# Método para extrair endereço IP válido


def extract_ip(string):
    # Regex para extrair o IP
    pattern_1 = r"\s*(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s*"
    pattern_2 = r"\s*(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):(\d+)\s*"

    # Extrai o IP usando a regex do pattern
    match_1 = re.match(pattern_2, string)
    match_2 = re.match(pattern_1, string)

    # Lógica para devolver endereço IP válido
    if match_1:
        ip = str(match_1.group(1))
        return ip
    elif match_2:
        ip = str(match_2.group(1))
        return ip
    else:
        raise Exception(f"[ERRO] Formato de endereço IP inválido.")

# Método para extrair endereço porta válido


def extract_port(string):
    # Regex para extrair o Porta
    pattern_1 = r"\s*(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):(\d+)\s*"
    pattern_2 = r"\s*(\d+)\s*"

    # Extrai o porta usando a regex do pattern
    match_1 = re.match(pattern_1, string)
    match_2 = re.match(pattern_2, string)

    # Lógica para devolver endereço porta válido
    if match_1:
        port_int = int(match_1.group(2))
        return port_int
    elif match_2:
        port_int = int(match_2.group(1))
        return port_int
    else:
        raise Exception(f"[ERRO] Formato de endereço porta inválido.")

# Método para capturar endereço IP válido


def get_ip(class_type):
    # Captura do IP
    ip = input(f"Informe o IP do {class_type} (default: 127.0.0.1): ")
    if not ip:
        ip = "127.0.0.1"
    ip = extract_ip(ip)
    # Exibe endereço IP recebido por input
    print(f"Endereço IP do {class_type} capturado: {ip}.")
    return ip

# Método para capturar endereço de porta válido


def get_port(class_type):

    class_type = class_type.lower()

    if (class_type == 'servidor' or class_type == 'server'):
        port = input(f"Informe a porta do {class_type} (default: 1099): ")
        if not port:
            port = "1099"
        port = extract_port(port)
        # Exibe endereço porta recebido por input
        print(f"Endereço de porta do {class_type} capturado: {port}.")
        return port

    elif (class_type == 'peer' or class_type == 'client' or class_type == 'cliente'):
        port = input(f"Informe a porta do {class_type} (default: 1100): ")
        if not port:
            port = "1100"
        port = extract_port(port)
        # Exibe endereço porta recebido por input
        print(f"Endereço de porta do {class_type} capturado: {port}.")
        return port

    else:
        # Exibe endereço porta recebido por input
        print(f"Class type: {class_type} não foi identificado.")

# Método para capturar caminho de arquivo válido


def get_filepath(file_path):
    while True:
        print("Digite o caminho do arquivo, ou 0 para sair.")
        path = input("Caminho do arquivo (default: peer folder): ")
        if not path:
            path = file_path
        if os.path.exists(path):
            print(f"O caminho '{path}' existe.")
            return path
        elif path == "0":
            break
        else:
            print("Caminho inválido. Por favor, tente novamente.")

# Método para capturar nome de arquivo


def get_filename():
    while True:
        print("Digite o nome do arquivo, ou 0 para sair.")
        filename = input("Nome do arquivo (default: 'README.md'): ")
        if not filename:
            filename = 'README.md'
        return filename


# Método para obter nomes dos arquivos em uma pasta
def get_file_names(folder):
    # Verifica se o caminho é uma pasta válida
    if not os.path.isdir(folder):
        raise ValueError("O caminho fornecido não é uma pasta válida.")

    # Obtém os nomes dos arquivos na pasta
    file_names = []
    for file_name in os.listdir(folder):
        file_path = os.path.join(folder, file_name)
        if os.path.isfile(file_path):
            file_names.append(file_name)

    return file_names

# Método para capturar entradas do peer


def interactive_menu(peer):
    # Peer Info
    my_ip = peer.ip
    my_port = peer.port
    my_server_uri = peer.server_uri
    my_folder = peer.folder

    # Peer Info
    print(f'INFO ABOUT ME: ')
    print(
        f"IP: {my_ip}, PORT: {my_port}, SERVER_URI: {my_server_uri},  FOLDER: {my_folder}")
    print("")

    # Menu
    while True:
        # Opções
        print("")
        print("############################")
        print("")
        print("Selecione uma opção:")
        print("1. JOIN")
        print("2. SEARCH")
        print("3. DOWNLOAD")
        print("0. Sair")
        print("")
        print("############################")
        print("")

        option = input("Opção: ")

        # JOIN
        if option == "1":
            peer_folder = get_filepath(my_folder)
            if peer_folder:
                peer.join(my_folder)
        # SEARCH
        elif option == "2":
            filename = get_filename()
            if filename:
                peer.search(filename)
        # DOWNLOAD
        elif option == "3":
            ip = get_ip('peer')
            port = get_port('peer')
            filename = get_filename()
            if filename:
                peer.download(ip, port, filename)
        # SAIR
        elif option == "0":
            print("Saindo do programa...")
            break
        # ERRO
        else:
            print("Opção inválida. Tente novamente.")
