# **Programação com sockets**

## Objetivo

Criar aplicação com paradigma cliente-servidor que se comunique usando sockets.

## Características

1. Servidor rodando;

2. Servidor deve ter um socket (porta);

3. Cliente deve ter um socket (porta).

> **Explicação:** porta é aonde vai se receber as mensagens;

> **Observação:** deve ser identificada com um número;

## Roteiro

1. Threads (python)
2. Socket (python)
3. TCP (python)
4. UDP (python)

> **Explicação:** socket é equivalente ao InetAddress do Java.
 
#  Threads

### **Definições:** 
1. Serve para rodar coisas em paralelo em múltiplos CPUs.

### **Observações:** 
1. SO (sistema operacional) decide a ordem de execução.

## **Passos:**
1. Importar threading;
1. Criar classe que herda de threading;
2. Criar método run;
3. Criar try-catch dentro do método run (para chamar funções de thread).

```py
import threading

class MyThread(threading.Thread):
    def __init__(self, thread_id, name, sleep_time):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.name = name
        self.sleep_time = sleep_time

    def run(self):
        try:
            for i in range(4):
                print("T: " + self.name + " " + str(i))
                time.sleep(self.sleep_time)
        except Exception as e:
            print(f"Interrupted error: {str(e)}")
        
        print(f'Iniciando a thread {self.name}')
        # Coloque aqui o código que deseja executar na thread
        print(f'Thread {self.name} finalizada')
```

## **Conceitos:**
1. Cada thread pode executar um tipo de serviço;
2. Execução de várias atividades;
3. Ideal quando existem múltiplas cpus (cores: quadcore, octacore...);
4. Só executa ao chamar o start; 
5. Start chama método run (deve existir dentro da thread);
6. E depois devemos decidir sleep ou morte da execução.

> **Exemplo 1:** 
> Cada thread, executa um processo que, por exemplo:
> 1. thread_1:  envia pacotes;
> 2. thread_2:  recebe pacotes;

> **Exemplo 2:** 
> 1. servidor: pode ter uma thread para cada cliente;


# Socket (InetAddress - java) 

### **Definições:** 
Serve para identificar: 
1. O endereço ip do servidor ou do cliente;
2. O número de porta do socket.

### **Observações:** 

1. Representa um endereço IP em Python.

## **Passos:**

1. Importa socket;
2. Define os endereços com os métodos abaixo:
    ```py
    import socket

    # Equivalente ao getByAddress do java em python:
    address = socket.inet_ntoa(b'\xC0\xA8\x00\x01') //endereço 127.0.0.1 = localhost (sua própria máquina)

    # Equivalente ao getByName do java em python:
    address = socket.gethostbyname("www.example.com")

    # Equivalente ao getHostAddress do java em python:
    ip_address = socket.gethostbyname("www.example.com")

    # Equivalente ao getHostName do java em python:
    hostname = socket.gethostbyaddr("192.168.0.1")[0]

    '''Observe que, em Python, o método gethostbyaddr retorna uma tupla com várias informações, incluindo o nome do host. A indexação [0] é usada para obter apenas o nome do host.'''
    ```
    > **Explicação:** em java esses métodos são static.

    > **Observação:** ou seja não se criar uma instância da classe "InetAddress" "Socket" em python.

## **Conceitos:** 
1. None.


# TCP (python)

### **Definições:** 
1. TCP protocolo da camada de transporte confiável.

### **Observações:** 
1. None.

## **Passos:**

1. **Servidor:** rodar;
2. **Servidor:** criar socket para aceitar conexões (criado pelo servidor);

```py
import socket

# Configurações do servidor
HOST = '127.0.0.1'  # Endereço IP do servidor
PORT = 8080  # Porta do servidor

# Criação do socket do servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))

# Aceita uma conexão de cliente e obtém o connectionSocket
connection_socket, addr = server_socket.accept()
print(f'Cliente {addr} conectado!')

```
3. **Cliente:** criar socket para se comunicar com servidor;
4. **Cliente:** especificar endereço IP e porta do processo servidor;
    > **Explicação:** é o chamado socket receptivo (ServerSocket), na apresentação de três vias.

    ![Diagrama de Estados protocolo TCP](tres_vias.jpeg)
5. **Cliente:** cria comunicação com servidor do lado do cliente;

6. **Servidor:** cria novo socket para manter conexões 
    > **Explicação:** na apresentação de três vias:
    > 1. É o chamado socket da conexão;
    > 2. Via por onde os bytes são transferidos.

    > **Observação:** feito de forma automática pelo python.
7. **Servidor:** cria comunicação com o cliente específico.

```py
import socket

# Configurações do servidor
HOST = '127.0.0.1'  # Endereço IP do servidor
PORT = 8080  # Porta do servidor

# Criação do socket do servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)
print('Servidor aguardando conexões...')

# Aceita uma conexão de cliente e obtém o connectionSocket
connection_socket, addr = server_socket.accept()
print(f'Cliente {addr} conectado!')

# Lê a requisição do connectionSocket
request = connection_socket.recv(4096).decode()
print(f'Requisição recebida:\n{request}')

# Processa a requisição e monta a resposta
response = 'HTTP/1.1 200 OK\r\nContent-Length: 18\r\n\r\nHello, cliente!'
print(f'Resposta enviada:\n{response}')

# Envia a resposta para o connectionSocket
connection_socket.send(response.encode())

# Fecha a conexão com o cliente
connection_socket.close()

# Encerra o socket do servidor
server_socket.close()

```

```py
import socket
import threading

def handle_client(connection_socket):
    # Lê a requisição do connectionSocket
    request = connection_socket.recv(4096).decode()
    print(f'Requisição recebida:\n{request}')

    # Processa a requisição e monta a resposta
    response = 'HTTP/1.1 200 OK\r\nContent-Length: 18\r\n\r\nHello, cliente!'
    print(f'Resposta enviada:\n{response}')

    # Envia a resposta para o connectionSocket
    connection_socket.send(response.encode())

    # Fecha a conexão com o cliente
    connection_socket.close()

# Configurações do servidor
HOST = '127.0.0.1'  # Endereço IP do servidor
PORT = 8080  # Porta do servidor

# Criação do socket do servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)
print('Servidor aguardando conexões...')

while True:
    # Aceita uma conexão de cliente e obtém o connectionSocket
    connection_socket, addr = server_socket.accept()
    print(f'Cliente {addr} conectado!')

    # Cria uma nova thread para lidar com a conexão do cliente
    client_thread = threading.Thread(target=handle_client, args=(connection_socket,))
    client_thread.start()

```

> **Observação:**

## **Conceitos:**

1. TCP;

    * Permite que o servidor fale com:

        1. Múltiplos clientes;
        2. Um cliente específico.

2. Transferência de bytes;

    * Do ponto de vista da aplicação oferece transferência de bytes entre e cliente e servidor:

        1. Em ordem;
        2. Confiável;

3. Classe Socket();

    * Socket do cliente - socket da conexão;

    * Em java utiliza:
        1. InputStream: serve como entrada para "ler" as informações enviadas pela saída (output stream) do host remoto;
        2. OutputStream: serve como saída para "escrever" as informações a serem lidas pela entrada do host remoto.
        3. close() : fecha a conexão com o host remoto, o nó local não poderá obter nenhuma informação do socker após o fechamento.

4. ServerSocket(): 

    * Socket receptivo;
    * accept(): cria um novo socket;


> **Observação**: em python não precisa, mas em java precisa das classes InputStream e OutputStream na classe Socket().

### **Diagrama de estados** 

![Diagrama de Estados protocolo TCP](diagrama_de_estados.jpeg)

### **Uso da classe Socket e ServerSocket**


> **Exemplo 1:** Nó Cliente com Nó Servidor concorrente.


# Pyro 4 (RMI - java)

### **Definições:** 
1. Pyro4 é uma biblioteca Python que permite a comunicação e invocação de métodos em objetos remotos. 
2. Ele fornece um mecanismo de chamada de procedimento remoto (RPC - Remote Procedure Call) 
3. Permite que você chame métodos de objetos Python em máquinas remotas, como se estivesse chamando métodos em objetos locais.

