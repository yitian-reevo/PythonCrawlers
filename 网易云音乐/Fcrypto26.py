from Crypto.Cipher import AES
from Crypto import Random

def pad(plain):
	padlen = 16 - len(plain) % 16
	return plain + "0"*padlen

key = '0102030405060708'
iv = Random.new().read(AES.block_size)
cipher = AES.new(key, AES.MODE_CBC, iv)

plain = "The message that needs to be encrypted"
plain = pad(plain)

msg = cipher.encrypt(plain)
print (msg)