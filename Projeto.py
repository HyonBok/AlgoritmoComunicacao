import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Variável para armazenar a referência ao canvas do gráfico
current_canvas = None

def on_close():
    # Aqui você pode cancelar eventos ou destruir objetos
    if current_canvas:
        current_canvas.get_tk_widget().destroy()
    root.quit()  # Finaliza o loop de eventos do Tkinter
    root.destroy()  # Fecha a janela do Tkinter

def encrypt_message():
    message = entry.get()
    encrypted_text = message  # Apenas copia o texto por enquanto
    binary_representation = ' '.join(format(ord(c), '08b') for c in encrypted_text)
    
    encrypted_label.configure(text=f"Criptografado: {encrypted_text}")
    
    # Converte os dados binários em uma lista de inteiros
    values = [int(bit) for bit in binary_representation.replace(' ', '')]

    # Gerar o gráfico
    generate_graph(values)
    
def generate_graph(values):
    global current_canvas

    # Se já existir um gráfico, destrua o canvas antigo
    if current_canvas:
        current_canvas.get_tk_widget().destroy()

    # Cria a figura e o gráfico
    fig, ax = plt.subplots(figsize=(5, 3))  # Ajuste o tamanho conforme necessário
    ax.step(range(len(values)), values, where='post', color='b')
    
    # Ajuste os limites do gráfico
    ax.set_ylim(-1.5, 2)  # Para ter um limite maior para visualização
    ax.set_title('Representação Onda Quadrada')
    ax.set_xlabel('Posição')
    ax.set_ylabel('Valor Binário')
    
    # Configura os ticks do eixo Y
    ax.set_yticks([-1, 0, 1])

    # Ajustar para não cortar a legenda
    fig.tight_layout(pad=3.0)  # Adiciona mais espaço entre o gráfico e a legenda

    # Embede o gráfico no Tkinter
    canvas = FigureCanvasTkAgg(fig, master=frame)  # frame é o frame do Tkinter onde o gráfico será exibido
    canvas.draw()
    
    # Posiciona o canvas na parte inferior da tela
    canvas.get_tk_widget().pack(side="bottom", pady=10, fill="both", expand=True)
    
    # Atualiza a referência do canvas atual
    current_canvas = canvas

# Configuração da janela
ctk.set_appearance_mode("dark")  # Tema escuro
ctk.set_default_color_theme("blue")
root = ctk.CTk()
root.title("Algoritmo")
root.geometry("600x400")

# Campo de entrada
entry = ctk.CTkEntry(root, width=300)
entry.pack(pady=10)

# Botão para criptografar
encrypt_button = ctk.CTkButton(root, text="Criptografar", command=encrypt_message)
encrypt_button.pack(pady=10)

# Labels para exibir os resultados
encrypted_label = ctk.CTkLabel(root, text="Criptografado:")
encrypted_label.pack(pady=5)

binary_label = ctk.CTkLabel(root, text="Binário:")
binary_label.pack(pady=5)

# Frame para o gráfico
frame = ctk.CTkFrame(root)
frame.pack(pady=20, fill="both", expand=True)

root.protocol("WM_DELETE_WINDOW", on_close)

# Inicia a interface gráfica
root.mainloop()

