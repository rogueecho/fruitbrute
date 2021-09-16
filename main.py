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


def gen_mnemonic():
    seed = ''
    with open('english.txt' , 'r') as dic:
        wordlist = dic.readlines()
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
    addr = w['children'][0]['address']
    return priv, addr

def check_bal(addr):
    if addr in bal_dict:
        return bal_dict[addr]
    else:
        return 0
    return balance

def win(prv, addr, bal):
    with open("win.txt", "rw") as output:
        chicken_dinner = 'Priv: {} | Addr: {} | Bal: {}'.format(prv,addr,bal)
        f.write(chicken_dinner)

def main():
    print("Welcome to FruitBrute!")
    print("Ingesting CSV, please wait...")
    global bal_dict
    bal_dict = csv_to_dict('posbal.csv')
    while True:
        seed = gen_mnemonic()
#        blib_priv, pywallet_addr = get_bitcoinlib_key(seed)
        pywallet_priv, pywallet_addr = get_pywallet_key(seed)

#        if blib_priv and pywallet_addr:
            #Check for balances of both
            #If > 0, save off private key, addr, and balance

        if pywallet_priv and pywallet_addr:
            print('Trying {} : {}'.format(pywallet_priv ,pywallet_addr))
            balance = check_bal(pywallet_addr)
            if balance:
                print('Priv: {} | Addr: {} | Bal: {}'.format(pywallet_priv,pywallet_addr,str(balance)))
                win(pywallet_priv, pywallet_addr, str(balance))
            #Check for balances of both
            #If > 0, save off private key, addr, and balance


    return 0

if __name__ == "__main__":
    main()
