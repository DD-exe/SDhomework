import hashlib
from django.shortcuts import render
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from Crypto.Cipher import DES, PKCS1_OAEP
from Crypto.PublicKey import RSA
import os
import base64
from file_encoder.views import rsa_maker


def index(request):
    if request.method == 'POST' and request.POST.get('rsa'):
        prikey, pubkey = rsa_maker()
        return render(request, 'txtencoder/index.html', {'prikey': prikey, 'pubkey': pubkey})
    encode = "ans: "
    decode = "ans: "
    mode = request.POST.get('de_mod')
    if mode is None:
        mode = request.POST.get('en_mod')
    if mode is not None:
        if mode == "option1":
            e, d = shiftCipher(request)
        elif mode == "option2":
            e, d = aes(request)
        elif mode == "option3":
            e, d = des(request)
        elif mode == "option4":
            e, d = rsa(request)
        elif mode == "option5":
            e, d = md5(request)
        elif mode == "option6":
            e, d = _hash(request)
        else:
            e = ""
            d = ""
    else:
        e = ""
        d = ""
    encode += e
    decode += d
    return render(request, 'txtencoder/index.html',
                  {'encode': encode,
                   'decode': decode})


def intt(strin):
    try:
        instr = int(strin)
        return instr
    except ValueError:
        return 0


def shiftCipher(request):
    if request.method == 'POST':
        data = request.POST.get('plaintext')
        key = request.POST.get('key1')
        if data is not None and key is not None:
            encode = process_string(data, intt(key))
        else:
            encode = ""
        data = request.POST.get('ciphertext')
        key = request.POST.get('key2')
        if data is not None and key is not None:
            decode = process_string(data, -intt(key))
        else:
            decode = ""

        return encode, decode


def process_string(data, key):
    processed_string = ""
    if data:
        for char in data:
            if char.isalpha() and char.islower():
                if char == 'z':
                    processed_string += 'a'
                else:
                    processed_string += chr((ord(char) + key - ord('a')) % 26 + ord('a'))
            else:
                processed_string += char

    return processed_string


def aes(request):
    if request.method == 'POST':
        backend = default_backend()

        data = request.POST.get('plaintext')
        key = request.POST.get('key1')
        if key is not None:
            if len(key) < 16:
                key = key.ljust(16, '0')
            elif 16 < len(key) < 24:
                key = key.ljust(24, '0')
            elif 24 < len(key) < 32:
                key = key.ljust(32, '0')
            elif len(key) > 32:
                return "密钥过长", ""
        if data is not None and key is not None:
            data = data.encode('utf-8')
            key = key.encode('utf-8')
            # print(data)
            iv = os.urandom(16)
            cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
            encryptor = cipher.encryptor()
            padder = padding.PKCS7(128).padder()
            padded_data = padder.update(data) + padder.finalize()

            encode = iv + encryptor.update(padded_data) + encryptor.finalize()
        else:
            encode = b''

        data = request.POST.get('ciphertext')
        key = request.POST.get('key2')
        if key is not None:
            if len(key) < 16:
                key = key.ljust(16, '0')
            elif 16 < len(key) < 24:
                key = key.ljust(24, '0')
            elif 24 < len(key) < 32:
                key = key.ljust(32, '0')
            elif len(key) > 32:
                return "", "密钥过长"
        if data is not None and key is not None:
            mdata = base64.b64decode(data.encode('utf-8'))
            key = key.encode('utf-8')
            iv = mdata[:16]
            data = mdata[16:]
            # print(data)
            cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
            decryptor = cipher.decryptor()
            pt = decryptor.update(data) + decryptor.finalize()
            unpadder = padding.PKCS7(128).unpadder()

            decode = unpadder.update(pt) + unpadder.finalize()
        else:
            decode = b''

        return base64.b64encode(encode).decode('utf-8'), decode.decode('utf-8')


def des(request):
    if request.method == 'POST':
        data = request.POST.get('plaintext')
        key = request.POST.get('key1')
        if key is not None:
            if len(key) < 8:
                key = key.ljust(8, '0')
            elif len(key) > 8:
                return "密钥过长", ""
        if data is not None and key is not None:
            data = data.encode('utf-8')
            key = key.encode('utf-8')
            if len(data) % 8 != 0:
                data += b'\0' * (8 - len(data) % 8)
            # print(data)
            cipher = DES.new(key, DES.MODE_ECB)
            encode = cipher.encrypt(data)
        else:
            encode = b''

        data = request.POST.get('ciphertext')
        key = request.POST.get('key2')
        if key is not None:
            if len(key) < 8:
                key = key.ljust(8, '0')
            elif len(key) > 8:
                return "", "密钥过长"
        if data is not None and key is not None:
            data = base64.b64decode(data.encode('utf-8'))
            key = key.encode('utf-8')
            # print(data)
            cipher = DES.new(key, DES.MODE_ECB)
            decode = cipher.decrypt(data)
        else:
            decode = b''

        return base64.b64encode(encode).decode('utf-8'), decode.decode('utf-8')


def md5(request):
    if request.method == 'POST':
        data = request.POST.get('plaintext')
        md5_hash = hashlib.md5(data.encode()).hexdigest()
        encode = md5_hash.upper() + "(32位大写)\n"
        encode += md5_hash + "(32位小写)\n"
        encode += md5_hash.upper()[8:-8] + "(16位大写)\n"
        encode += md5_hash[8:-8] + "(16位小写)\n"

        return encode, ""


def _hash(request):
    if request.method == 'POST':
        data = request.POST.get('plaintext')
        sha1_hash = hashlib.sha1(data.encode()).hexdigest()
        sha224_hash = hashlib.sha224(data.encode()).hexdigest()
        sha256_hash = hashlib.sha256(data.encode()).hexdigest()
        sha384_hash = hashlib.sha384(data.encode()).hexdigest()
        sha512_hash = hashlib.sha512(data.encode()).hexdigest()
        encode = sha1_hash + "(SHA1)\t\t\t\t\n"
        encode += sha224_hash + "(SHA224)\n"
        encode += sha256_hash + "(SHA256)\n"
        encode += sha384_hash + "(SHA384)\n"
        encode += sha512_hash + "(SHA512)\n"

        return encode, ""


def rsa(request):
    if request.method == 'POST':
        data = request.POST.get('plaintext')
        key = request.POST.get('key1')
        if data is not None and key is not None:
            data = data.encode('utf-8')
            key = RSA.import_key(base64.b64decode(key))
            cipher = PKCS1_OAEP.new(key)
            encode = cipher.encrypt(data)
        else:
            encode = b''
        data = request.POST.get('ciphertext')
        key = request.POST.get('key2')
        if data is not None and key is not None:
            data = base64.b64decode(data.encode('utf-8'))
            key = key.encode('utf-8')
            key = RSA.import_key(base64.b64decode(key))
            cipher = PKCS1_OAEP.new(key)
            decode = cipher.decrypt(data)
        else:
            decode = b''

        return base64.b64encode(encode).decode('utf-8'), decode.decode('utf-8')
