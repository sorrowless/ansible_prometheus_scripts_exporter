#!/usr/bin/python3

import json
import requests
import sys

usage = """
Usage:
    check-bitcoin-sync.py <blockchainApiUrl> <localBtcUrl> [<rpcuser> <rpcpassword>]

where:
    blockchainApiUrl is an URL to blockchain.info
    localBtcUrl is an URL to local bitcoind instance like
                     http://localhost:18332
"""

if len(sys.argv) < 2:
    print(usage)
    sys.exit(2)

# Getting local block number
local_btc_url = sys.argv[2]
payload = '{"jsonrpc":"1.0","id":"curltext","method":"getblockcount","params":[]}'  # noqa
headers = {'Content-Type': 'text/plain'}
try:
    if len(sys.argv) < 4:
        r = requests.post(local_btc_url, data=payload, headers=headers)
    else:
        rpcuser = sys.argv[3]
        rpcpassword = sys.argv[4]
        r = requests.post(local_btc_url, data=payload, headers=headers, auth=(rpcuser,rpcpassword))
    local_bnum = int(r.json()['result'])
except:
    local_bnum = -1

# Getting remote block number
remote_btc_url = sys.argv[1]

try:
    r = requests.get(remote_btc_url)
    remote_bnum = int(r.json()['height'])
except:
    remote_bnum = -1

print(json.dumps(
    {"local_blocknumber": local_bnum, "remote_blocknumber": remote_bnum}))
