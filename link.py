import socket

# Configuração do servidor
HOST = '127.0.0.1'  # Endereço IP local (localhost)
PORT = 65432        # Porta para escutar conexões

data = [1, 0, -1, 0, 1, -1]

def receiver():
    # Criando o socket do servidor
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))  # Associar o socket ao IP e porta
        server_socket.listen()            # Colocar o socket no modo de escuta
        print(f"Servidor escutando em {HOST}:{PORT}...")
        
        conn, addr = server_socket.accept()  # Aceitar conexão de um cliente
        with conn:
            print(f"Conectado por {addr}")
            while True:
                data = conn.recv(1024)  # Receber até 1024 bytes
                if not data:
                    break
                print(f"Recebido: {data.decode()}")
                conn.sendall(data)  # Enviar os dados de volta (eco)

def sender(data):
    # Criando o socket do cliente
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))  # Conectar ao servidor
        client_socket.sendall(data)  # Enviar dados
        data = client_socket.recv(1024)  # Receber a resposta

    print(f"Recebido do servidor: {data.decode()}")
