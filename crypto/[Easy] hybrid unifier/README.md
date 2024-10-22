![img](../../../../../assets/htb.png)

<img src='../../../../../assets/logo.png' style='zoom: 80%;' align=left /><font size='5'>hybrid unifier</font>

​	19<sup>th</sup> September 2024 / Document No. D24.102.XX

​	Prepared By: `rasti`

​	Challenge Author: `rasti`

​	Difficulty: <font color='green'>Easy</font>

​	Classification: Official

# Synopsis

- `hybrid unifier` is an easy crypto challenge. This challenge implements an API with a few endpoints. The motivation behind the challenge is to showcase a real world application of Hybrid Cryptography that could be found out in the wild. The goal is to follow the correct steps, establish a secure session and communicate with the server with E2E encryption. A PDF file with instructions is provided for extra help and guidance. Having established a secure session, the player has to authenticate with the challenge/response method and send `flag` as action to get the flag.

## Description

- In the depths of an ancient library, an old manuscript held the key to an unseen power. Scholars who dared to unlock its secrets would first exchange a series of encrypted symbols, forming a bond no one could break. As they secured their connection, layers of protection wrapped around them like invisible chains. But as the final cipher was set, a chilling realization struck—the connection they forged was now bound to something far darker, something watching from the shadows.



## Skills Required

- Familiar with Python source code analysis.
- Basic knowledge of the Diffie Hellman Key Exchange Protocol.
- Know how to encrypt/decrypt data using AES.
- Know how to use libraries for API consumption.

## Skills Learned

- Learn about simplified but yet real world applications of Hybrid Cryptography and Challenge/Response authentication.
- Learn how to combine Diffie Hellman and AES to achieve fast and secure E2E encryption.

# Enumeration

In this challenge, we are provided with a simple Flask application. Below, there is the project structure:

```bash
$ tree .

.
├── Dockerfile
├── build-docker.sh
├── challenge
│   ├── README.pdf
│   └── application
│       ├── app.py
│       ├── crypto
│       │   └── session.py
│       ├── requirements.txt
│       └── views.py
└── flag.txt
```

What is interesting for us is the source code of the application, which is under the `challenge/application` directory.

We are also provided a Dockerfile and a `build-docker.sh` script to automate the process of running the application locally.

## Analyzing the source code

Let us take a look at `views.py` which handles the requests from/to the API endpoints. Above each method, there are comments that indicate to the users the correct order in which to access the endpoints.

From a cryptographic point of view, the communication is handled as:

- Client sends their Diffie Hellman public key to the server.
- The server computes the session key.
- The server sends its public key to the client so that the client agrees on the same session key.
- This session key is sha256-hashed and will be used as the AES symmetric key that will encrypt/decrypt the rest of the communication.

This info is provided in the README pdf too.

To get the flag, we need to encrypt a packet with the action set to `flag`, send it to the `/api/dashboard` endpoint and if the decryption succeeds, we get the flag. This is shown below:

```python
@bp.route('/api/dashboard', methods=['POST'])
def access_secret():
    # error handling and challenge/response omitted for brevity
    data = request.json
    encrypted_packet = data['packet_data']
    packet = session.decrypt_packet(encrypted_packet)
    action = packet['packet_data']
    if action == 'flag':
        return jsonify(session.encrypt_packet(open('/flag.txt').read()))
    elif action == 'about':
        return jsonify(session.encrypt_packet('<REDACTED>'))
    else:
        return jsonify(session.encrypt_packet('[!] Unknown action.'))
```

## Analyzing the SecureSession class

On top of the source code, we can see that a `SecureSession` object is initialized. This object will handle all the cryptography-related components of the application.

```python
session = SecureSession(384)
```

Part of the SecureSession is shown below. We will analyze the redacted methods a bit later.

```python
from Crypto.Util.number import getPrime
import os
from secrets import randbelow

class SecureSession:
    def __init__(self, bits):
        self.bits = bits
        self.g = 2
        self.p = getPrime(self.bits)
        self.compute_server_public_key()
        self.reset_challenge()
        self.initialized = False
		
    def compute_server_public_key(self):
        self.a = randbelow(self.p)
        self.server_public_key = pow(self.g, self.a, self.p)

    def reset_challenge(self):
    		self.challenge = os.urandom(24)
        
    # the rest of the class is REDACTED for brevity
```

We can see that the challenge that will be used as the authentication mechanism is a 24-byte string and the protocol being used is the Diffie Hellman Key Exchange Protocol with a random 384-bit prime.

# Solution

## Requesting the Diffie Hellman parameters

Let us start with the first endpoint.

```python
# Step 1. Request the Diffie Hellman parameters
@bp.route('/api/request-session-parameters', methods=['POST'])
def get_session_parameters():
    return jsonify({'g': hex(session.g), 'p': hex(session.p)})
```

As expected, this endpoint simply returns the domain parameters of the Diffie Hellman Key Exchange protocol; that is the generator $g$ and the prime $p$.

We need to know these parameters before sending our public key to the server.

Let us write a function that accesses this endpoint and retrieves the parameters.

```python
import json, requests

URL = 'http://localhost:1337/api'

def retrieve_dh_parameters():
		params = json.loads(requests.post(f'{URL}/request-session-parameters').content)
  	g = eval(params['g'])
		p = eval(params['p'])
    return g, p
```

## Establishing a secure session

Moving on to the next endpoint.

```python
# Step 2. Initialize a secure session with the server by sending your Diffie Hellman public key
@bp.route('/api/init-session', methods=['POST'])
def init_session():
    if session.initialized:
        return jsonify({'status_code': 400, 'error': 'A secure session has already been established.'})

    data = request.json
    if 'client_public_key' not in data:
        return jsonify({'status_code': 400, 'error': 'You need to send the client public key.'})
    
    client_public_key = data['client_public_key']
    session.establish_session_key(client_public_key)
    session.initialized = True
    return jsonify({'status_code': 200, 'success': 'A secure session was successfully established. There will be E2E encryption for the rest of the communication.', 'server_public_key': hex(session.server_public_key)})
```

We can see that this endpoint requires a `client_public_key` parameter which is self-explanatory. Upon receiving the client's public key, the server computes the shared secret with the standard Diffie Hellman method:

```python
def establish_session_key(self, client_public_key):
		key = pow(client_public_key, self.a, self.p)
    self.session_key = sha256(str(key).encode()).digest()
```

Finally, the server outputs its public key so that the session establishment completes.

Let us write a function to generate our own Diffie Hellman keys, sends the public key to the server and finally computes the session key.

```python
from hashlib import sha256
import random

def establish_secure_session(g, p):
  	a = random.randint(2, p-2)
    A = pow(g, a, p)
    server_public_key = eval(json.loads(requests.post(f'{URL}/init-session', json={'client_public_key': A}).content)['server_public_key'])
    shared_key = pow(server_public_key, a, p)
    session_key = sha256(str(shared_key).encode()).digest()
    return session_key
```

Now both ends have agreed on the same session key. The rest of the packets will be transferred encrypted and will be decrypted upon their destination is reached (E2E encryption). To access the next two endpoints, an initialized session will be mandatory.

## Authenticating with the challenge/response method

The next endpoint basically sends the encrypted challenge to the client for authentication.

```python
# Step 3. Request an encrypted challenge.
@bp.route('/api/request-challenge', methods=['POST'])
def request_challenge():
    if not session.initialized:
        return jsonify({'status_code': 400, 'error': 'A secure server-client session has to be established first.'})

    return jsonify({'encrypted_challenge': session.get_encrypted_challenge().decode()})
```

To access any other endpoint, the client must prove that they own the same session key by successfully decrypting and sending the plaintext challenge back to the server. The challenge is encrypted as follows:

```python
from base64 import b64encode as be

def get_encrypted_challenge(self):
    iv = os.urandom(16)
    cipher = AES.new(self.session_key, AES.MODE_CBC, iv)
    encrypted_challenge = iv + cipher.encrypt(pad(self.challenge, 16))
    return be(encrypted_challenge)
```

All we have to do is create a function that accesses this endpoint and decrypts the challenge after parsing the encrypted packet properly. The parsing process is summarized below:

- Base64 decode the encrypted packet
- Use the first 16 bytes as the AES-CBC IV and the rest as the encrypted data.
- Decrypt the encrypted data and unpad it.

```python
from base64 import b64decode as bd
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

def decrypt_challenge(session_key):
    data = json.loads(requests.post(f'{URL}/request-challenge').content)['encrypted_challenge']
    data = bd(data.encode())
    iv = data[:16]
    encrypted_challenge = data[16:]
    cipher = AES.new(session_key, AES.MODE_CBC, iv)
    challenge = unpad(cipher.decrypt(encrypted_challenge), 16)
    return challenge
```

## Sending the flag action

Knowing the challenge, we can now authenticate to the `/api/dashboard` endpoint. The handler for this endpoint is implemented as:

```python
# Step 4. Authenticate by responding to the challenge and send an encrypted packet with 'flag' as action to get the flag. 
@bp.route('/api/dashboard', methods=['POST'])
def access_secret():
    if not session.initialized:
        return jsonify({'status_code': 400, 'error': 'A secure server-client session has to be established first.'})

    data = request.json

    if 'challenge' not in data:
        return jsonify({'status_code': 400, 'error': 'You need to send the hash of the challenge.'})

    if 'packet_data' not in data:
        return jsonify({'status_code': 400, 'error': 'Empty packet.'})
        
    challenge_hash = data['challenge']
    if not session.validate_challenge(challenge_hash):
        return jsonify({'status_code': 401, 'error': 'Invalid challenge! Something wrong? You can visit /request-challenge to get a new challenge!'})

    encrypted_packet = data['packet_data']

    packet = session.decrypt_packet(encrypted_packet)
    if not 'packet_data' in packet:
        return jsonify({'status_code': 400, 'error': packet['error']})
    
    action = packet['packet_data']
    if action == 'flag':
        return jsonify(session.encrypt_packet(open('/flag.txt').read()))
    elif action == 'about':
        return jsonify(session.encrypt_packet('[+] Welcome to my custom API! You are currently Alpha testing my new E2E protocol.\nTo get the flag, all you have to do is to follow the protocol as intended. For any bugs, feel free to contact us :-] !'))
    else:
        return jsonify(session.encrypt_packet('[!] Unknown action.'))
```

There is a lot of error handling but the core logic of the function is not hard to understand.

Let us take a look at how the challenge is verified exactly.

```python
def validate_challenge(self, challenge_hash):
    validated = challenge_hash == sha256(self.challenge).hexdigest()
    if validated:
        self.reset_challenge()
    return validated
```

We can see that the challenges are not compared directly but are first sha256-hashed. If the challenge is valid, a new challenge is generated for future purposes and the function returns the validation status (true/false).

To get the flag, we must send the challenge hash, encrypt the string `flag` using the session key and send it to the server, base64 encoded.

Let us write a function that performs these steps:

```python
from base64 import b64encode as be

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
```

## Getting the flag

The steps to get the flag can be summarized as:

- First, the user has to retrieve the diffie hellman domain parameters.
- Then, a secure session must be established between the server and the client.
- Challenge/Response authentication is implemented so the user has to retrieve the encrypted challenge, decrypt it and send it back to the server along with any other data.
- Having the correct challenge, we can send it to `/api/dashboard` with the action set to `flag` and get the flag.

These steps are implemented with the following code.

```python
def pwn():
    g, p = retrieve_dh_parameters()
    session_key = establish_secure_session(g, p)
    challenge = decrypt_challenge(session_key)
    flag = get_flag(challenge, session_key)
    print(flag.decode())

if __name__ == '__main__':
    pwn()
```

