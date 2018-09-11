from management.boxes import token_status
import random

BASE_ALPH = tuple("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")
BASE_DICT = dict((c, v) for v, c in enumerate(BASE_ALPH))
BASE_LEN = len(BASE_ALPH)

def decode(string):
    num = 0
    for char in string:
        num = num * BASE_LEN + BASE_DICT[char]
    return num

def encode(num):
    if not num:
        return BASE_ALPH[0]

    encoding = ""
    while num:
        num, rem = divmod(num, BASE_LEN)
        encoding = BASE_ALPH[rem] + encoding
    return encoding

def create_token(user_id):
    while True:
        value = random.randint(0,99999)
        token = encode(user_id * 10000000 + value)

        if token_status(token) == -1:
            return token

