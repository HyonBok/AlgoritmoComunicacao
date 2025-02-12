import customtkinter as ctk
import matlab.engine

def matlab_algorithm(binary_data):
    eng = matlab.engine.start_matlab()
    result = binary_data  # Apenas retorna o mesmo valor sem tentar chamar uma função inexistente
    eng.quit()
    return result

def encrypt_message():
    message = entry.get()
    encrypted_text = message  # Apenas copia o texto por enquanto
    binary_representation = ' '.join(format(ord(c), '08b') for c in encrypted_text)
    processed_binary = matlab_algorithm(binary_representation)
    
    encrypted_label.configure(text=f"Criptografado: {encrypted_text}")
    binary_label.configure(text=f"Binário: {processed_binary}")
    
    # Converte os dados binários em uma lista de inteiros
    binary_values = [int(bit) for bit in processed_binary.replace(' ', '')]

    graph(binary_values)
    
def graph(binary_values):
    # Converte para o formato adequado do MATLAB (matlab.double)
    matlab_binary_values = matlab.double(binary_values)
    
    # Gerar gráfico no MATLAB
    eng = matlab.engine.start_matlab()
    
    # Criação do gráfico da onda quadrada
    eng.figure(nargout=0)
    eng.stairs(matlab_binary_values, nargout=0)  # Usando stairs para criar a onda quadrada
    eng.title('Representação Onda Quadrada')
    eng.xlabel('Posição')
    eng.ylabel('Valor Binário')
    eng.grid(True, nargout=0)
    eng.yticks([-1, 0, 1], nargout=0)  # Ajuste do eixo Y para incluir valores -1, 0, 1
    eng.quit()

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

# Inicia a interface gráfica
root.mainloop()
