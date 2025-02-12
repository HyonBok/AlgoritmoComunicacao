def binary_to_text(binary):
    binary_string = ''.join(binary.split())  # Remove os espaços e junta os bits em uma string contínua
    text_result = ''
    for i in range(0, len(binary_string), 8):  # Percorre a string de 8 em 8 bits
        byte = binary_string[i:i+8]
        if len(byte) == 8:  # Certifique-se de que temos um byte completo
            text_result += chr(int(byte, 2))  # Converte de binário para caractere
    return text_result

def text_to_binary(text):
    binary_result = ' '.join(format(ord(char), '08b') for char in text)  # Mantém os espaços para visualização
    return binary_result

