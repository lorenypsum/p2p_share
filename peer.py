import socket
import threading
import Pyro4
import os
import re

from utils import input_ip, input_port

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

# Inicialização do peer
def start_peer():

    # Exibe a mensagem
    print("Inicializando peer.")

    # Armazena endereço de IP do peer
    peer_ip = input_ip()

    # Armazena endereço de porta do peer
    peer_port = input_port()

    # Armazena server_uri
    server_uri = input(f"Digite a uri do peer: (default: PYRO:server@127.0.0.1:1099): ")
    if not server_uri:
        server_uri = "PYRO:server@127.0.0.1:1099"

    # Captura as informações de pasta do peer
    peer_folder = input("Digite a pasta do peer: (default: .)")
    if not peer_folder:
        peer_folder = "."
    
    # Inicializa peer
    peer = Peer(ip = peer_ip, server_uri = server_uri, port = peer_port, folder = peer_folder)  
    return peer

# Classe do Cliente (Peers)
class Peer:
    
    # Inicializa as informações o peer
    def __init__(self, server_uri, ip, port, folder):
        self.server_uri = server_uri
        self.ip = ip
        self.port = port
        self.folder = folder
        self.proxy = Pyro4.Proxy(server_uri)
        self.server_socket = socket.create_server((self.ip, self.port), family=socket.AF_INET)
        threading.Thread(target=self.listen_for_download_requests, daemon=True).start()


    # Método para enviar requisição de JOIN ao servidor
    def join(self, folder):
        # Armazena nomes dos arquivos
        files = get_file_names(folder)

        # Lógica para conectar peer ao servidor
        try:
            # Acessa servidor por proxy
            response = self.proxy.join({"ip": self.ip, "port": self.port,"files": files})
            if response == "JOIN_OK":
                # Exibe mensagem no console do cliente (peer)
                print(f"Sou peer {self.ip}:{self.port} com arquivos {' '.join(files)}.")
            else:
                # Exibe mensagem no console do cliente (peer)
                print(f"Resposta inesperada (join_server): {response}.")
        except Exception as e:
            # Exibe mensagem no console do cliente (peer)
            print(f"Ocorreu uma exceção (join_server): {e}")
            
    # Método para enviar requisição de UPDATE ao servidor
    def update(self, filename):

        # Lógica para conectar peer ao servidor
        try:
            # Acessa servidor por proxy
            response = self.proxy.update({"ip": self.ip, "port": self.port}, filename)
            # Lógica
            if response == "UPDATE_OK":
                # Exibe mensagem no console do cliente (peer)
                # print(f"Sou peer {self.ip}:{self.port} realizou o download do arquivo {filename}.")
                pass
            else:
                # Exibe mensagem no console do cliente (peer)
                print(f"Resposta inesperada (update_server): {response}.")
        except Exception as e:
            # Exibe mensagem no console do cliente (peer)
            print(f"Ocorreu uma exceção (update_server): {e}")
    
    # Método para enviar requisição de SEARCH ao servidor
    def search(self, filename):
        # Lógica para conectar peer ao servidor
        try:
            # Acessa servidor por proxy
            response = self.proxy.search({"ip": self.ip, "port": self.port}, filename)
            # Exibe mensagem no console do cliente (peer)
            print(f"Peers com arquivo solicitado: {' '.join(response)}.")
        except Exception as e:
            # Exibe mensagem no console do cliente (peer)
            print(f"Ocorreu uma exceção (search_server): {e}.")
    
    # Método para enviar requisição de DOWNLOAD por TCP a outro peer
    def download(self, peer_ip, peer_port, filename):
        # Conecta-se ao peer utilizando sockets TCP
        sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        sock.connect((peer_ip, peer_port))

        # Envia a requisição de DOWNLOAD ao peer
        sock.send(f"{filename}".encode("utf-8"))

        # Recebe o arquivo do peer
        with open(os.path.join(self.folder, filename), "wb") as file:
            while True:
                data = sock.recv(1024)
                if not data:
                    break
                file.write(data)
        sock.close()
        # Exibe mensagem no console do cliente (peer)
        print(f"Arquivo {filename} baixado com sucesso na pasta {self.folder}.")
        self.update(filename)
    
    def listen_for_download_requests(self):
        self.server_socket.listen()
        while True:
            conn, addr = self.server_socket.accept()
            threading.Thread(target=self.handle_download_request, args=[conn], daemon=True).start()
            
    def handle_download_request(self, conn):
        filename = conn.recv(1024).decode("utf-8")
        with open(os.path.join(self.folder, filename), 'r') as file:
            while True:
                data = file.read(1024)
                if not data:
                    break
                conn.write(data)
        conn.close()

# Função principal do cliente (peer)
def main():
   
    # Criação do objeto Peer
    peer = start_peer()

    while True:
        command = input("Digite seu comando (JOIN <pasta>, SEARCH <arquivo>, DOWNLOAD <ip>:<porta> <arquivo>): ")
        
        join_match = re.match(r"JOIN (.+)", command)
        if join_match:
            peer.join(join_match.group(1))

        search_match = re.match(r"SEARCH (.+)", command)
        if search_match:
            peer.search(search_match.group(1))

        download_match = re.match(r"DOWNLOAD (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):(\d+) (.+)", command)
        if download_match:
            peer.download(download_match.group(1), int(download_match.group(2)), download_match.group(3))

if __name__ == "__main__":
    main()