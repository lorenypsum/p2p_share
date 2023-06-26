import Pyro4
from utils import get_ip, get_port

# Classe do servidor
@Pyro4.expose
class Server:
    def __init__(self):
        # Guarda um dicionário de infomações de peer chaveadas pelo endereço de origem conectado ao Pyro4
        self.peers = {}

    # Método para adicionar um peer ao servidor
    def join(self, peer_info):
        peer_id = Pyro4.current_context.client_sock_addr
        self.peers[peer_id] = peer_info

        # Armazena resposta esperada
        response = "JOIN_OK"

        # Exibe mensagem no console do servidor
        print(f"Peer {peer_info['address']} adicionado com arquivos {' '.join(peer_info['files'])}.")
        
        # Retorna a resposta para o peer
        return response
    
    # Método para atualizar as informações de um peer após o download
    def update(self, filename):
        # Atualiza as informações do peer com o novo arquivo
        peer_id = Pyro4.current_context.client_sock_addr
        peer_info = self.peers[peer_id]
        peer_info['files'].append(filename)

        # Armazena resposta esperada
        response = "UPDATE_OK"

        # Exibe mensagem no console do servidor
        print(f"Peer {peer_info['address']} terminou o download do arquivo {filename}.")
        
        # Retorna a resposta para o peer
        return response  
    
    # Método para procurar um arquivo no servidor    
    def search(self, filename):
        peer_id = Pyro4.current_context.client_sock_addr
        peer_info = self.peers[peer_id]
        print(f"Peer {peer_info['address']} solicitou arquivo {filename}.")

        # Procura pelos peers que possuem o arquivo solicitado
        peers_with_file = [peer_info['address'] for peer_info in self.peers.values() if filename in peer_info['files']]
        
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
