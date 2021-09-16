#FruitBrute

FruitBrute is a simple script that generates random seed phrases from english.txt, uses pywallet to generates BTC private keys, (bitcoinlib coming soon!), checks them against a csv containing public wallets containing positive balances and if it matches writes it to win.txt.

##Usage:

> python3 main.py

## Installation:
> pip install -r requirements.txt

## Preparation:
This repo contains a small sample csv file containing public BTC wallet addresses with positive balances. To generate a full (well, close) list check out graymauser's project:

[https://github.com/graymauser/btcposbal2csv)](https://github.com/graymauser/btcposbal2csv)


