from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
app = Flask(__name__)
CORS(app)
import time
from function import encode, decode, encode_str, decode_str, encodeCBCString, decodeCBCString, Meet_in_the_Middle, doubleEncode, doubleDecode, tripleEncode, tripleDecode
import numpy as np
from werkzeug.utils import secure_filename
import os

@app.route('/encrypt16Bit', methods=['POST'])
@cross_origin(origin='http://127.0.0.1:8080')  # 允许指定源的跨域请求
# 8080 端口是前端开发服务器运行的端口，只有来自 http://127.0.0.1:8080 的前端请求才会被允许进行跨域通信
def encrypt16Bit():
    data = request.get_json()
    key = data['key']
    plaintext = data['plaintext']
    key = np.array(list(key)).astype(int)
    plaintext = np.array(list(plaintext)).astype(int)
    # 调用加密函数
    encrypted = encode(key, plaintext)
    return jsonify({'encrypted': encrypted.tolist()})


@app.route('/decrypt16Bit', methods=['POST'])
@cross_origin(origin='http://127.0.0.1:8080')  # 允许指定源的跨域请求
def decrypt16Bit():
    data = request.get_json()
    key = data['key']
    ciphertext = data['ciphertext']
    key = np.array(list(key)).astype(int)
    ciphertext = np.array(list(ciphertext)).astype(int)
    # 调用解密函数
    decrypted = decode(key, ciphertext)
    return jsonify({'decrypted': decrypted.tolist()})

@app.route('/encrypt16Bit_2AES', methods=['POST'])
@cross_origin(origin='http://127.0.0.1:8080')  # 允许指定源的跨域请求
# 8080 端口是前端开发服务器运行的端口，只有来自 http://127.0.0.1:8080 的前端请求才会被允许进行跨域通信
def encrypt16Bit_2AES():
    data = request.get_json()
    key = data['key']
    plaintext = data['plaintext']
    key = np.array(list(key)).astype(int)
    plaintext = np.array(list(plaintext)).astype(int)
    # 调用加密函数
    encrypted = doubleEncode(key, plaintext)
    return jsonify({'encrypted': encrypted.tolist()})


@app.route('/decrypt16Bit_2AES', methods=['POST'])
@cross_origin(origin='http://127.0.0.1:8080')  # 允许指定源的跨域请求
def decrypt16Bit_2AES():
    data = request.get_json()
    key = data['key']
    ciphertext = data['ciphertext']
    key = np.array(list(key)).astype(int)
    ciphertext = np.array(list(ciphertext)).astype(int)
    # 调用解密函数
    decrypted = doubleDecode(key, ciphertext)
    return jsonify({'decrypted': decrypted.tolist()})


@app.route('/encrypt16Bit_3AES', methods=['POST'])
@cross_origin(origin='http://127.0.0.1:8080')  # 允许指定源的跨域请求
# 8080 端口是前端开发服务器运行的端口，只有来自 http://127.0.0.1:8080 的前端请求才会被允许进行跨域通信
def encrypt16Bit_3AES():
    data = request.get_json()
    key = data['key']
    plaintext = data['plaintext']
    key = np.array(list(key)).astype(int)
    plaintext = np.array(list(plaintext)).astype(int)
    # 调用加密函数
    encrypted = tripleEncode(key, plaintext)
    return jsonify({'encrypted': encrypted.tolist()})


@app.route('/decrypt16Bit_3AES', methods=['POST'])
@cross_origin(origin='http://127.0.0.1:8080')  # 允许指定源的跨域请求
def decrypt16Bit_3AES():
    data = request.get_json()
    key = data['key']
    ciphertext = data['ciphertext']
    key = np.array(list(key)).astype(int)
    ciphertext = np.array(list(ciphertext)).astype(int)
    # 调用解密函数
    decrypted = tripleDecode(key, ciphertext)
    return jsonify({'decrypted': decrypted.tolist()})


# ASCII加密路由
@app.route('/encrypt_ascii', methods=['POST'])
@cross_origin(origin='http://127.0.0.1:8080')  # 允许指定源的跨域请求
def encrypt_ascii():
    data = request.get_json()
    plaintext = data['plaintext']
    key = data['key']
    key = np.array(list(key)).astype(int)
    encrypted = encode_str(key, plaintext)
    return jsonify({"encrypted": encrypted})

# ASCII解密路由
@app.route('/decrypt_ascii', methods=['POST'])
@cross_origin(origin='http://127.0.0.1:8080')
def decrypt_ascii():
    data = request.get_json()
    ciphertext = data['ciphertext']
    key = data['key']
    key = np.array(list(key)).astype(int)
    decrypted = decode_str(key, ciphertext)
    return jsonify({"decrypted": decrypted})

# ASCII加密路由CBC
@app.route('/encrypt_ascii_CBC', methods=['POST'])
@cross_origin(origin='http://127.0.0.1:8080')  # 允许指定源的跨域请求
def encrypt_ascii_CBC():
    data = request.get_json()
    plaintext = data['plaintext']
    key = data['key']
    key = np.array(list(key)).astype(int)
    encrypted = encodeCBCString(key, plaintext)
    return jsonify({"encrypted": encrypted})


# ASCII解密路由CBC
@app.route('/decrypt_ascii_CBC', methods=['POST'])
@cross_origin(origin='http://127.0.0.1:8080')
def decrypt_ascii_CBC():
    data = request.get_json()
    ciphertext = data['ciphertext']
    key = data['key']
    key = np.array(list(key)).astype(int)
    decrypted = decodeCBCString(key, ciphertext)
    return jsonify({"decrypted": decrypted})


@app.route('/encrypt_file', methods=['POST'])
@cross_origin(origin='http://127.0.0.1:8080')  # 允许指定源的跨域请求
def encrypt_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    file = request.files['file']
    key = request.form.get('key')
    try:
        key = np.array(list(key)).astype(int)
    except ValueError:
        return jsonify({'error': 'Invalid key format'}), 400

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join('/tmp', filename)
    file.save(file_path)

    encrypted_content = ''
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                encrypted_line = encodeCBCString(key, line)
                encrypted_content += encrypted_line
    finally:
        os.remove(file_path)  # 删除临时保存的文件
       # 返回加密后的内容
    return jsonify({'encrypted': encrypted_content})



@app.route('/decrypt_file', methods=['POST'])
@cross_origin(origin='http://127.0.0.1:8080')  # 允许指定源的跨域请求
def decrypt_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    file = request.files['file']
    key = request.form.get('key')
    try:
        key = np.array(list(key)).astype(int)
    except ValueError:
        return jsonify({'error': 'Invalid key format'}), 400

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join('/tmp', filename)
    file.save(file_path)

    decrypted_content = ''
    try:
        with open(file_path, 'r',encoding='utf-8') as file:
            for line in file:
                decrypted_line = decodeCBCString(key, line)
                decrypted_content += decrypted_line
    finally:
        os.remove(file_path)  # 删除临时保存的文件
    return jsonify({'decrypted': decrypted_content})


# 中间相遇路由
@app.route('/attack', methods=['POST'])
@cross_origin(origin='http://127.0.0.1:8080')
def attack():
    data = request.get_json()
    plaintext = data['plaintext']
    ciphertext = data['ciphertext']
    ciphertext = np.array(list(ciphertext)).astype(int)
    plaintext = np.array(list(plaintext)).astype(int)
    key = Meet_in_the_Middle(ciphertext, plaintext)
    if key and all(isinstance(k, np.ndarray) for k in key):
        key = [k.tolist() for k in key]
    # 检查key是否为空或者不是有效的密钥
    if not key:  # 如果 key 是空列表，直接判断列表是否为空
        return jsonify({"message": "未找到密钥"}), 200   # 返回404错误码表示未找到密钥
    return jsonify({"key": key})


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8050, debug=True)
