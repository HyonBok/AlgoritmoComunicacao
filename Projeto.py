import customtkinter as ctk
import os
import socket
import json

import encryption
import converter
import link
import mlt3

class App:
    def __init__(self, root):
        # Gera uma chave aleatória de 256 bits (32 bytes)
        self.key = os.urandom(32)
        
        # Configuração da janela
        self.root = root
        self.root.title("Algoritmo")
        self.root.geometry("600x400")
        self.main()
    # métodos de botões:
    def encrypt_button_click(self):
        # Obtém o texto da entrada e chama a função de criptografia
        encrypted_text = encryption.encrypt_message(self.entry.get(), self.key)
        
        # Atualiza os rótulos com o texto criptografado e sua representação binária
        self.encrypted_label.configure(text=f"Criptografado: {encrypted_text}")
        
        # Converte os caracteres criptografados para binário e atualiza o rótulo binário
        binary_text = converter.text_to_binary(encrypted_text)
        self.binary_label.configure(text=f"Binário: {binary_text}")

    def change_state(self, state):
        # Limpa a tela
        for widget in self.root.winfo_children():
            widget.destroy()
        if state == 'sender':
            self.sender()
        if state == 'receiver':
            self.receiver()
        if state == 'main':
            self.main()
        if state == 'msg_received':
            self.msg_received()

    # Estados:
    def main(self):

        # Botões para Receptor e Emissor
        self.sender_button = ctk.CTkButton(self.root, text="Emissor", command=lambda: self.change_state('sender'))
        self.sender_button.pack(pady=10)

        self.receiver_button = ctk.CTkButton(self.root, text="Receptor", command=lambda: self.change_state('receiver'))
        self.receiver_button.pack(pady=10)
    def sender(self):
        # Campo de entrada
        self.entry = ctk.CTkEntry(self.root, width=300)
        self.entry.pack(pady=10)
        
        # Botão para criptografar
        self.encrypt_button = ctk.CTkButton(self.root, text="Criptografar", command=self.encrypt_button_click)
        self.encrypt_button.pack(pady=10)
        
        # Labels para exibir os resultados
        self.encrypted_label = ctk.CTkLabel(self.root, text="Criptografado:")
        self.encrypted_label.pack(pady=5)

        self.binary_label = ctk.CTkLabel(self.root, text="Binário:")
        self.binary_label.pack(pady=5)

        # Conexão:
        # Porta:
        self.port_label = ctk.CTkLabel(self.root, text="Porta: ")
        self.port_label.pack(pady=10)
        self.port_entry = ctk.CTkEntry(self.root, width=300)
        self.port_entry.pack(pady=10)

        # IP:
        self.ip_label = ctk.CTkLabel(self.root, text="IP: ")
        self.ip_label.pack(pady=10)
        self.ip_entry = ctk.CTkEntry(self.root, width=300)
        self.ip_entry.pack(pady=10)

        # Abrir conexão
        self.connect_server = ctk.CTkButton(self.root, text="Conectar", command=self.connect_server)
        self.connect_server.pack(pady=10)
        # Botão voltar
        self.back_button = ctk.CTkButton(self.root, text="Voltar", command=lambda: self.change_state('main'))
        self.back_button.pack(pady=10)

    def receiver(self):
        # Pega o endereço ip:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        self.ip_label = ctk.CTkLabel(self.root, text=f"Endereço IP: {ip_address}")
        self.ip_label.pack(pady=10)

        # Porta:
        self.port_label = ctk.CTkLabel(self.root, text="Porta: ")
        self.port_label.pack(pady=10)
        self.port_entry = ctk.CTkEntry(self.root, width=300)
        self.port_entry.pack(pady=10)
        # Abrir conexão
        self.open_server_btn = ctk.CTkButton(self.root, text="Abrir conexão", command=self.open_server)
        self.open_server_btn.pack(pady=10)

        # Botão voltar
        self.back_button = ctk.CTkButton(self.root, text="Voltar", command=lambda: self.change_state('main'))
        self.back_button.pack(pady=10)

    def msg_received(self):
        self.binary_label = ctk.CTkLabel(self.root, text=mlt3.mlt3_decode(self.received_data))
        self.binary_label.pack(pady=10)
        self.encrypted_label = ctk.CTkLabel(self.root, text=encryption.decrypt_message(self.binary_label._text, self.key))
        self.encrypted_label.pack(pady=10)
        self.msg_label = ctk.CTkLabel(self.root, text=converter.binary_to_text(self.encrypted_label._text))
        self.msg_label.pack(pady=10)

    def connect_server(self):
        link.sender(
            mlt3.mlt3_encode(self.binary_label._text),
            int(self.port_entry.get()),
            self.ip_entry.get()
        )

    def open_server(self):
        self.received_data = link.receiver(int(self.port_entry.get()))
        self.change_state('msg_received')
# Inicia a interface gráfica
if __name__ == "__main__":
    ctk.set_appearance_mode("dark")  # Tema escuro

    # Cria a janela principal e passa para a classe
    root = ctk.CTk()
    app = App(root)
    root.mainloop()