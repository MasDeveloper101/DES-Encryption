from Crypto.Cipher import DES  # pip install pycryptodome


def pad(message):
    while len(message) % 8 != 0:
        message = message + ' ' # Adds a space to message
    return bytes(message, encoding='ascii')


if __name__ == "__main__":
    path = input('Do you want to encrypt or decrypt (e/d): ')
    key = bytes(input('Enter the key: '), 'ascii') # This is the secret key that differs inputs
    if path == 'E'.lower(): # Encode/Encrypt
        des = DES.new(key, DES.MODE_ECB)
        text = input('Enter text here: ')
        text = pad(text)
        c = des.encrypt(text)
        print(c.decode('utf8'))

    if path == 'D'.lower(): # Decode/Decrypt
        des = DES.new(key, DES.MODE_ECB)
        text = bytes(input('Enter what you want to encrypt: '), 'utf8')
        c = text.decode('unicode-escape').encode('ISO-8859-1')
        c = des.decrypt(c)
        print(c.decode('utf8'))