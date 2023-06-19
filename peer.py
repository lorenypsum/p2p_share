import socket
import threading
import Pyro4
import os

from utils import get_ip, get_port, interactive_menu

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
    peer_ip = get_ip('peer')

    # Armazena endereço de porta do peer
    peer_port = get_port('peer')

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
        # Verifica se o caminho existe e armazena os arquivos encontrado nele
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
                print(f"Sou peer {self.ip}:{self.port} realizou o download do arquivo {filename}.")
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
    
    # Método para enviar arquivo da requisição de DOWNLOAD por TCP por outro peer
    def download(self, peer_ip, peer_port, filename):

        # Conecta-se ao peer utilizando sockets TCP
        sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        sock.connect((peer_ip, peer_port))

        # TODO Envia a requisição de DOWNLOAD ao peer? 
        # TODO isso devolve uma resposta?
        # ou seja, é aqui que eu recebo a resposta se a conexão foi aceita ou rejeitada
        
        # Envia a requisição de DOWNLOAD ao peer
        sock.send(f"{filename}".encode("utf-8"))

        # Armazena caminho do arquivo
        file_path = os.path.join(self.folder, filename)

        # Recebe a resposta do peer
        response = sock.recv(1024).decode("utf-8")
        response = response.lower()

        if response == "accept":
            # Tamanho do arquivo recebido do peer
            file_size = int(sock.recv(1024).decode("utf-8"))

            # Envia a resposta de aceitação para o peer
            sock.send("ACCEPT".encode("utf-8"))

            # Recebe o arquivo do peer
            with open(file_path, "wb") as file:
                bytes_received = 0
                while bytes_received < file_size:
                    data = sock.recv(4096)
                    file.write(data)
                    bytes_received += len(data)

            # Exibe mensagem no console do cliente (peer)
            print(f"Arquivo {filename} baixado com sucesso na pasta {self.folder}.")
            self.update(filename)
        else:
            # Exibe mensagem no console do cliente (peer)
            print(f"O peer {peer_ip}:{peer_port} rejeitou a transferência do arquivo {filename}.")

        sock.close()
    
    # Método de conexão para peer receber requisição de download
    def listen_for_download_requests(self):
        self.server_socket.listen()
        while True:
            conn, addr = self.server_socket.accept()
            threading.Thread(target=self.handle_download_request, args=[conn], daemon=True).start()
            
    # Método de conexão para peer enviar dados de arquivo requisitado
    def handle_download_request(self, conn):
        # Tamanho do pacote em bytes
        CHUNK_SIZE = 4096  

        # Armazenar conexão entre peers?
        filename = conn.recv(1024).decode("utf-8")

        # Armazenar caminho do arquivo
        file_path = os.path.join(self.folder, filename)

        # TODO Verifica se existe o arquivo no caminho - eu recebo essa resposta no método acima?
        if os.path.exists(file_path):
            # Enviar resposta de aceitação para o cliente
            conn.send("ACCEPT".encode("utf-8"))
        else:
            # File not found, send error message to the client
            conn.send("REJECT".encode("utf-8"))
            conn.close()
            return

        # Armazenar tamanho do arquivo
        file_size = os.path.getsize(file_path)

        # TODO Enviar o tamanho do arquivo para o cliente?
        conn.send(str(file_size).encode("utf-8"))

        # TODO Receber resposta do cliente (accept/reject)?
        response = conn.recv(1024).decode("utf-8")
        response = response.lower()

        # Verifica se cliente rejeitou enviar o arquivo
        if response != "accept":
            print("Peer rejeitou a transferência do arquivo, fechar a conexão.")
            conn.close()
            return

        # Abre o arquivo em modo binário para a leitura
        with open(file_path, 'rb') as file:
            # Envia o arquivo em pacotes
            while True:
                data = file.read(CHUNK_SIZE)
                if not data:
                    break
                #conn.write(data)
                conn.sendall(data)

        # Fecha a conezão depois que o arquivo é enviado
        conn.close()

# Função principal do cliente (peer)
def main():
    # Criação do objeto Peer
    peer = start_peer()
    # Menu iterativo do lado do cliente (peer)
    interactive_menu(peer)

if __name__ == "__main__":
    main()