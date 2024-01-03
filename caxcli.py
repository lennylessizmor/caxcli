"""CLI for the Piccadilly CAX.

Usage:
  caxcli list [options]
  caxcli depth <pair> [options]
  caxcli (bid|ask) <pair> <price> <amount>
  caxcli cancel <order_id>
  caxcli withdraw <symbol> <amount>

Options:
  -h --help          Show this screen.
  --version          Show version.
  --json             Print raw json (don't format anything).
  --timeout=<N>      How many seconds to wait for CAX response [default: 5].
  --deposits         List all user deposits.
  --withdraws        List all user withdraws.
  --balances         List all user balances.
  --orderbooks       List all orderbooks.
  --symbols          List all symbols.
  --orders           List all orders.
  --trades           List all trades.
  --symbol=<symbol>  Asset symbol (eg 'NTN').
  --status=<status>  Filter order list by <status>.
  --pair=<pair>      Filter order list by <pair>.
  --start=<date>     Filter order list by timestamp on or after <date>.
  --end=<date>       Filter order list by timestamp on or before <date>.
  --side=<side>      Filter order list by <side>.
"""
from docopt import docopt
import os
import subprocess
import requests
import pandas as pd
import json
import configparser
from version import __version__

##
## Globals
##

args = docopt(__doc__, version=__version__)
base_url = "https://cax.piccadilly.autonity.org/api"
timeout_seconds = int(args['--timeout'])

def read_config(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Configuration file not found: {file_path}")
    config = configparser.ConfigParser()
    config.read(file_path)
    return config

try:
    config = read_config('.caxcli')

except FileNotFoundError as fnf_error:
    print(fnf_error)
    exit(1)
except configparser.Error as cp_error:
    print(f"Error parsing config file: {cp_error}")
    exit(1)

api_key = config['api']['api_key']

headers = {
    'API-Key': api_key
}

params = {}
if args['--status']:
    params['status'] = args['--status'].lower()
if args['--start']:
    params['start'] = args['--start']
if args['--end']:
    params['end'] = args['--end']
if args['--pair']:
    params['pair'] = args['--pair'].upper()
if args['--symbol']:
    params['symbol'] = args['--symbol'].upper()

##
## Main
##

def main():
    if args['depth']:
        x = get_orderbook_depth(args['<pair>'].upper())
        print_orderbook_depth_val(x)
    if args['list']:
        if args['--deposits']:
            x = get_account_deposits(params)
            print_table_return_val(x)
        if args['--withdraws']:
            x = get_account_withdraws(params)
            print_table_return_val(x)
        if args['--balances']:
            x = get_all_account_balances(params)
            print_table_return_val(x)
        if args['--orderbooks']:
            x = get_all_orderbooks()
            print_table_return_val(x)
        if args['--symbols']:
            x = get_all_symbols(params)
            print_table_return_val(x)
        if args['--orders']:
            x = get_orders(params)
            print_table_return_val(x)
        if args['--trades']:
            x = get_trades(params)
            print_table_return_val(x)
    if args['bid']:
        x = post_submit_limit_order(args['<pair>'], 'bid', args['<price>'], args['<amount>'])
        print(x)
    if args['ask']:
        x = post_submit_limit_order(args['<pair>'], 'ask', args['<price>'], args['<amount>'])
        print(x)
    if args['cancel']:
        x = del_cancel_order(args['<order_id>'])
        print(x)
    if args['withdraw']:
        x = post_request_withdraw(args['<symbol>'].upper(), args['<amount>'])
        print(x)
        
if __name__ == '__main__':
    main()

##
## Utils
##

def send_cax_get_request(endpoint, params=None):
    url = base_url + endpoint
    try:
        if params is None:
            response = requests.get(url, headers=headers, timeout=timeout_seconds)
        else:
            response = requests.get(url, params=params, headers=headers, timeout=timeout_seconds)
        resp = response.json()
        return resp
    except requests.Timeout:
        print("request to cax.piccadilly.autonity.org timed out")
    except requests.RequestException:
        print("failed to retrieve data")

def send_cax_post_request(endpoint, json=None):
    url = base_url + endpoint
    try:
        if json is None:
            response = requests.post(url, headers=headers, timeout=timeout_seconds)
        else:
            response = requests.post(url, headers=headers, json=json, timeout=timeout_seconds)
        resp = response.json()
        return resp
    except requests.Timeout:
        print("request to cax.piccadilly.autonity.org timed out")
    except requests.RequestException:
        print("failed to retrieve data")

def send_cax_delete_request(endpoint, json=None):
    url = base_url + endpoint
    try:
        if json is None:
            response = requests.delete(url, headers=headers, timeout=timeout_seconds)
        else:
            response = requests.delete(url, headers=headers, json=json, timeout=timeout_seconds)
        resp = response.json()
        return resp
    except requests.Timeout:
        print("request to cax.piccadilly.autonity.org timed out")
    except requests.RequestException:
        print("failed to retrieve data")

def format_pair(pair):
    pair = pair.upper()
    return pair

def print_table_return_val(x):
    if args['--json']:
        x = json.dumps(x)
    else:
        x = pd.DataFrame(x)
    print(x)

def print_orderbook_depth_val(x):    
    if not args['--json']:
        columns = ["amount","price"]
        asks = pd.DataFrame(x['asks'])
        asks = asks.astype(float)
        asks = asks[columns]
        asks = asks.sort_values(by="price", ascending=False)
        bids = pd.DataFrame(x['bids'])
        bids = bids.astype(float)
        bids = bids[columns]
        bids = bids.sort_values(by="price", ascending=False)
        asks_string = asks.to_string(index=False, header=False)
        bids_string = bids.to_string(index=False, header=False)
        print(asks_string)
        print("")
        print(bids_string)
        print("")
        print(x['timestamp'])
    else:
        print(json.dumps(x))
        
##
## Account endpoints
##

def get_account_deposits(params):
    resp = send_cax_get_request("/deposits", params=params)
    return resp

# def post_create_api_key():
#     return None

def post_request_withdraw(symbol, amount):
    data = {
        'symbol': symbol,
        'amount': amount
    }
    x = send_cax_post_request("/withdraws", data)
    return(x)

def get_account_withdraws(params):
    resp = send_cax_get_request("/withdraws", params=params)
    return resp

def get_all_account_balances(params):
    resp = send_cax_get_request("/balances", params=params)
    return resp

# def get_symbol_account_balance(name):
#     resp = send_cax_get_request("/balances/" + name)
#     return resp

##
## Exchange endpoints
##

def get_all_orderbooks():
    resp = send_cax_get_request("/orderbooks")
    return resp

# def get_exchange_status(params):
#     resp = send_cax_get_request("/status", params)
#     return resp
    
def get_all_symbols(params):
    resp = send_cax_get_request("/symbols", params)
    return resp
    
# def get_orderbook_info(pair):
#     resp = send_cax_get_request("/orderbooks/" + pair)
#     return resp

# def get_symbol_info(name):
#     resp = send_cax_get_request("/symbols/" + name)
#     return resp

def get_orderbook_quote(pair):
    resp = send_cax_get_request("/orderbooks/" + pair + "/quote")
    return resp

def get_orderbook_depth(pair):
    resp = send_cax_get_request("/orderbooks/" + pair + "/depth")
    return resp

##
## Trading endpoints
##

def get_orders(params):
    resp = send_cax_get_request("/orders", params)
    return resp

def post_submit_limit_order(pair, side, price, amount):
    data = {
        'pair': pair,
        'side': side,
        'price': price,
        'amount': amount
    }
    x = send_cax_post_request("/orders", data)
    return x

def get_trades(params=None):
    if params is not None:
        resp = send_cax_get_request("/trades", params)
    else:
        resp = send_cax_get_request("/trades")
    return resp

# def get_order_info():
#     return None

def del_cancel_order(order_id):
    x = send_cax_delete_request("/orders/" + order_id)
    return x

# def get_trade_info():
#     return None
