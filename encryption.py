import hashlib
import os

def encrypt_message(message, key):
    
    """
    Criptografa uma mensagem usando uma chave fornecida.\n
    Parâmetros:
    - message (str): A mensagem a ser criptografada.
    - key (bytes): A chave usada para criptografar a mensagem.\n
    Retorna:
    - str: A mensagem criptografada.
    """
    
    # Gerar um sal aleatório
    salt = os.urandom(6)

    # Usar a chave e o sal para criar uma chave mais segura 
    #   - (HMAC -> Hash-based Message Authentication Code - Código de Autenticação de Mensagem Baseado em Hash)
    #   - (PBKDF2 -> Password-Based Key Derivation Function 2 - Função de Derivação de Chave Baseada em Senha 2)
    #   - (sha256 -> Secure Hash Algorithm 256 bits - Algoritmo de Hash Seguro de 256 bits)
    secure_key = hashlib.pbkdf2_hmac('sha256', key, salt, 100000)
    
    # Inicializar a mensagem criptografada com o sal em hexadecimal
    encrypted_message = salt.hex()
    for char in message:
        # Criptografar o caractere
        encrypted_char = chr((ord(char) + secure_key[0]) % 256)
        encrypted_message += encrypted_char
        # Atualizar a chave segura para o próximo caractere
        secure_key = hashlib.pbkdf2_hmac('sha256', secure_key, salt, 1)
    
    message = encrypted_message

    return message

def decrypt_message(encrypted_message, key):

    """
    Descriptografa uma mensagem usando uma chave fornecida.\n
    Parâmetros:
    - encrypted_message (str): A mensagem criptografada.
    - key (bytes): A chave usada para descriptografar a mensagem.\n
    Retorna:
    - str: A mensagem descriptografada.
    """

    # Extrair o sal da mensagem criptografada
    salt = bytes.fromhex(encrypted_message[:12])
    encrypted_message = encrypted_message[12:]
    
    # Usar a chave e o sal para criar uma chave mais segura
    secure_key = hashlib.pbkdf2_hmac('sha256', key, salt, 100000)
    
    # Inicializar a mensagem descriptografada
    decrypted_message = ""
    for char in encrypted_message:
        # Descriptografar o caractere
        decrypted_char = chr((ord(char) - secure_key[0]) % 256)
        decrypted_message += decrypted_char
        # Atualizar a chave segura para o próximo caractere
        secure_key = hashlib.pbkdf2_hmac('sha256', secure_key, salt, 1)
    
    return decrypted_message
