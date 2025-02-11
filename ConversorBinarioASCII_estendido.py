
def binary_to_text(binary):
    binary_values = binary.split(' ')
    ascii_characters = [chr(int(b, 2)) for b in binary_values]
    text_result = ''.join(ascii_characters)
    return text_result

def text_to_binary(text):
    binary_result = ' '.join(format(ord(char), '08b') for char in text)
    return binary_result

mensagem = "Olá, mundo! Çãõ"
binario = text_to_binary(mensagem)
print(binario)

texto = binary_to_text(binario)
print(texto)