import Pyro4

# Classe do servidor
class Server:
    def __init__(self):
        # Inicializa as estruturas de dados do servidor
        self.peers = {}

    # Método para adicionar um peer ao servidor
    def join(self, peer_info):
        # Armazena as informações do peer no dicionário
        peer_address = peer_info["ip"] + ":" + str(peer_info["port"])
        self.peers[peer_address] = peer_info["files"]

        # Exibe a mensagem de confirmação no console do servidor
        print(f"Peer {peer_address} adicionado com arquivos {', '.join(peer_info['files'])}")

        # Retorna a resposta para o peer
        return "JOIN_OK"  
    
    # Método para procurar um arquivo no servidor    
    def search(self, filename):

        # Procura pelos peers que possuem o arquivo solicitado
        peers_with_file = [peer for peer, files in self.peers.items() if filename in files]

        # Exibe a lista de peers com o arquivo solicitado no console do servidor
        print(f"Peers com arquivo solicitado ({filename}): {', '.join(peers_with_file)}")
        
        # Retorna a lista de peers para o peer que fez a requisição
        return peers_with_file  
        
    # Método para atualizar as informações de um peer após o download
    def update(self, peer_address, filename):
       
        # Atualiza as informações do peer com o novo arquivo
        self.peers[peer_address].append(filename)

        # Exibe a mensagem de confirmação no console do servidor
        print(f"Peer {peer_address} baixou o arquivo {filename}")
        
        # Retorna a resposta para o peer
        return "UPDATE_OK"  

# Método para inicializar o servidor
def start_server():
        # Inicialização do servidor Pyro4
        daemon = Pyro4.Daemon()

        # Registro da classe Server no servidor Pyro4 
        uri = daemon.register(Server)

        # Exibe informação de inicialização do servidor
        print(f"Servidor iniciado em {uri}")

        # Aguarda as requisições dos peers
        daemon.requestLoop()

# Função principal do server
def main():
    start_server()

if __name__ == "__main__":
    main()
