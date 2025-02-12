import socket
import time
import json
# 192.168.15.14
# Configuração do servidor
HOST_SERVER = '0.0.0.0'

data = [1, 0, -1, 0, 1, -1]

def receiver(port):
    # Criando o socket do servidor
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST_SERVER, port))  # Associar o socket ao IP e porta
        server_socket.listen()  # Colocar o socket no modo de escuta
        print(f"Servidor escutando em {HOST_SERVER}:{port}...")
        
        conn, addr = server_socket.accept()  # Aceitar conexão de um cliente
        with conn:
            print(f"Conectado por {addr}")
            start_time = time.time()  # Armazena o tempo inicial
            while True:
                if time.time() - start_time > 10:  # Verifica se 10 segundos se passaram
                    print("Tempo limite atingido. Encerrando conexão...")
                    break
                
                data = conn.recv(1024)  # Receber até 1024 bytes
                if not data:
                    break
                conn.sendall(data)  # Enviar os dados de volta (eco)
                lista = json.loads(data.decode('utf-8'))
                print(f"Recebido: {lista}")

                return lista

def sender(data, port, host):
    # Criando o socket do cliente
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))  # Conectar ao servidor
        data_bytes = json.dumps([-1, 0, 1]).encode('utf-8')
        client_socket.sendall(data_bytes) # Enviar dados
        data = client_socket.recv(1024).decode('utf-8')  # Receber a resposta
        lista = json.loads(data)
    print(f"Recebido do servidor: {lista}")


