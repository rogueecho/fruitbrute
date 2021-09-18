#!/usr/bin/env python3

# This script randomly selects seed words from english.txt (used by pywallet and bitcoinlib),
# it then generates a wallet, checks the public address against a CSV of positive-balance wallets
# and returns the private key, public wallet address, and balance if found
# CSV generated using https://github.com/graymauser/btcposbal2csv and too large to host on github, sorry!

import requests
import random
import time
import pandas as pd
#from bitcoinlib.wallets import Wallet, wallet_delete
#from bitcoinlib.mnemonic import Mnemonic
from pywallet import wallet


def gen_mnemonic(wordlist):
    seed = ''
        for i in range(0,11):
            seed += random.choice(wordlist).rstrip() + " "
        seed += random.choice(wordlist).rstrip()
    return seed

#bitcoinlib does some form of entropy checking so I can't force it a weakly randomized seed. GOOD!
#def get_bitcoinlib_key(seed):
#    also_seed = Mnemonic().to_seed(seed)
#    try: 
#        w = Wallet.create("whatever", keys=also_seed, network='bitcoin')
#    
#    except ValueError:
#        return False, False
#    priv = w.get_key().wif
#    return priv, addr

def csv_to_dict(csvfile):
    df = pd.read_csv(csvfile)
    output = df.to_dict()
    return output


def get_pywallet_key(seed):
    w = wallet.create_wallet(network="BTC", seed=seed, children=1)
    priv = w['private_key']
    # Check wallet addr and 1-deep child addr because I have no idea how child wallets work
    # TO DO: Figure out how child wallets work
    addr1 = w['address']
    addr2 = w['children'][0]['address']
    addrs = [addr1, addr2]
    return priv, addrs

def check_bal(addr, bal_dict):
    if addr in bal_dict:
        return bal_dict[addr]
    else:
        return 0
    yield balance

def win(prv, addr, bal):
    with open("win.txt", "rw") as output:
        chicken_dinner = 'Priv: {} | Addr: {} | Bal: {}'.format(prv,addr,bal)
        f.write(chicken_dinner)

def main():
    print("Welcome to FruitBrute!")
    print("Ingesting CSV, please wait...")
    bal_dict = csv_to_dict('posbal.csv')
    while True:
        with open('english.txt' , 'r') as dic:
            wordlist = dic.readlines()
        seed = gen_mnemonic(wordlist)
#        blib_priv, pywallet_addr = get_bitcoinlib_key(seed)
        pywallet_priv, pywallet_addrs = get_pywallet_key(seed)

            #Check for balances of both
            #If > 0, save off private key, addr, and balance

        if pywallet_priv and pywallet_addrs:
            for pywallet_addr in pywallet_addrs:
                print('Trying {} : {}'.format(pywallet_priv ,pywallet_addr))
                if pywallet_addr in bal_dict:
                    balance = check_bal(pywallet_addr, bal_dict)
                    if balance:
                        print('Priv: {} | Addr: {} | Bal: {}'.format(pywallet_priv,pywallet_addr,str(balance)))
                        win(pywallet_priv, pywallet_addr, str(balance))

    return 0

if __name__ == "__main__":
    main()

