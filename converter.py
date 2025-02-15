def binary_to_text(binary):
    binary_string = ''.join(str(bit) for bit in binary)  # Converte cada bit para string
    text_result = ''
    for i in range(0, len(binary), 8):  # Percorre a string de 8 em 8 bits
        byte = binary_string[i:i+8]
        if len(byte) == 8:  # Certifique-se de que temos um byte completo
            text_result += chr(int(byte, 2))  # Converte de binário para caractere
    return text_result

def text_to_binary(text):
    binary_result = ''.join(format(ord(char), '08b') for char in text)  # Sem espaços
    return binary_result
