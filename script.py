import requests
import re
import json
import ast


def fetch_challenge(path):
    response = requests.get("https://ciphersprint.pulley.com/" + path)
    json_response = response.json()
    return json_response

def decrypt_path(path, method):
    method = method
    return path

def level_one(path):
    str_arr = re.search(r'\[.*?\]', path).group()
    arr = eval(str_arr)
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

level = 0
hint_path = "nicholasrokosz@gmail.com"

while level < 5:
    # print(level)
    challenge_info = fetch_challenge(hint_path)
    print(challenge_info)

    hint_path = challenge_info['encrypted_path']

    if level == 1:
        hint_path = level_one(hint_path)
    if level == 2:
        hint_path = level_two(hint_path)
        # level_two(hint_path)
    if level == 3:
        n = int(re.search(r'\d+', challenge_info['encryption_method']).group())
        # print(n)
        hint_path = level_three(hint_path, n)

    level = challenge_info['level'] + 1

# response = requests.get(URL + "/nicholasrokosz@gmail.com")
# json = response.json()
# hint_path = json['encrypted_path']
# next_response = requests.get(URL + hint_path)
# hint_path = re.search(r'/\S+', json['hint']).group()

# print(f"Response content: {response.text}")
# print(f"Next response content: {next_response.text}")
# print(hint_path)
