from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
import os
from cryptography.hazmat.backends import default_backend

def encrypt_message(message, key):
    # Gera um IV (vetor de inicialização) aleatório
    iv = os.urandom(16)
    
    # Cria um objeto Cipher com o algoritmo AES no modo CBC
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    # Cria um encriptador
    encryptor = cipher.encryptor()
    
    # Adiciona padding à mensagem para que seu tamanho seja múltiplo do bloco
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_message = padder.update(message.encode()) + padder.finalize()
    
    # Criptografa a mensagem
    encrypted_message = encryptor.update(padded_message) + encryptor.finalize()
    
    return iv + encrypted_message

def decrypt_message(encrypted_message, key):
    # Extrai o IV da mensagem criptografada
    iv = encrypted_message[:16]
    encrypted_message = encrypted_message[16:]
    
    # Cria um objeto Cipher com o algoritmo AES no modo CBC
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    
    # Cria um descriptador
    decryptor = cipher.decryptor()
    
    # Descriptografa a mensagem
    padded_message = decryptor.update(encrypted_message) + decryptor.finalize()
    
    # Remove o padding da mensagem
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    message = unpadder.update(padded_message) + unpadder.finalize()
    
    return message.decode()

# Gera uma chave aleatória de 256 bits (32 bytes)
key = os.urandom(32)

# Mensagem a ser criptografada
message = "Esta é uma mensagem secreta."

# Criptografa a mensagem
encrypted_message = encrypt_message(message, key)
print(f"Mensagem criptografada: {encrypted_message}")

# Descriptografa a mensagem
decrypted_message = decrypt_message(encrypted_message, key)
print(f"Mensagem descriptografada: {decrypted_message}")