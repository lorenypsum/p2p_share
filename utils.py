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
    
# Método para extrair endereço porta válido
def input_ip():    
    # Captura do IP
    ip_input = input("Informe o IP (default: 127.0.0.1): ")
    if not ip_input:
        ip_input = "127.0.0.1"
    ip = extract_ip(ip_input)
    # Exibe endereço IP recebido por input
    print(f"IP capturado: {ip}")
    return ip

def input_port():
    # Captura da porta
    port_input = input("Informe a porta (default: 1099): ")
    if not port_input:
        port_input = "1099"
    port = extract_port(port_input)
    # Exibe endereço porta recebido por input
    print(f"Porta capturada: {port}")
    return port