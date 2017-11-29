from p2pool.bitcoin import networks
from p2pool.util import math

# CHAIN_LENGTH = number of shares back client keeps
# REAL_CHAIN_LENGTH = maximum number of shares back client uses to compute payout
# REAL_CHAIN_LENGTH must always be <= CHAIN_LENGTH
# REAL_CHAIN_LENGTH must be changed in sync with all other clients
# changes can be done by changing one, then the other

nets = dict(

    groestlcoin=math.Object(
        PARENT=networks.nets['groestlcoin'],
        SHARE_PERIOD=15, # seconds
        CHAIN_LENGTH=24*60*60//15, # shares
        REAL_CHAIN_LENGTH=24*60*60//15, # shares
        TARGET_LOOKBEHIND=60, # shares  //with that the pools share diff is adjusting faster, important if huge hashing power comes to the pool
        SPREAD=30, # blocks
        IDENTIFIER='a15320ffb197c089'.decode('hex'),
        PREFIX='867c36a56116e81e'.decode('hex'),
        P2P_PORT=11331,
        MIN_TARGET=0,
        MAX_TARGET=2**256//2**20 - 1,
        PERSIST=False,
        WORKER_PORT=11330,
        BOOTSTRAP_ADDRS='74.71.249.124'.split(' '),
        ANNOUNCE_CHANNEL='#p2pool-grs',
        VERSION_CHECK=lambda v: True,
    ),

    groestlcoin_testnet=math.Object(
        PARENT=networks.nets['groestlcoin_testnet'],
        SHARE_PERIOD=15, # seconds
        CHAIN_LENGTH=24*60*60//15, # shares
        REAL_CHAIN_LENGTH=24*60*60//15, # shares
        TARGET_LOOKBEHIND=60, # shares  //with that the pools share diff is adjusting faster, important if huge hashing power comes to the pool
        SPREAD=30, # blocks
        IDENTIFIER='a15320ffb197c089'.decode('hex'),
        PREFIX='867c36a56116e81e'.decode('hex'),
        P2P_PORT=21331,
        MIN_TARGET=0,
        MAX_TARGET=2**256//2**20 - 1,
        PERSIST=False,
        WORKER_PORT=21330,
        BOOTSTRAP_ADDRS=''.split(' '),
        ANNOUNCE_CHANNEL='',
        VERSION_CHECK=lambda v: True,
    ),

)
for net_name, net in nets.iteritems():
    net.NAME = net_name
