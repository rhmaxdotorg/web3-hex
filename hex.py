#!/usr/bin/python3
#
# hex.py web3 stats app
#

import os
import sys
import json
import urllib.request
import web3
from web3 import Web3

#
# config
#
API_KEY = "ADD-YOUR-KEY-HERE"
RPC_URL = "https://mainnet.infura.io/v3" + "/" + API_KEY

#
# defs
#
HEX_ADD = "0x2b591e99afE9f32eAA6214f7B7629768c40Eeb39"
HEX_ABI  = [{"inputs":[],"payable":False,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"owner","type":"address"},{"indexed":True,"internalType":"address","name":"spender","type":"address"},{"indexed":False,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"uint256","name":"data0","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"data1","type":"uint256"},{"indexed":True,"internalType":"bytes20","name":"btcAddr","type":"bytes20"},{"indexed":True,"internalType":"address","name":"claimToAddr","type":"address"},{"indexed":True,"internalType":"address","name":"referrerAddr","type":"address"}],"name":"Claim","type":"event"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"uint256","name":"data0","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"data1","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"data2","type":"uint256"},{"indexed":True,"internalType":"address","name":"senderAddr","type":"address"}],"name":"ClaimAssist","type":"event"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"uint256","name":"data0","type":"uint256"},{"indexed":True,"internalType":"address","name":"updaterAddr","type":"address"}],"name":"DailyDataUpdate","type":"event"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"uint256","name":"data0","type":"uint256"},{"indexed":True,"internalType":"uint40","name":"stakeId","type":"uint40"}],"name":"ShareRateChange","type":"event"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"uint256","name":"data0","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"data1","type":"uint256"},{"indexed":True,"internalType":"address","name":"stakerAddr","type":"address"},{"indexed":True,"internalType":"uint40","name":"stakeId","type":"uint40"}],"name":"StakeEnd","type":"event"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"uint256","name":"data0","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"data1","type":"uint256"},{"indexed":True,"internalType":"address","name":"stakerAddr","type":"address"},{"indexed":True,"internalType":"uint40","name":"stakeId","type":"uint40"},{"indexed":True,"internalType":"address","name":"senderAddr","type":"address"}],"name":"StakeGoodAccounting","type":"event"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"uint256","name":"data0","type":"uint256"},{"indexed":True,"internalType":"address","name":"stakerAddr","type":"address"},{"indexed":True,"internalType":"uint40","name":"stakeId","type":"uint40"}],"name":"StakeStart","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"from","type":"address"},{"indexed":True,"internalType":"address","name":"to","type":"address"},{"indexed":False,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"uint256","name":"data0","type":"uint256"},{"indexed":True,"internalType":"address","name":"memberAddr","type":"address"},{"indexed":True,"internalType":"uint256","name":"entryId","type":"uint256"},{"indexed":True,"internalType":"address","name":"referrerAddr","type":"address"}],"name":"XfLobbyEnter","type":"event"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"uint256","name":"data0","type":"uint256"},{"indexed":True,"internalType":"address","name":"memberAddr","type":"address"},{"indexed":True,"internalType":"uint256","name":"entryId","type":"uint256"},{"indexed":True,"internalType":"address","name":"referrerAddr","type":"address"}],"name":"XfLobbyExit","type":"event"},{"payable":True,"stateMutability":"payable","type":"fallback"},{"constant":True,"inputs":[],"name":"allocatedSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":False,"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":True,"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":False,"inputs":[{"internalType":"uint256","name":"rawSatoshis","type":"uint256"},{"internalType":"bytes32[]","name":"proof","type":"bytes32[]"},{"internalType":"address","name":"claimToAddr","type":"address"},{"internalType":"bytes32","name":"pubKeyX","type":"bytes32"},{"internalType":"bytes32","name":"pubKeyY","type":"bytes32"},{"internalType":"uint8","name":"claimFlags","type":"uint8"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"},{"internalType":"uint256","name":"autoStakeDays","type":"uint256"},{"internalType":"address","name":"referrerAddr","type":"address"}],"name":"btcAddressClaim","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":True,"inputs":[{"internalType":"bytes20","name":"","type":"bytes20"}],"name":"btcAddressClaims","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[{"internalType":"bytes20","name":"btcAddr","type":"bytes20"},{"internalType":"uint256","name":"rawSatoshis","type":"uint256"},{"internalType":"bytes32[]","name":"proof","type":"bytes32[]"}],"name":"btcAddressIsClaimable","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[{"internalType":"bytes20","name":"btcAddr","type":"bytes20"},{"internalType":"uint256","name":"rawSatoshis","type":"uint256"},{"internalType":"bytes32[]","name":"proof","type":"bytes32[]"}],"name":"btcAddressIsValid","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":False,"stateMutability":"pure","type":"function"},{"constant":True,"inputs":[{"internalType":"address","name":"claimToAddr","type":"address"},{"internalType":"bytes32","name":"claimParamHash","type":"bytes32"},{"internalType":"bytes32","name":"pubKeyX","type":"bytes32"},{"internalType":"bytes32","name":"pubKeyY","type":"bytes32"},{"internalType":"uint8","name":"claimFlags","type":"uint8"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"claimMessageMatchesSignature","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":False,"stateMutability":"pure","type":"function"},{"constant":True,"inputs":[],"name":"currentDay","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"dailyData","outputs":[{"internalType":"uint72","name":"dayPayoutTotal","type":"uint72"},{"internalType":"uint72","name":"dayStakeSharesTotal","type":"uint72"},{"internalType":"uint56","name":"dayUnclaimedSatoshisTotal","type":"uint56"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[{"internalType":"uint256","name":"beginDay","type":"uint256"},{"internalType":"uint256","name":"endDay","type":"uint256"}],"name":"dailyDataRange","outputs":[{"internalType":"uint256[]","name":"list","type":"uint256[]"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":False,"inputs":[{"internalType":"uint256","name":"beforeDay","type":"uint256"}],"name":"dailyDataUpdate","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":True,"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":False,"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":True,"inputs":[],"name":"globalInfo","outputs":[{"internalType":"uint256[13]","name":"","type":"uint256[13]"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"globals","outputs":[{"internalType":"uint72","name":"lockedHeartsTotal","type":"uint72"},{"internalType":"uint72","name":"nextStakeSharesTotal","type":"uint72"},{"internalType":"uint40","name":"shareRate","type":"uint40"},{"internalType":"uint72","name":"stakePenaltyTotal","type":"uint72"},{"internalType":"uint16","name":"dailyDataCount","type":"uint16"},{"internalType":"uint72","name":"stakeSharesTotal","type":"uint72"},{"internalType":"uint40","name":"latestStakeId","type":"uint40"},{"internalType":"uint128","name":"claimStats","type":"uint128"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":False,"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":True,"inputs":[{"internalType":"bytes32","name":"merkleLeaf","type":"bytes32"},{"internalType":"bytes32[]","name":"proof","type":"bytes32[]"}],"name":"merkleProofIsValid","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":False,"stateMutability":"pure","type":"function"},{"constant":True,"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[{"internalType":"bytes32","name":"pubKeyX","type":"bytes32"},{"internalType":"bytes32","name":"pubKeyY","type":"bytes32"},{"internalType":"uint8","name":"claimFlags","type":"uint8"}],"name":"pubKeyToBtcAddress","outputs":[{"internalType":"bytes20","name":"","type":"bytes20"}],"payable":False,"stateMutability":"pure","type":"function"},{"constant":True,"inputs":[{"internalType":"bytes32","name":"pubKeyX","type":"bytes32"},{"internalType":"bytes32","name":"pubKeyY","type":"bytes32"}],"name":"pubKeyToEthAddress","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":False,"stateMutability":"pure","type":"function"},{"constant":True,"inputs":[{"internalType":"address","name":"stakerAddr","type":"address"}],"name":"stakeCount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":False,"inputs":[{"internalType":"uint256","name":"stakeIndex","type":"uint256"},{"internalType":"uint40","name":"stakeIdParam","type":"uint40"}],"name":"stakeEnd","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":False,"inputs":[{"internalType":"address","name":"stakerAddr","type":"address"},{"internalType":"uint256","name":"stakeIndex","type":"uint256"},{"internalType":"uint40","name":"stakeIdParam","type":"uint40"}],"name":"stakeGoodAccounting","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":True,"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"uint256","name":"","type":"uint256"}],"name":"stakeLists","outputs":[{"internalType":"uint40","name":"stakeId","type":"uint40"},{"internalType":"uint72","name":"stakedHearts","type":"uint72"},{"internalType":"uint72","name":"stakeShares","type":"uint72"},{"internalType":"uint16","name":"lockedDay","type":"uint16"},{"internalType":"uint16","name":"stakedDays","type":"uint16"},{"internalType":"uint16","name":"unlockedDay","type":"uint16"},{"internalType":"bool","name":"isAutoStake","type":"bool"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":False,"inputs":[{"internalType":"uint256","name":"newStakedHearts","type":"uint256"},{"internalType":"uint256","name":"newStakedDays","type":"uint256"}],"name":"stakeStart","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":True,"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":False,"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":False,"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":True,"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"xfLobby","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":False,"inputs":[{"internalType":"address","name":"referrerAddr","type":"address"}],"name":"xfLobbyEnter","outputs":[],"payable":True,"stateMutability":"payable","type":"function"},{"constant":True,"inputs":[{"internalType":"address","name":"memberAddr","type":"address"},{"internalType":"uint256","name":"entryId","type":"uint256"}],"name":"xfLobbyEntry","outputs":[{"internalType":"uint256","name":"rawAmount","type":"uint256"},{"internalType":"address","name":"referrerAddr","type":"address"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":False,"inputs":[{"internalType":"uint256","name":"enterDay","type":"uint256"},{"internalType":"uint256","name":"count","type":"uint256"}],"name":"xfLobbyExit","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":False,"inputs":[],"name":"xfLobbyFlush","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":True,"inputs":[{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"address","name":"","type":"address"}],"name":"xfLobbyMembers","outputs":[{"internalType":"uint40","name":"headIndex","type":"uint40"},{"internalType":"uint40","name":"tailIndex","type":"uint40"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[{"internalType":"address","name":"memberAddr","type":"address"}],"name":"xfLobbyPendingDays","outputs":[{"internalType":"uint256[2]","name":"words","type":"uint256[2]"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[{"internalType":"uint256","name":"beginDay","type":"uint256"},{"internalType":"uint256","name":"endDay","type":"uint256"}],"name":"xfLobbyRange","outputs":[{"internalType":"uint256[]","name":"list","type":"uint256[]"}],"payable":False,"stateMutability":"view","type":"function"}]

HEX_USD = "0x69d91b94f0aaf8e8a2586909fa77a5c2c89818d5" # hex/usdc pool
DEX_URL = "https://api.dexscreener.com/latest/dex/pairs/ethereum/" + HEX_USD

#
# get a connection to infura node
#
def getWeb3():
    w3 = None

    try:
        w3 = Web3(Web3.HTTPProvider(RPC_URL))
    except Exception as error:
        print("- %s\n" % error)

    return w3

#
# setup contract address
#
def getContract(w3, address, abi):
    contract = None

    try:
        contract = w3.eth.contract(address=address, abi=abi)
    except Exception as error:
        print("- %s\n" % error)

    return contract

#
# get globalInfo from contract
#
def getGlobalInfo(contract):
    info = None

    try:
        info = contract.functions.globalInfo()
    except Exception as error:
        print("- %s\n" % error)

    return info

#
# get stats from contract info
#
def printHexStats(contract, info):
    name   = contract.functions.name().call()
    dec    = contract.functions.decimals().call()
    supply = contract.functions.totalSupply().call() / 10**dec

    shareRate        = info.call()[2] / 10
    stakeSharesTotal = info.call()[5] / 1000000000000

    print("name:             %s" % name)
    print("decimals:         %d" % dec)
    print("totalSupply:      %d" % supply)
    print("shareRate:        %d" % shareRate)
    print("stakeSharesTotal: %d\n" % stakeSharesTotal)

    #
    # dexscreener whitelists anvil app, so this works there but otherwise we get
    # a 403 probably because we need an API key here too -- code left for reference
    #

    # currentPrice = "unknown"

    # try:
    #     currentPrice = float(urllib.request.urlopen(DEX_URL).read()['pair']['priceUsd'])
    # except Exception as error:
    #     print("- %s\n" % error)

    # print("price:            {:0.3f}\n".format(currentPrice))

#
# main function
#
def main():
    w3 = getWeb3()

    if(w3 == None):
        return

    if not w3.isConnected():
        print("- web3 could not connect to %s with API_KEY" % RPC_URL)
        return

    print("+ successfully connected to the blockchain")

    contract = getContract(w3, HEX_ADD, HEX_ABI)

    if(contract == None):
        return

    print("+ ready to talk to the contract\n")

    info = getGlobalInfo(contract)

    if(info == None):
        return

    printHexStats(contract, info)

    return

if(__name__ == '__main__'):
	main()
