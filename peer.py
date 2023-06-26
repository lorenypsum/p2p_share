import random
import socket
import threading
import Pyro4
import os

from utils import get_file_names, get_ip, get_port, interactive_menu

# Classe do Cliente (Peers)


class Peer:

    # Inicializa as informações o peer
    def __init__(self, server_uri, ip, port, folder):
        self.server_uri = server_uri
        self.ip = ip
        self.port = port
        self.folder = folder
        self.proxy = Pyro4.Proxy(server_uri)
        self.server_socket = socket.create_server(
            (self.ip, self.port), family=socket.AF_INET)
        threading.Thread(
            target=self.listen_for_download_requests, daemon=True).start()

    # Método para enviar requisição de JOIN ao servidor

    def join(self, folder):
        # Verifica se o caminho existe e armazena os arquivos encontrado nele
        files = get_file_names(folder)

        # Lógica para conectar peer ao servidor
        try:
            # Acessa servidor por proxy
            response = self.proxy.join(
                {'address': f'{self.ip}:{self.port}', 'files': files})
            if response == "JOIN_OK":
                # Exibe mensagem no console do cliente (peer)
                print(
                    f"Sou peer {self.ip}:{self.port} com arquivos {' '.join(files)}.")
            else:
                # Exibe mensagem no console do cliente (peer)
                print(f"Resposta inesperada (join_server): {response}.")
        except Exception as e:
            # Exibe mensagem no console do cliente (peer)
            print(f"Ocorreu uma exceção (join_server): {e}")

    # Método para enviar requisição de UPDATE ao servidor
    def update(self, filename):
        try:
            # Acessa servidor por proxy
            response = self.proxy.update(filename)
            # Lógica
            if response == "UPDATE_OK":
                # Exibe mensagem no console do cliente (peer)
                print(
                    f"Sou peer {self.ip}:{self.port} realizou o download do arquivo {filename}.")
            else:
                # Exibe mensagem no console do cliente (peer)
                print(f"Resposta inesperada (update_server): {response}.")
        except Exception as e:
            # Exibe mensagem no console do cliente (peer)
            print(f"Ocorreu uma exceção (update_server): {e}")

    # Método para enviar requisição de SEARCH ao servidor
    def search(self, filename):
        try:
            # Acessa servidor por proxy
            response = self.proxy.search(filename)
            # Exibe mensagem no console do cliente (peer)
            print(f"Peers com arquivo solicitado: {' '.join(response)}.")
        except Exception as e:
            # Exibe mensagem no console do cliente (peer)
            print(f"Ocorreu uma exceção (search_server): {e}.")

    # Método para enviar arquivo da requisição de DOWNLOAD por TCP por outro peer
    def download(self, peer_ip, peer_port, filename):
        # Conecta-se ao peer utilizando sockets TCP
        sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        sock.connect((peer_ip, peer_port))
        with sock:
            # Envia a requisição de DOWNLOAD ao peer, que vai recebê-la no método handle_download_request
            sock.sendall(f"{filename}".encode("utf-8"))

            # Recebe a resposta do peer
            response = sock.recv(6).decode("utf-8")
            if response.lower() != "accept":
                # Exibe mensagem no console do cliente (peer)
                print(
                    f"O peer {peer_ip}:{peer_port} rejeitou a transferência do arquivo {filename}.")
                return

            # Armazena caminho do arquivo
            file_path = os.path.join(self.folder, filename)
            # Recebe o arquivo do peer
            with open(file_path, "wb") as file:
                while True:
                    data = sock.recv(4096)
                    if not data:
                        break
                    file.write(data)
            print(
                f"Arquivo {filename} baixado com sucesso na pasta {self.folder}.")
            self.update(filename)

    # Método de conexão para peer receber requisição de download
    def listen_for_download_requests(self):
        self.server_socket.listen()
        while True:
            sock, addr = self.server_socket.accept()
            threading.Thread(target=self.handle_download_request,
                             args=[sock], daemon=True).start()

    # Método de conexão para peer enviar dados de arquivo requisitado
    def handle_download_request(self, sock: socket.socket):
        with sock:
            # Recebe o nome do arquivo desejado
            filename = sock.recv(4096).decode("utf-8")

            # Armazenar caminho do arquivo
            file_path = os.path.join(self.folder, filename)

            # Verifica se existe o arquivo no caminho - peer recebe essa resposta no método download
            if not os.path.exists(file_path) or random.random() > 0.5:
                sock.sendall("REJECT".encode("utf-8"))
                return
            sock.sendall("ACCEPT".encode("utf-8"))

            # Enviar o arquivo
            with open(file_path, 'rb') as file:
                sock.sendfile(file)


# Inicialização do peer
def start_peer():

    # Exibe a mensagem
    print("Inicializando Peer.")

    # Armazena endereço de IP do peer
    peer_ip = get_ip('peer')

    # Armazena endereço de porta do peer
    peer_port = get_port('peer')

    # Armazena server_uri
    server_uri = input(
        f"Digite a uri do servidor: (default: PYRO:server@127.0.0.1:1099): ")
    if not server_uri:
        server_uri = f"PYRO:server@127.0.0.1:1099"

    # Captura as informações de pasta do peer
    peer_folder = input("Digite a pasta do peer: (default: . ) ")
    if not peer_folder:
        peer_folder = '.'

    # Inicializa peer
    peer = Peer(ip=peer_ip, server_uri=server_uri,
                port=peer_port, folder=peer_folder)
    return peer


# Função principal do cliente (peer)
def main():
    # Criação do objeto Peer
    peer = start_peer()
    # Menu iterativo do lado do cliente (peer)
    interactive_menu(peer)


if __name__ == "__main__":
    main()
