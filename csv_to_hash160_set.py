import csv
import bz2
import pickle
from hashlib import sha256 
BASE58_ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
BASE58_ALPHABET_INDEX = {char: index for index, char in enumerate(BASE58_ALPHABET)}


def hex_to_bytes(hexed):
    if len(hexed) & 1:
        hexed = '0' + hexed
    return bytes.fromhex(hexed)

def int_to_unknown_bytes(num, byteorder='big'):
    """Converts an int to the least number of bytes as possible."""
    return num.to_bytes((num.bit_length() + 7) // 8 or 1, byteorder)

def double_sha256(bytestr):
    r = sha256(sha256(bytestr).digest()).digest()
    return r

def double_sha256_checksum(bytestr):
    r = double_sha256(bytestr)[:4]
    return r

def b58decode(string):
    alphabet_index = BASE58_ALPHABET_INDEX
    num = 0
    try:
        for char in string:
            num *= 58
            num += alphabet_index[char]
    except KeyError:
        raise ValueError('"{}" is an invalid base58 encoded '
                         'character.'.format(char)) from None
    bytestr = int_to_unknown_bytes(num)
    pad = 0
    for char in string:
        if char == '1':
            pad += 1
        else:
            break
    return b'\x00' * pad + bytestr

def b58decode_check(string):
    decoded = b58decode(string)
    shortened = decoded[:-4]
    decoded_checksum = decoded[-4:]
    hash_checksum = double_sha256_checksum(shortened)
    if decoded_checksum != hash_checksum:
        raise ValueError('Decoded checksum {} derived from "{}" is not equal to hash '
                         'checksum {}.'.format(decoded_checksum, string, hash_checksum))
    return shortened


with open('test.csv', newline='') as csvfile:
     spamreader = csv.reader(csvfile)
     hash160_list = []
     test_list = ['157RMZhbBLC1wucv3jxQqqHjbKezL1yy7g','1GL37AoxoUj45fPNYf8Dq5CTncyRYLqo7','3Q8dZUbatx5FC5CdQYRLg7gDnkQec5Pvp8','3JvL6Ymt8MVWiCNHC7oWU6nLeHNJKLZGLN'] # low entropy keys to test the sets
     for x in test_list:
         hash160 = b58decode_check(x)
         hash160_list.append(hash160[1:])
     for row in spamreader:
         try:
             address = row[0]
             amount  = int(row[1])
             hash160 = b58decode_check(address)
             hash160_list.append(hash160[1:])
         except Exception as e:
             print(e)
             continue

print("total_len",len(hash160_list))
new_list = [hash160_list[i:i+1000000] for i in range(0, len(hash160_list), 1000000)]
print("new_list",len(new_list))

file_num = 0
for x in new_list:
   f = bz2.BZ2File(f'{file_num}.set', 'wb')
   pickle.dump(set(x), f)
   file_num += 1
f.close()
