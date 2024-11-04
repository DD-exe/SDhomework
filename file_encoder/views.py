import base64
import os

from cryptography.hazmat.backends.openssl import backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding

from Crypto.Cipher import DES, PKCS1_OAEP
from Crypto.PublicKey import RSA

from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    _warning = ""
    if request.method == 'POST' and request.POST.get('rsa'):
        prikey, pubkey = rsa_maker()
        return render(request, 'file_encoder/index.html', {'prikey': prikey, 'pubkey': pubkey})
    if request.method == 'POST' and request.FILES.get('file'):
        mode = request.POST.get('de_mod')
        e_d = 0
        key = request.POST.get('key2')
        if key is None:
            mode = request.POST.get('en_mod')
            e_d = 1
            key = request.POST.get('key1')
        file = request.FILES['file']
        file_content = file.read()
        if mode is not None:
            if mode == "option2":
                file_content, _warning = aes(file_content, e_d, key)
            elif mode == "option3":
                file_content, _warning = des(file_content, e_d, key)
            # elif mode == "option4":
                # file_content, _warning = rsa(file_content, e_d, key)
        else:
            return render(request, 'file_encoder/index.html', {'warning': "mode=None"})
        response = HttpResponse(file_content, content_type='application/octet-stream')
        # _warning="ok"
        response['Content-Disposition'] = f'attachment; filename={_warning}'
        return response

    return render(request, 'file_encoder/index.html', {'warning': _warning})


def aes(data, e_d, key):
    if key is not None:
        if len(key) < 16:
            key = key.ljust(16, '0')
        elif 16 < len(key) < 24:
            key = key.ljust(24, '0')
        elif 24 < len(key) < 32:
            key = key.ljust(32, '0')
        elif len(key) > 32:
            return b'', "too_looooog_key.error"
    code = b''
    _warning = key
    if data is not None and key is not None:
        if e_d == 1:
            key = key.encode('utf-8')
            iv = os.urandom(16)
            cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
            encryptor = cipher.encryptor()
            padder = padding.PKCS7(128).padder()
            padded_data = padder.update(data) + padder.finalize()

            code = iv + encryptor.update(padded_data) + encryptor.finalize()
            _warning = "finish_AES_encode.enc"
        else:
            key = key.encode('utf-8')
            iv = data[:16]
            data = data[16:]
            cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
            decryptor = cipher.decryptor()
            pt = decryptor.update(data) + decryptor.finalize()
            unpadder = padding.PKCS7(128).unpadder()

            code = unpadder.update(pt) + unpadder.finalize()
            _warning = "finish_AES_decode.dec"
    return code, _warning


def des(data, e_d, key):
    if len(key) < 8:
        key = key.ljust(8, '0')
    elif len(key) > 8:
        return b'', "too_looooog_key.error"
    code = b''
    _warning = ""
    if data is not None and key is not None:
        if e_d == 1:
            key = key.encode('utf-8')
            if len(data) % 8 != 0:
                data += b'\0' * (8 - len(data) % 8)
            cipher = DES.new(key, DES.MODE_ECB)
            code = cipher.encrypt(data)
            _warning = "finish_DES_encode.enc"
        else:
            key = key.encode('utf-8')
            cipher = DES.new(key, DES.MODE_ECB)
            code = cipher.decrypt(data)
            _warning = "finish_DES_decode.dec"
    return code, _warning


def rsa(data, e_d, key):
    code = b''
    _warning = ""
    if data is not None and key is not None:
        key = RSA.import_key(base64.b64decode(key))
        if e_d == 1:
            cipher = PKCS1_OAEP.new(key)
            chunk_len = 64
            for i in range(0, len(data), chunk_len):
                chunk = data[i:i + chunk_len]
                if len(chunk) < chunk_len:
                    chunk += b'\0' * (chunk_len - len(chunk))
                code += cipher.encrypt(chunk)
            _warning = "finish_RSA_encode.enc"
        else:
            cipher = PKCS1_OAEP.new(key)
            chunk_len = 64
            for i in range(0, len(data), chunk_len):
                chunk = data[i:i + chunk_len]
                if len(chunk) < chunk_len:
                    chunk += b'\0' * (chunk_len - len(chunk))
                code += cipher.decrypt(chunk)
            _warning = "finish_RSA_decode.dec"
    return code, _warning


def rsa_maker():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()

    ans1 = "private_key:" + base64.b64encode(private_key).decode('utf-8')
    ans2 = "public_key:" + base64.b64encode(public_key).decode('utf-8')

    return ans1, ans2
