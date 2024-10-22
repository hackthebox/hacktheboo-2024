import requests, random, json
from base64 import b64encode as be, b64decode as bd
from hashlib import sha256
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

URL = 'http://localhost:1337/api'

def retrieve_dh_parameters():
    params = json.loads(requests.post(f'{URL}/request-session-parameters').content)
    g = eval(params['g'])
    p = eval(params['p'])
    return g, p

def establish_secure_session(g, p):
    a = random.randint(2, p-2)
    A = pow(g, a, p)
    server_public_key = eval(json.loads(requests.post(f'{URL}/init-session', json={'client_public_key': A}).content)['server_public_key'])
    shared_key = pow(server_public_key, a, p)
    session_key = sha256(str(shared_key).encode()).digest()
    return session_key

def decrypt_challenge(session_key):
    data = json.loads(requests.post(f'{URL}/request-challenge').content)['encrypted_challenge']
    data = bd(data.encode())
    iv = data[:16]
    encrypted_challenge = data[16:]
    cipher = AES.new(session_key, AES.MODE_CBC, iv)
    challenge = unpad(cipher.decrypt(encrypted_challenge), 16)
    return challenge

def get_flag(challenge, session_key):
    iv = b'\x00'*16
    cipher = AES.new(session_key, AES.MODE_CBC, iv)
    encrypted_packet = iv + cipher.encrypt(pad(b'flag', 16))
    data = bd(json.loads(requests.post(f'{URL}/dashboard', json={'challenge': sha256(challenge).hexdigest(), 'packet_data': be(encrypted_packet).decode()}).content)['packet_data'])
    iv = data[:16]
    encrypted_flag = data[16:]
    cipher = AES.new(session_key, AES.MODE_CBC, iv)
    flag = unpad(cipher.decrypt(encrypted_flag), 16)
    return flag

def pwn():
    g, p = retrieve_dh_parameters()
    session_key = establish_secure_session(g, p)
    challenge = decrypt_challenge(session_key)
    flag = get_flag(challenge, session_key)
    print(flag.decode())

if __name__ == '__main__':
    pwn()