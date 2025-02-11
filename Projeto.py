import customtkinter as ctk

def encrypt_message():
    message = entry.get()
    encrypted_text = message  # Apenas copia o texto por enquanto
    encrypted_label.configure(text=f"Criptografado: {encrypted_text}")
    binary_label.configure(text=f"Binário: {' '.join(format(ord(c), '08b') for c in encrypted_text)}")

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