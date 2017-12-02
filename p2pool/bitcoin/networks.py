import os
import platform

from twisted.internet import defer

from . import data
from p2pool.util import math, pack, jsonrpc

@defer.inlineCallbacks
def check_genesis_block(bitcoind, genesis_block_hash):
    try:
        yield bitcoind.rpc_getblock(genesis_block_hash)
    except jsonrpc.Error_for_code(-5):
        defer.returnValue(False)
    else:
        defer.returnValue(True)

nets = dict(

    groestlcoin=math.Object(
        P2P_PREFIX='f9beb4d4'.decode('hex'),
        P2P_PORT=1331,
        ADDRESS_VERSION=36,
        RPC_PORT=1441,
        RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
            'groestlcoinaddress' in (yield bitcoind.rpc_help()) and
            not (yield bitcoind.rpc_getinfo())['testnet']
        )),
        SUBSIDY_FUNC=lambda nBits, height: __import__('groestlcoin_subsidy').getBlockBaseValue(nBits, height+1),
        POW_FUNC=lambda data: pack.IntType(256).unpack(__import__('groestlcoin_hash').getHash(data, 80)),
        BLOCK_PERIOD=60, # s
        SYMBOL='GRS',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'Groestlcoin') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/Groestlcoin/') if platform.system() == 'Darwin' else os.path.expanduser('~/.groestlcoin'), 'groestlcoin.conf'),
        BLOCK_EXPLORER_URL_PREFIX='http://chainz.cryptoid.info/grs/block.dws?',
        ADDRESS_EXPLORER_URL_PREFIX='http://chainz.cryptoid.info/grs/address.dws?',
        TX_EXPLORER_URL_PREFIX='http://chainz.cryptoid.info/grs/tx.dws?',
        SANE_TARGET_RANGE=(2**256//2**32//1000 - 1, 2**256//2**20 - 1),
        DUMB_SCRYPT_DIFF=256,
        DUST_THRESHOLD=0.001e8,
    ),

    groestlcoin_testnet=math.Object(
        P2P_PREFIX='0b110907'.decode('hex'),
        P2P_PORT=17777,
        ADDRESS_VERSION=111,
        RPC_PORT=17766,
        RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
            'GroestlCoinaddress' in (yield bitcoind.rpc_help()) and
            (yield bitcoind.rpc_getinfo())['testnet']
        )),
        SUBSIDY_FUNC=lambda nBits, height: __import__('groestlcoin_subsidy').getBlockBaseValue(nBits, height+1),
        POW_FUNC=lambda data: pack.IntType(256).unpack(__import__('groestlcoin_hash').getHash(data, 80)),
        BLOCK_PERIOD=60, # s
        SYMBOL='GRS',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'Groestlcoin') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/Groestlcoin/') if platform.system() == 'Darwin' else os.path.expanduser('~/.groestlcoin'), 'groestlcoin.conf'),
        BLOCK_EXPLORER_URL_PREFIX='',
        ADDRESS_EXPLORER_URL_PREFIX='',
        TX_EXPLORER_URL_PREFIX='',
        SANE_TARGET_RANGE=(2**256//2**32//1000 - 1, 2**256//2**20 - 1),
        DUMB_SCRYPT_DIFF=256,
        DUST_THRESHOLD=0.001e8,
    ),

)
for net_name, net in nets.iteritems():
    net.NAME = net_name
