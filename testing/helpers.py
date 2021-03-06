# (c) Copyright 2018 by Coinkite Inc. This file is part of Coldcard <coldcardwallet.com>
# and is covered by GPLv3 license found in COPYING.
#
# stuff I need sometimes
from io import BytesIO
from binascii import b2a_hex
from decimal import Decimal
import random

def B2A(s):
    return str(b2a_hex(s), 'ascii')
    
def U2SAT(v):
    return int(v * Decimal('1E8'))

# use like this:
#
#       with into_hex() as a:
#           a.write('sdlkfjsdflkj')
#
# ... will print hex of whatever was streamed.
#
class into_hex(BytesIO):
    def __exit__(self, *a):
        print('hex: %s' % str(b2a_hex(self.getvalue()), 'ascii'))
        return super().__exit__(*a)

'''
    >>> from binascii import *
    >>> from helpers import into_hex
    >>> from pycoin.tx.Tx import Tx
    >>> t = Tx.from_hex('010000....')
    >>> with into_hex() as fd:
    >>>     t.txs_out[0].stream(fd)
'''

def dump_txos(hx, out_num=0):
    from binascii import b2a_hex
    from helpers import into_hex
    from pycoin.tx.Tx import Tx

    t = Tx.from_hex(hx)
    with into_hex() as fd:
        t.txs_out[out_num].stream(fd)

    print('hash160: %s' % b2a_hex(t.txs_out[out_num].hash160()))

    return t

def prandom(count):
    # make some bytes, randomly, but not: deterministic
    return bytes(random.randint(0, 255) for i in range(count))

def fake_dest_addr(style='p2pkh'):
    # Make a plausible output address, but it's random garbage. Cant use for change outs

    # See CTxOut.get_address() in ../shared/serializations

    if style == 'p2wpkh':
        return bytes([0, 20]) + prandom(20)

    if style == 'p2wsh':
        return bytes([0, 32]) + prandom(32)

    if style in ['p2sh', 'p2wsh-p2sh', 'p2wpkh-p2sh']:
        # all equally bogus P2SH outputs
        return bytes([0xa9, 0x14]) + prandom(20) + bytes([0x87])

    if style == 'p2pkh':
        return bytes([0x76, 0xa9, 0x14]) + prandom(20) + bytes([0x88, 0xac])

    # missing: if style == 'p2pk' =>  pay to pubkey, considered obsolete

    raise ValueError('not supported: ' + style)

def make_change_addr(wallet, style):
    # provide script, pubkey and xpath for a legit-looking change output
    import struct, random
    from pycoin.encoding import hash160

    redeem_scr, actual_scr = None, None
    deriv = [12, 34, random.randint(0, 1000)]

    xfp, = struct.unpack('I', wallet.fingerprint())

    dest = wallet.subkey_for_path('/'.join(str(i) for i in deriv))

    target = dest.hash160()
    assert len(target) == 20

    is_segwit = False
    if style == 'p2pkh':
        redeem_scr = bytes([0x76, 0xa9, 0x14]) + target + bytes([0x88, 0xac])
    elif style == 'p2wpkh':
        redeem_scr = bytes([0, 20]) + target
        is_segwit = True
    elif style == 'p2wpkh-p2sh':
        redeem_scr = bytes([0, 20]) + target
        actual_scr = bytes([0xa9, 0x14]) + hash160(redeem_scr) + bytes([0x87])
    else:
        raise ValueError('cant make fake change output of type: ' + style)

    return redeem_scr, actual_scr, is_segwit, dest.sec(), struct.pack('4I', xfp, *deriv)

def swab32(n):
    # endian swap: 32 bits
    import struct
    return struct.unpack('>I', struct.pack('<I', n))[0]

def xfp2str(xfp):
    # Standardized way to show an xpub's fingerprint... it's a 4-byte string
    # and not really an integer. Used to show as '0x%08x' but that's wrong endian.
    from binascii import b2a_hex
    from struct import pack
    return b2a_hex(pack('<I', xfp)).decode('ascii').upper()

# EOF
