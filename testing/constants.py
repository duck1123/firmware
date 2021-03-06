# (c) Copyright 2018 by Coinkite Inc. This file is part of Coldcard <coldcardwallet.com>
# and is covered by GPLv3 license found in COPYING.
#

SIM_PATH = '/tmp/ckcc-simulator.sock'

# Simulator normally powers up with this 'wallet'
simulator_fixed_xprv = "tprv8ZgxMBicQKsPeXJHL3vPPgTAEqQ5P2FD9qDeCQT4Cp1EMY5QkwMPWFxHdxHrxZhhcVRJ2m7BNWTz9Xre68y7mX5vCdMJ5qXMUfnrZ2si2X4"

simulator_fixed_words = "wife shiver author away frog air rough vanish fantasy frozen noodle athlete pioneer citizen symptom firm much faith extend rare axis garment kiwi clarify"

simulator_fixed_xfp = 0x4369050f

from ckcc_protocol.constants import AF_P2WSH, AFC_SCRIPT, AF_P2SH, AF_P2WSH_P2SH

unmap_addr_fmt = {
    'p2sh': AF_P2SH,
    'p2wsh': AF_P2WSH,
    'p2wsh-p2sh': AF_P2WSH_P2SH,
}

# all possible addr types, including multisig/scripts
ADDR_STYLES = ['p2wpkh', 'p2wsh', 'p2sh', 'p2pkh', 'p2wsh-p2sh', 'p2wpkh-p2sh']

# single-signer
ADDR_STYLES_SINGLE = ['p2wpkh', 'p2pkh', 'p2wpkh-p2sh']

# multi signer
ADDR_STYLES_MS = ['p2sh', 'p2wsh', 'p2wsh-p2sh']
