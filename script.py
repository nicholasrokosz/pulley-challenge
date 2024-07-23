import requests
import re
import ast
import binascii


def fetch_challenge(path):
    response = requests.get("https://ciphersprint.pulley.com/" + path)
    json_response = response.json()
    return json_response

def decrypt_path(path, method):
    method = method
    return path

def level_one(path):
    str_arr = re.search(r'\[.*?\]', path).group()
    arr = ast.literal_eval(str_arr)
    str = ''.join(list(map(lambda n: chr(n), arr)))
    return 'task_' + str

def level_two(path):
    hex_only_string = re.sub(r'[^0-9a-fA-F]', '', path[5:])
    # print(hex_only_string)
    return 'task_' + hex_only_string

def level_three(path, n):
    str = path[5:]
    rotated_str = str[-n:] + str[:-n]
    return 'task_' + rotated_str

def xor_decrypt(data, key):
    key_bytes = key.encode()
    return bytes([data[i] ^ key_bytes[i % len(key_bytes)] for i in range(len(data))])

def level_four(path):
    str = path[5:]
    hex_decoded = binascii.unhexlify(str)
    xor_decrypted = xor_decrypt(hex_decoded, "secret")
    result = binascii.hexlify(xor_decrypted).decode()
    print(result)
    return 'task_' + result



level = 0
hint_path = "nicholasrokosz@gmail.com"

while level < 6:
    # print(level)
    challenge_info = fetch_challenge(hint_path)
    print(challenge_info)

    hint_path = challenge_info['encrypted_path']

    if level == 1:
        hint_path = level_one(hint_path)
    if level == 2:
        hint_path = level_two(hint_path)
    if level == 3:
        n = int(re.search(r'\d+', challenge_info['encryption_method']).group())
        hint_path = level_three(hint_path, n)
    if level == 4:
        hint_path = level_four(hint_path)

    level = challenge_info['level'] + 1
