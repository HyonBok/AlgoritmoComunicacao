import socket

# Configuração do servidor
HOST_CLIENT = '192.168.15.14'  # Endereço IP do servidor
HOST_SERVER = '0.0.0.0'
# PORT = 65432        # Porta para escutar conexões

data = [1, 0, -1, 0, 1, -1]

def receiver(port):
    # Criando o socket do servidor
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST_SERVER, port))  # Associar o socket ao IP e porta
        server_socket.listen()            # Colocar o socket no modo de escuta
        print(f"Servidor escutando em {HOST_SERVER}:{port}...")
        
        conn, addr = server_socket.accept()  # Aceitar conexão de um cliente
        with conn:
            print(f"Conectado por {addr}")
            while True:
                data = conn.recv(1024)  # Receber até 1024 bytes
                if not data:
                    break
                print(f"Recebido: {data.decode()}")
                conn.sendall(data)  # Enviar os dados de volta (eco)

def sender(data, port, host):
    # Criando o socket do cliente
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))  # Conectar ao servidor
        client_socket.sendall(data)  # Enviar dados
        data = client_socket.recv(1024)  # Receber a resposta

    print(f"Recebido do servidor: {data.decode()}")
# data = str(data).encode()
# sender(data)
