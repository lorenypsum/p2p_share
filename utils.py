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
def get_filepath():   
    while True:
        print("Digite o caminho do arquivo, ou 0 para sair.")
        path = input("Caminho do arquivo: ")
        if os.path.exists(path):
            print(f"O caminho '{path}' existe.")
            return path
        elif path == "0":
            break
        else:
            print("Caminho inválido. Por favor, tente novamente.")

# Método para capturar nome de arquivo
def get_filename():   
        filename = input("Digite o nome do arquivo: ")
        return filename

# Método para capturar entradas do peer
def interactive_menu(peer):
    # Peer Info
    peer_ip = peer.ip
    peer_port = peer.port
    peer_server_uri = peer.server_uri
    peer_folder = peer.folder

    # Menu
    while True:
        # Peer Info
        print( f'INFO PEER ATUAL: ')
        print(f"IP: {peer_ip}, PORT: {peer_port}, SERVER_URI: {peer_server_uri},  FOLDER: {peer_folder}")
        # Opções
        print("############################")
        print("")
        print("Selecione uma opção:")
        print("1. JOIN")
        print("2. SEARCH")
        print("3. DOWNLOAD")
        print("0. Sair")
        print("")
        print("############################")

        option = input("Opção: ")

        # JOIN
        if option == "1":
            folder = get_filepath()
            peer.join(folder)
        # SEARCH
        elif option == "2":
            filename = get_filename()
            peer.join(filename)
        # DOWNLOAD
        elif option == "3":
            ip = get_ip('peer')
            port = get_port('peer')
            filename = get_filename()
            peer.download(ip, port, filename)
        # SAIR
        elif option == "0":
            print("Saindo do programa...")
            break
        # ERRO        
        else:
            print("Opção inválida. Tente novamente.")