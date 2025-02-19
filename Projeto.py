import customtkinter as ctk
import os
import socket
import json
import encryption
import converter
import link
import mlt3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class App:
    def __init__(self, root):
        # Chave estática
        self.key = 256 * b'\x02' # Chave de 256 bytes com o valor 2
        
        # Configuração da janela
        self.root = root
        self.root.title("Algoritmo")
        self.root.geometry(f"{2000}x{1100}+{-10}+{-10}")  # Definindo a altura mínima da janela para 800px (Caber o gráfico)
        self.main()

        self.encrypted = None
        self.binary = None
        self.mlt = None

        self.fig = None  # Variável para armazenar o gráfico
        self.current_canvas = None  # Inicialização de current_canvas como None

    # Métodos de botões:
    def encrypt_button_click(self):
        # Obtém o texto da entrada e chama a função de criptografia
        encrypted_text = encryption.encrypt_message(self.entry.get(), self.key)
        
        # Atualiza os rótulos com o texto criptografado e sua representação binária
        self.encrypted_label.configure(text=encrypted_text)
        # self.encrypted_label.configure(text=self.entry.get())
        
        # Converte os caracteres criptografados para binário e atualiza o rótulo binário
        self.binary = converter.text_to_binary(encrypted_text)
        formatted_binary = ' '.join([self.binary[i:i+4] for i in range(0, len(self.binary), 4)])
        self.binary_label.configure(text=formatted_binary) # Colocar espaçamento entre 4 bits

        self.generate_graph(mlt3.mlt3_encode(self.binary_label._text), self.results_frame)

    def binary_button_click(self):

        # Atualiza o rótulo binário com o texto da entrada
        self.binary_label.configure(text=self.binary_entry.get())

        self.generate_graph(mlt3.mlt3_encode(self.binary_label._text), self.results_frame)


    def generate_graph(self, code, results_frame):
        if self.current_canvas:
            self.current_canvas.get_tk_widget().destroy()

        # encode = mlt3.mlt3_encode(self.binary_label._text)
        encode = [int(x) - 1 for x in code]

        # Cria a figura e o gráfico com tamanho maior
        self.fig, self.ax = plt.subplots(figsize=(10, 6))  # Ajuste o tamanho conforme necessário
        self.ax.step(range(len(encode) + 1), encode + [encode[-1]], where='post', color='b')

        # Ajuste os limites do gráfico
        self.ax.set_ylim(-1.5, 2)  # Para ter um limite maior para visualização
        self.ax.set_title('Representação Onda Quadrada')
        self.ax.set_xlabel('Posição')
        self.ax.set_ylabel('Valor Binário')

        # Configura os ticks do eixo Y
        self.ax.set_yticks([-1, 0, 1])

        # Ajustar para não cortar a legenda
        self.fig.tight_layout(pad=3.0)  # Adiciona mais espaço entre o gráfico e a legenda
        
        # Embede o gráfico no Tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, master=results_frame)  # frame é o frame do Tkinter onde o gráfico será exibido
        self.canvas.draw()

        # Armazena o canvas atual para poder destruir o anterior, se necessário
        self.current_canvas = self.canvas
        self.canvas.get_tk_widget().pack()  # Exibe o gráfico na janela

        # Conectar eventos de zoom e movimento
        self.canvas.mpl_connect("scroll_event", self.on_scroll_or_move)  # Conecta o evento de scroll

    def on_scroll_or_move(self, event):
        """Zoom com a roda do mouse ou movimento horizontal com Shift + Scroll."""
        if self.current_canvas is None or not self.fig:  # Verifica se há um gráfico
            return  # Não faz nada se não houver gráfico

        # Verifica se a tecla Shift está pressionada durante o scroll
        if 'shift' in event.modifiers:  # 'shift' estará presente em event.modifiers
            # Movimento horizontal com Shift + Scroll
            direction = 1 if event.step > 0 else -1
            xlim = self.ax.get_xlim()
            new_xlim = [xlim[0] + direction * 0.05 * (xlim[1] - xlim[0]), 
                        xlim[1] + direction * 0.05 * (xlim[1] - xlim[0])]
            self.ax.set_xlim(new_xlim)  # Ajusta os limites horizontais
            self.canvas.draw()
        else:
            # Zoom normal com a roda do mouse
            xlim = self.ax.get_xlim()
            zoom_factor = 0.9 if event.step > 0 else 1.1  # Aproxima com scroll up, afasta com scroll down
            self.ax.set_xlim([event.xdata + (x - event.xdata) * zoom_factor for x in xlim])
            self.canvas.draw()

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

        # Título da tela
        self.title_label = ctk.CTkLabel(self.root, text="Tela Inicial", font=("Arial", 80), text_color="white")
        self.title_label.pack(pady=100)

        # Frame para centralizar os botões
        self.center_frame = ctk.CTkFrame(self.root)
        self.center_frame.place(relx=0.5, rely=0.5, anchor='center')

        # Botões para Receptor e Emissor
        self.sender_button = ctk.CTkButton(self.center_frame, text="Emissor", command=lambda: self.change_state('sender'), width=200, height=50, fg_color="green")
        self.sender_button.pack(pady=40, padx=20)

        self.receiver_button = ctk.CTkButton(self.center_frame, text="Receptor", command=lambda: self.change_state('receiver'), width=200, height=50, fg_color="green")
        self.receiver_button.pack(pady=40, padx=20)

        # Botão para fechar a aplicação
        self.quit_button = ctk.CTkButton(self.center_frame, text="Fechar", command=fechar_app, width=200, height=50, fg_color="red")
        self.quit_button.pack(pady=40, padx=20)

    def sender(self):
        
        # Frame para a entrada e criptografia
        entry_frame = ctk.CTkFrame(self.root)
        entry_frame.place(relx=0.2, rely=0.3, anchor='center')

        # Campo de entrada com texto de placeholder
        self.entry_label = ctk.CTkLabel(entry_frame, text="Mensagem:")
        self.entry_label.pack(pady=5)
        self.entry = ctk.CTkEntry(entry_frame, width=280, placeholder_text="Digite a Mensagem")
        self.entry.pack(pady=10)
        
        # Botão para criptografar
        self.encrypt_button = ctk.CTkButton(entry_frame, text="Criptografar", command=self.encrypt_button_click)
        self.encrypt_button.pack(pady=10)

        # Frame para a conexão
        connection_frame = ctk.CTkFrame(self.root)
        connection_frame.place(relx=0.2, rely=0.5, anchor='center')

        # Porta:
        self.port_label = ctk.CTkLabel(connection_frame, text="Porta: ")
        self.port_label.grid(row=0, column=0, padx=10, pady=10, sticky='e')
        self.port_entry = ctk.CTkEntry(connection_frame, width=200)
        self.port_entry.grid(row=0, column=1, padx=10, pady=10)

        # IP:
        self.ip_label = ctk.CTkLabel(connection_frame, text="IP: ")
        self.ip_label.grid(row=1, column=0, padx=10, pady=10, sticky='e')
        self.ip_entry = ctk.CTkEntry(connection_frame, width=200)
        self.ip_entry.grid(row=1, column=1, padx=10, pady=10)
        
        # Abrir conexão
        self.connect_server = ctk.CTkButton(connection_frame, text="Conectar", command=self.connect_server)
        self.connect_server.grid(row=2, column=0, columnspan=2, pady=10)

        # Frame para os resultados com tamanho mínimo
        self.results_frame = ctk.CTkFrame(self.root)
        self.results_frame.place(relx=0.7, rely=0.47, anchor='center')

        # Labels para exibir os resultados
        self.encrypted_label_title = ctk.CTkLabel(self.results_frame, text="Criptografado:", font=("Arial", 16, "italic"), text_color="cyan")
        self.encrypted_label = ctk.CTkLabel(self.results_frame, text="", font=("Arial", 14), text_color="white")
        self.encrypted_label_title.pack(pady=10)
        self.encrypted_label.pack(pady=10)

        self.binary_label_title = ctk.CTkLabel(self.results_frame, text="Binário:", font=("Arial", 16, "italic"), text_color="cyan")
        self.binary_label = ctk.CTkLabel(self.results_frame, text="", wraplength=900, font=("Arial", 14), text_color="white")  # Define wraplength para quebrar a linha
        self.binary_label_title.pack(pady=10)
        self.binary_label.pack(pady=10)

        # Adiciona um campo de entrada para o binário
        # Frame para o binário
        binary_frame = ctk.CTkFrame(self.root)
        binary_frame.place(relx=0.2, rely=0.7, anchor='center')

        # Campo de entrada com texto de placeholder
        self.binary_entry = ctk.CTkEntry(binary_frame, width=200, placeholder_text="Digite o binário a ser plotado")
        self.binary_entry.grid(row=0, column=1, padx=10, pady=10)

        # Botão para enviar o binário
        self.binary_button = ctk.CTkButton(binary_frame, text="Plotar Binário", command=self.binary_button_click)
        self.binary_button.grid(row=1, column=0, columnspan=2, pady=10)

        # Botão voltar
        self.back_button = ctk.CTkButton(self.results_frame, text="Voltar", command=lambda: self.change_state('main'))
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

    def test_receiver(self, data):

        # Limpa a tela
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.received_data = data

        # Frame para os resultados
        self.results_frame = ctk.CTkFrame(self.root)
        self.results_frame.place(relx=0.20, rely=0.45, anchor='center')

        # Gráfico
        graphics_frame = ctk.CTkFrame(self.root)
        graphics_frame.place(relx=0.71, rely=0.46, anchor='center')

        self.generate_graph(self.received_data, graphics_frame)

        # Labels para exibir os resultados
        self.binary_label_title = ctk.CTkLabel(self.results_frame, text="Binário Recebido:", font=("Arial", 16, "italic"), text_color="cyan")
        binary_text = mlt3.mlt3_decode(self.received_data)
        formatted_binary = ' '.join([binary_text[i:i+4] for i in range(0, len(binary_text), 4)])
        self.binary_label = ctk.CTkLabel(self.results_frame, text=formatted_binary, wraplength=500, font=("Arial", 14), text_color="white")
        self.binary_label_title.pack(pady=10)
        self.binary_label.pack(pady=10)

        self.msg_label_title = ctk.CTkLabel(self.results_frame, text="Mensagem Decodificada:", font=("Arial", 16, "italic"), text_color="cyan")
        self.msg_label = ctk.CTkLabel(self.results_frame, text=converter.binary_to_text(self.binary_label._text), wraplength=900, font=("Arial", 14), text_color="white")
        self.msg_label_title.pack(pady=10)
        self.msg_label.pack(pady=10)

        self.encrypted_label_title = ctk.CTkLabel(self.results_frame, text="Mensagem Decriptografada:", font=("Arial", 16, "italic"), text_color="cyan")
        self.encrypted_label = ctk.CTkLabel(self.results_frame, text=encryption.decrypt_message((self.msg_label._text), self.key), wraplength=900, font=("Arial", 14), text_color="white")
        self.encrypted_label_title.pack(pady=10)
        self.encrypted_label.pack(pady=10)

        # Botão voltar
        self.back_button = ctk.CTkButton(self.results_frame, text="Voltar", command=lambda: self.change_state('receiver'))
        self.back_button.pack(pady=20)

    def msg_received(self):
        # self.binary_label = ctk.CTkLabel(self.root, text=mlt3.mlt3_decode(self.received_data))
        # self.binary_label.pack(pady=10)

        # self.msg_label = ctk.CTkLabel(self.root, text=converter.binary_to_text(self.binary_label._text))
        # self.msg_label.pack(pady=10)

        # self.encrypted_label = ctk.CTkLabel(self.root, text=encryption.decrypt_message((self.msg_label._text), self.key))
        # self.encrypted_label.pack(pady=10)

        # self.generate_graph(self.received_data)
        # # Botão voltar
        # self.back_button = ctk.CTkButton(self.root, text="Voltar", command=lambda: self.change_state('receiver'))
        # self.back_button.pack(pady=10)

        # self.received_data = data

        # Frame para os resultados
        self.results_frame = ctk.CTkFrame(self.root)
        self.results_frame.place(relx=0.20, rely=0.45, anchor='center')

        # Gráfico
        graphics_frame = ctk.CTkFrame(self.root)
        graphics_frame.place(relx=0.71, rely=0.46, anchor='center')

        self.generate_graph(self.received_data, graphics_frame)

        # Labels para exibir os resultados
        self.binary_label_title = ctk.CTkLabel(self.results_frame, text="Binário Recebido:", font=("Arial", 16, "italic"), text_color="cyan")
        binary_text = mlt3.mlt3_decode(self.received_data)
        formatted_binary = ' '.join([binary_text[i:i+4] for i in range(0, len(binary_text), 4)])
        self.binary_label = ctk.CTkLabel(self.results_frame, text=formatted_binary, wraplength=500, font=("Arial", 14), text_color="white")
        self.binary_label_title.pack(pady=10)
        self.binary_label.pack(pady=10)

        self.msg_label_title = ctk.CTkLabel(self.results_frame, text="Mensagem Decodificada:", font=("Arial", 16, "italic"), text_color="cyan")
        self.msg_label = ctk.CTkLabel(self.results_frame, text=converter.binary_to_text(self.binary_label._text), wraplength=900, font=("Arial", 14), text_color="white")
        self.msg_label_title.pack(pady=10)
        self.msg_label.pack(pady=10)

        self.encrypted_label_title = ctk.CTkLabel(self.results_frame, text="Mensagem Decriptografada:", font=("Arial", 16, "italic"), text_color="cyan")
        self.encrypted_label = ctk.CTkLabel(self.results_frame, text=encryption.decrypt_message((self.msg_label._text), self.key), wraplength=900, font=("Arial", 14), text_color="white")
        self.encrypted_label_title.pack(pady=10)
        self.encrypted_label.pack(pady=10)

        # Botão voltar
        self.back_button = ctk.CTkButton(self.results_frame, text="Voltar", command=lambda: self.change_state('receiver'))
        self.back_button.pack(pady=20)

    def connect_server(self):
        # self.test_receiver(mlt3.mlt3_encode(self.binary_label._text))
        link.sender(
            mlt3.mlt3_encode(self.binary_label._text),
            int(self.port_entry.get()),
            self.ip_entry.get()
        )

    def open_server(self):
        self.received_data = link.receiver(int(self.port_entry.get()))
        self.change_state('msg_received')

def fechar_app():
    root.quit()  # Finaliza o loop de eventos de forma segura
    root.destroy()  # Libera os recursos de forma limpa

# Inicia a interface gráfica
if __name__ == "__main__":
    ctk.set_appearance_mode("dark")  # Tema escuro

    # Cria a janela principal e passa para a classe
    root = ctk.CTk()
    app = App(root)
    root.protocol("WM_DELETE_WINDOW", fechar_app)
    root.mainloop()
