import re
import click

from hashlib import sha256
from binascii import hexlify, unhexlify


def base58encode(hex):
    alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
    hex_to_int = int(hex, 16) # convert to integer
    base_58 = ''

    # Loop through dividing by 58 and taking remainder as digit conversion
    while hex_to_int > 0:
        remainder = int(hex_to_int % 58)
        hex_to_int = hex_to_int // 58
        base_58 = f'{alphabet[remainder]}{base_58}'

    # Add leading 1 for every pair of leading 00s
    p = re.compile('^([0]+)')
    leading_zeros = int(p.match(hex).span()[-1] / 2)
    leading_ones = re.sub('.', lambda x: x.group() * leading_zeros, '1')
    base_58 = f'{leading_ones}{base_58}'

    return base_58


def checksum(hex):
    binary = unhexlify(hex)
    hash = sha256(binary).digest()
    return sha256(hash).hexdigest()[0:8]


@click.command()
@click.argument('hex')
def hash160_encode(hex, script='p2pkh'):
    # Leading digits to convert based on type of script
    prefixes = {
        'p2pkh': '00',
        'p2sh': '05',
        'p2pkh_testnet': '6F',
        'p2sh_testnet': 'C4'
    }

    prefix = prefixes[script]
    cs = checksum(prefix + hex)
    print(base58encode(prefix + hex + cs))


if __name__ == '__main__':
    hash160_encode()
