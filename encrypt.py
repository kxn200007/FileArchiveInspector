import sys

ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
ALPHABET_INDEX = {c: i for i, c in enumerate(ALPHABET)}

def vigenere_cipher(plaintext, key, decrypt=False):
    ciphertext = []
    key_index = 0
    for char in plaintext.upper():
        if char not in ALPHABET:
            # Ignore non-alphabetic characters
            ciphertext.append(char)
        else:
            key_char = key[key_index % len(key)].upper()
            key_index += 1
            key_pos = ALPHABET_INDEX[key_char]
            char_pos = ALPHABET_INDEX[char]
            if decrypt:
                shift = char_pos - key_pos
            else:
                shift = char_pos + key_pos
            shift %= len(ALPHABET)
            ciphertext.append(ALPHABET[shift])
    return ''.join(ciphertext)


password = None
while True:
    try:
        command = sys.stdin.readline().strip()
        if not command:
            continue
        parts = command.split()
        if parts[0] == 'PASSKEY':
            password = ''.join(filter(str.isalpha, parts[1].upper()))
            print('RESULT Password set')
        elif parts[0] == 'ENCRYPT':
            if password is None:
                print('ERROR No password set')
            else:
                plaintext = ' '.join(parts[1:])
                ciphertext = vigenere_cipher(plaintext, password)
                print(f'RESULT {ciphertext}')
        elif parts[0] == 'DECRYPT':
            if password is None:
                print('ERROR No password set')
            else:
                ciphertext = ' '.join(parts[1:])
                plaintext = vigenere_cipher(ciphertext, password, decrypt=True)
                print(f'RESULT {plaintext}')
        elif parts[0] == 'QUIT':
            break
        else:
            print('ERROR Invalid command')
    except EOFError:
        break