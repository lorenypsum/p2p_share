import Pyro4

from utils import get_ip, get_port

# Classe do servidor
@Pyro4.expose
class Server:
    def __init__(self):
        # Inicializa as estruturas de dados do servidor
        self.peers = {}

    # Método para adicionar um peer ao servidor
    def join(self, peer_info):
        # Armazena as informações do peer no dicionário
        peer_address = peer_info["ip"] + ":" + str(peer_info["port"])
        self.peers[peer_address] = peer_info["files"]

        # Armazena resposta esperada
        response = "JOIN_OK"

        # Exibe mensagem no console do servidor
        print(f"Peer {peer_info['ip']}:{peer_info['port']} adicionado com arquivos {' '.join(peer_info['files'])}.")
        
        # Retorna a resposta para o peer
        return response
    
    # Método para atualizar as informações de um peer após o download
    def update(self, peer_info, filename):
        # Armazena as informações do endereço do peer no dicionário
        peer_address = peer_info["ip"] + ":" + str(peer_info["port"])
       
        # Atualiza as informações do peer com o novo arquivo
        self.peers[peer_address].append(filename)

        # Armazena resposta esperada
        response = "UPDATE_OK"

        # Exibe mensagem no console do servidor
        print(f"Peer {peer_info['ip']}:{peer_info['port']} terminou o download do arquivo {filename}.")
        
        # Retorna a resposta para o peer
        return response  
    
    # Método para procurar um arquivo no servidor    
    def search(self, peer_info, filename):

        # Procura pelos peers que possuem o arquivo solicitado
        peers_with_file = [peer for peer, files in self.peers.items() if filename in files]

        # Exibe mensagem no console do servidor
        print(f"Peer {peer_info['ip']}:{peer_info['port']} solicitou arquivo {filename}.")
        
        # Retorna a lista de peers para o peer que fez a requisição
        return peers_with_file  
        
# Método para inicializar o servidor
def start_server():

    # Exibe a mensagem
    print("Inicializando Server.")
    
    # Armazena endereço de IP do servidor
    ip = get_ip('servidor')

    # Armazena endereço de porta do servidor
    port = get_port('servidor')

    # Inicialização do servidor Pyro4
    daemon = Pyro4.Daemon(host=ip, port=port)
    uri = daemon.register(Server(), 'server')

    # Exibe informações de inicialização do servidor
    print(f"Servidor iniciado em: {uri}")

    # Aguarda as requisições dos peers
    daemon.requestLoop()


# Função principal do server
def main():
    start_server()

if __name__ == "__main__":
    main()
