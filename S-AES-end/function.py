import numpy as np

# 构造状态矩阵 输入16位0/1数组
def stateMatConstruct(arr):
    arr = np.array(arr)
    S00 = arr[0:4]  # 取出前四个元素，代表状态矩阵的第一个部分
    S10 = arr[4:8]
    S01 = arr[8:12]
    S11 = arr[12:16]
    return [S00, S01, S10, S11] # 返回一个包含这四个部分的新列表


# 状态矩阵析构，转换回数组，状态矩阵重新组合成一个16位的数组
def stateMatDestorey(mat):
    # np.concatenate用于将多个数组沿指定轴连接起来。
    # mat[0] 是状态矩阵的第一个部分（S00），对应于矩阵的左上角。
    return np.concatenate([mat[0], mat[2], mat[1], mat[3]])


# 密钥加 输入16bit与密钥，做异或
def addKey(arr, key):
    arr = np.array(arr)
    key = np.array(key)
    res = np.bitwise_xor(arr, key)
    return res


# 半字节替代 S盒
def halfByteSubstitude(arr):
    indexDic = {(0, 0): 0, (0, 1): 1, (1, 0): 2, (1, 1): 3}
    # 定义了一个4x4的S盒矩阵 SBox.每个S盒包含四个数组，每个数组代表一个4位的输出。
    SBox = [
        [np.array([1, 0, 0, 1]), np.array([0, 1, 0, 0]), np.array([1, 0, 1, 0]), np.array([1, 0, 1, 1])],
        [np.array([1, 1, 0, 1]), np.array([0, 0, 0, 1]), np.array([1, 0, 0, 0]), np.array([0, 1, 0, 1])],
        [np.array([0, 1, 1, 0]), np.array([0, 0, 1, 0]), np.array([0, 0, 0, 0]), np.array([0, 0, 1, 1])],
        [np.array([1, 1, 0, 0]), np.array([1, 1, 1, 0]), np.array([1, 1, 1, 1]), np.array([0, 1, 1, 1])]
    ]
    # 将输入的16位数据 arr 分解成四个4位的部分，并组织成一个状态矩阵。
    mat = stateMatConstruct(arr)
    # 循环遍历状态矩阵的每个部分（共4个）
    # 对于每个部分，它使用 indexDic 来获取前两个比特和后两个比特的索引，然后使用这些索引来从 SBox 中查找对应的替换值。
    # 替换后的值被存储回状态矩阵 mat 中。
    for i in range(4):
        mat[i] = SBox[indexDic[tuple(mat[i][0:2])]][indexDic[tuple(mat[i][2:4])]]
    return stateMatDestorey(mat)

# 逆S盒
def inverseHalfByteSubstitude(arr):
    indexDic = {(0, 0): 0, (0, 1): 1, (1, 0): 2, (1, 1): 3}
    SBox = [
        [np.array([1, 0, 1, 0]), np.array([0, 1, 0, 1]), np.array([1, 0, 0, 1]), np.array([1, 0, 1, 1])],
        [np.array([0, 0, 0, 1]), np.array([0, 1, 1, 1]), np.array([1, 0, 0, 0]), np.array([1, 1, 1, 1])],
        [np.array([0, 1, 1, 0]), np.array([0, 0, 0, 0]), np.array([0, 0, 1, 0]), np.array([0, 0, 1, 1])],
        [np.array([1, 1, 0, 0]), np.array([0, 1, 0, 0]), np.array([1, 1, 0, 1]), np.array([1, 1, 1, 0])]
    ]
    mat = stateMatConstruct(arr)
    for i in range(4):
        mat[i] = SBox[indexDic[tuple(mat[i][0:2])]][indexDic[tuple(mat[i][2:4])]]
    return stateMatDestorey(mat)


# 行移位
def rowShift(arr):
    S00, S01, S10, S11 = stateMatConstruct(arr)
    # 第一行不变，第二行进行移位
    mat = [S00, S01, S11, S10]
    return stateMatDestorey(mat)


# 有限域乘法
def mulGF(a, b):
    # 不可约多项式: p(x) = x^4 + x + 1
    # 二进制表示
    irreducible = 0b10011
    # 正常多项式乘法
    result = 0
    # 计算 a * b 的多项式乘积
    # 对于 b 的每一位，如果这一位是1，则将 a 左移 i 位（相当于乘以 x^i）
    # 然后与 result 进行异或操作
    for i in range(4):
        if (b >> i) & 1:
            result ^= a << i
    # 模不可约多项式
    # 对 result 进行模 x^4 + x + 1 的运算
    # 它检查 result 的第5位到第8位（从右往左数，最低位为第0位）
    # 如果这些位中的任意一位是1，则将 irreducible 左移相应的位数
    # 然后与 result 进行异或操作
    for i in range(7, 3, -1):  # i依次取值7.6.5.4
        # 如果是1，说明 result 的第 i 位是1。则对不可约多项式进行右移
        if (result >> i) & 1:
            result ^= irreducible << (i - 4)
    return result & 0b1111


# 有限域矩阵乘法
def mulGFMat(mat1, mat2):
    result = [[0] * 2 for _ in range(2)]
    for i in range(2):
        for j in range(2):
            sum = 0
            for k in range(2):
                # 异或操作（^=）来累加这些乘积。
                sum ^= mulGF(int(''.join(map(str, mat1[i][k])), 2), int(''.join(map(str, mat2[k][j])), 2))
            result[i][j] = np.array(list(map(int, format(sum, '04b'))))
    return result


# 列混淆
def columnMix(arr):
    # [1 4]
    # [4 1]
    mixMat = [
        [np.array([0, 0, 0, 1]), np.array([0, 1, 0, 0])],
        [np.array([0, 1, 0, 0]), np.array([0, 0, 0, 1])],
    ]
    mat = stateMatConstruct(arr)
    mat = [
        [mat[0], mat[1]],
        [mat[2], mat[3]]
    ]
    result = mulGFMat(mixMat, mat)
    K = [item for sublist in result for item in sublist]
    return stateMatDestorey(K)


# 逆列混淆
def inverseColumnMix(arr):
    # [9 2]
    # [2 9]
    mixMat = [
        [np.array([1, 0, 0, 1]), np.array([0, 0, 1, 0])],
        [np.array([0, 0, 1, 0]), np.array([1, 0, 0, 1])],
    ]
    mat = stateMatConstruct(arr)
    mat = [
        [mat[0], mat[1]],
        [mat[2], mat[3]]
    ]
    result = mulGFMat(mixMat, mat)
    K = [item for sublist in result for item in sublist]
    return stateMatDestorey(K)


# 密钥扩展中函数g
def functionG(w, RCON):
    n0 = w[0:4]
    n1 = w[4:8]
    indexDic = {(0, 0): 0, (0, 1): 1, (1, 0): 2, (1, 1): 3}
    # 每个S盒包含四个数组，每个数组代表一个4位的输出。
    SBox = [
        [np.array([1, 0, 0, 1]), np.array([0, 1, 0, 0]), np.array([1, 0, 1, 0]), np.array([1, 0, 1, 1])],
        [np.array([1, 1, 0, 1]), np.array([0, 0, 0, 1]), np.array([1, 0, 0, 0]), np.array([0, 1, 0, 1])],
        [np.array([0, 1, 1, 0]), np.array([0, 0, 1, 0]), np.array([0, 0, 0, 0]), np.array([0, 0, 1, 1])],
        [np.array([1, 1, 0, 0]), np.array([1, 1, 1, 0]), np.array([1, 1, 1, 1]), np.array([0, 1, 1, 1])]
    ]
    n0 = SBox[indexDic[tuple(n0[0:2])]][indexDic[tuple(n0[2:4])]]
    n1 = SBox[indexDic[tuple(n1[0:2])]][indexDic[tuple(n1[2:4])]]
    w0 = np.concatenate([n1, n0])
    return np.bitwise_xor(w0, RCON)


# 生成密钥 密钥扩展
def generate_key(key):
    w0 = key[0:8]
    w1 = key[8:16]
    RCON1 = np.array([1, 0, 0, 0, 0, 0, 0, 0])
    RCON2 = np.array([0, 0, 1, 1, 0, 0, 0, 0])
    w2 = np.bitwise_xor(w0, functionG(w1, RCON1))
    w3 = np.bitwise_xor(w2, w1)
    w4 = np.bitwise_xor(w2, functionG(w3, RCON2))
    w5 = np.bitwise_xor(w4, w3)
    return np.concatenate([w0, w1]), np.concatenate([w2, w3]), np.concatenate([w4, w5])


# 加密算法
def encode(key, content):
    k1, k2, k3 = generate_key(key)
    content = np.array(content)
    content = addKey(
        rowShift(halfByteSubstitude(addKey(columnMix(rowShift(halfByteSubstitude(addKey(content, k1)))), k2))), k3)
    return content


# 解密
def decode(key, content):
    k1, k2, k3 = generate_key(key)
    content = np.array(content)
    content = addKey(inverseHalfByteSubstitude(
        rowShift(inverseColumnMix(addKey(inverseHalfByteSubstitude(rowShift(addKey(content, k3))), k2)))), k1)
    return content


# 双重加密
def doubleEncode(key, content):
    firstKey = key[0:16]
    lastKey = key[16:32]
    # 以新密钥加密 用第一次密钥加密明文得到的密文
    return encode(lastKey, encode(firstKey, content))


# 双重解密
def doubleDecode(key, content):
    firstKey = key[0:16]
    lastKey = key[16:32]
    return decode(firstKey, decode(lastKey, content))


# 三重加密
def tripleEncode(key, content):
    firstKey = key[0:16]
    lastKey = key[16:32]
    return encode(firstKey, decode(lastKey, encode(firstKey, content)))


# 三重解密
def tripleDecode(key, content):
    firstKey = key[0:16]
    lastKey = key[16:32]
    return decode(firstKey, encode(lastKey, decode(firstKey, content)))


# 字符串转为二进制数组
def string_change(string):
    def int_to_16bit_bin_array(num):
        return np.array([int(b) for b in format(num, '016b')])

    def string_to_bin_arrays(s):
        return [int_to_16bit_bin_array(ord(c)) for c in s]

    arr = string_to_bin_arrays(string)
    arr = [np.array(list(c)) for c in arr]
    arr = [c.astype(int) for c in arr]
    return arr


# 加密字符串
def encode_str(key, string):
    # 将输入的字符串 string 转换为一个二进制数组 arr
    arr = string_change(string)
    # 对每个元素应用 encode 函数，使用密钥 key 进行加密
    en_arr = [encode(key, c) for c in arr]
    # 将 en_arr 中的每个元素（目前是NumPy数组）转换为字符串形式
    en_arr = [c.astype(str) for c in en_arr]
    # 将 en_arr 中的每个字符串元素（由二进制数字组成）转换为没有空格的连续字符串
    en_arr = [''.join(c.tolist()) for c in en_arr]
    # 将 en_arr 中的每个二进制字符串转换为对应的十进制整数。
    # int(c, 2) 表示将字符串 c 作为二进制数解析。
    en_arr = [int(c, 2) for c in en_arr]
    # 将 en_arr 中的每个十进制整数转换为对应的字符
    encoded_string = ''.join([chr(i) for i in en_arr])
    return encoded_string


# 解密字符串
def decode_str(key, string):
    arr = string_change(string)
    de_arr = [decode(key, c) for c in arr]
    de_arr = [c.astype(str) for c in de_arr]
    de_arr = [''.join(c.tolist()) for c in de_arr]
    de_arr = [int(c, 2) for c in de_arr]
    decoded_string = ''.join([chr(i) for i in de_arr])
    return decoded_string


# CBC加密字符串
def encodeCBCString(key, string):
    IV = np.array([1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1])
    arr = string_change(string)
    en_arr = []
    for i in range(len(arr)):
        temp = np.bitwise_xor(arr[i], IV)
        IV = encode(key, temp)
        # en_arr 最终包含了所有加密块的序列
        en_arr.append(IV)
    en_arr = [c.astype(str) for c in en_arr]
    en_arr = [''.join(c.tolist()) for c in en_arr]
    en_arr = [int(c, 2) for c in en_arr]
    encoded_string = ''.join([chr(i) for i in en_arr])
    return encoded_string


# CBC解密字符串
def decodeCBCString(key, string):
    firstIV = np.array([1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1])
    arr = string_change(string)
    arr.reverse()
    de_arr = []
    for i in range(len(arr)):
        if i != len(arr) - 1:
            IV = arr[i + 1]
        else:
            IV = firstIV
        temp = decode(key, arr[i])
        temp = np.bitwise_xor(temp, IV)
        de_arr.append(temp)
    de_arr.reverse()
    de_arr = [c.astype(str) for c in de_arr]
    de_arr = [''.join(c.tolist()) for c in de_arr]
    de_arr = [int(c, 2) for c in de_arr]
    decoded_string = ''.join([chr(i) for i in de_arr])
    return decoded_string


# 相遇攻击破解双重加密
def Meet_in_the_Middle (ciphertext, plaintext):
    possible_keys = []
    midTextA = {}
    midTextB = {}

    # 对每一个可能的keyA, 加密明文并存储中间结果
    for key in range(2 ** 16):
        # 将整数密钥转换为16位的二进制数组 binary_key
        binary_key = np.array([int(b) for b in format(key, '016b')])
        # 加密得到中间结果
        encoded_text = encode(binary_key, plaintext)
        # 将 encoded_text 作为键，binary_key 作为值，存储在字典 midTextA 中。
        midTextA[tuple(encoded_text)] = binary_key

    # 对每一个可能的keyB, 解密密文并存储中间结果
    for key in range(2 ** 16):
        binary_key = np.array([int(b) for b in format(key, '016b')])
        # 使用 decode 函数和 keyB 对密文 ciphertext 进行解密，得到中间结果 decoded_text。
        decoded_text = decode(binary_key, ciphertext)
        # 将 decoded_text 作为键，binary_key 作为值，存储在字典 midTextB 中。
        midTextB[tuple(decoded_text)] = binary_key

    # 循环遍历字典 midTextA 的所有键，对于每个键检查该键是否也存在于字典 midTextB 中
    # 如果存在，说明找到了一个匹配的中间结果，将对应的两个密钥 keyA 和 keyB 拼接起来，添加到列表 possible_keys 中
    for encoded_text_str in midTextA.keys():
        if encoded_text_str in midTextB.keys():
            possible_keys.append(np.concatenate([midTextA.get(encoded_text_str), midTextB.get(encoded_text_str)]))

    return possible_keys


if __name__ == '__main__':
    pass
    # print(string_change('asdasdasd'))
    # k = brute_force_sdes([0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0],
    #                      [1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0]
    #                      )
    #
    # print(encode_str([1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0], 'HelloWorld'))
    # print(encodeCBCString([1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0], 'HelloWorld'))
    # print(doubleDecode([1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0],
    #                    [0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0]))
    # [0 1 0 0 1 1 1 0 0 0 1 0 1 0 0 0]
    # [1 0 0 0 1 0 1 0 0 0 0 1 1 1 0 0]
    # print(encode([0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0],
    #              encode([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #                     [1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0])))
    # [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0]
    # [1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0]
    # 0    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    # 1    (0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0)
    # 2    (0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0)
    # 3    (1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0)
    # 4    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0)
    # Name: key1, dtype: object
    # 0    (0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0)
    # 1    (0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1)
    # 2    (1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0)
    # 3    (1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0)
    # 4    (0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0)
    # Name: key2, dtype: object

    # x = [1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0]
    # print(rowShift(halfByteSubstitude(x)))
    # print(columnMix(rowShift(halfByteSubstitude(x))))
    # print(generate_key([0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]))
    # print(encode([1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0], [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]))
    # print(decode([1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0], [1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0]))