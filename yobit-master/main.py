import argparse
import time
from YoBit import YoBit
yb = YoBit(api_key='81E47402A0827714070A14D80F7188F0', api_secret='a76dbd274a818364bff8cb7c0ccba8dc')

def get_trade_info(symbol, rate, pair):
    ticker_info = yb.ticker(symbol)
    market_price = ticker_info[symbol]['sell']
    print("market price:%.8f"%market_price)
    new_price = market_price + round((market_price * rate),8)
    print("new price:%.8f"%new_price)
    balance_info = yb.get_info()
    btc_balance = balance_info['return']['funds'][pair]
    print("btc balance:", btc_balance)
    btc_count = round((btc_balance / new_price),8)
    print("btc count:", btc_count)
    return new_price, btc_count

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--symbol", type=str, help="Market Symbol (Ex: trx_btc)", required=True)
    option = parser.parse_args()
    pair='eth'
    symbol = option.symbol+'_'+pair
    rate = 0.02
    test_mode=False

    type_all = 'buy_all'
    print("symbol:%s , type:%s, rate:%.8f" % (symbol, type_all, rate))
    buy_price, buy_count = get_trade_info(symbol, rate, pair)
    type = 'buy'
    print(type + " new price : %.8f, count : %.8f" % (buy_price, buy_count))
    if test_mode == False:
        buy_trade = yb.trade(symbol, type, buy_price, buy_count)
        print(buy_trade)
        if (buy_trade['success'] == 1):
            print("Alış yapıldı.")

    type_all = 'sell_all'
    print("symbol:%s , type:%s, rate:%.8f" % (symbol, type_all, rate))
    sell_count = buy_count
    type = 'sell'
    exit_cycle = False
    count = 2
    while not exit_cycle:
        sell_price = buy_price * count
        print(type + " sell price : %.8f, count : %.8f" % (sell_price, sell_count))
        sell_trade = yb.trade(symbol, type, sell_price, sell_count)
        print("sell trade:",sell_trade)
        order_id = sell_trade['return']['order_id']
        print("order id:",order_id)
        time.sleep(10)
        cancel_info = yb.cancel_order(order_id)
        print("cancel info:", cancel_info)
        if (cancel_info['success']==0):
            exit_cycle = True
            print("Satış yapıldı.")
        else:
            ticker_info = yb.ticker(symbol)
            if (ticker_info[symbol]['buy']>sell_price):
                time.sleep(5)
        count = count - 0.5

def buy_op():
    parser = argparse.ArgumentParser()
    parser.add_argument("--symbol", type=str, help="Market Symbol (Ex: trx_btc)", required=True)
    option = parser.parse_args()
    pair='eth'
    symbol = option.symbol+'_'+pair
    rate = 0.02
    test_mode=False

    type_all = 'buy_all'
    print("symbol:%s , type:%s, rate:%.8f" % (symbol, type_all, rate))
    buy_price, buy_count = get_trade_info(symbol, rate, pair)
    type = 'buy'

    if test_mode == False:
        buy_price = buy_price-0.00002000
        print(type + " new price : %.8f, count : %.8f" % (buy_price, buy_count))
        print(yb.trade(symbol, type, str(buy_price), buy_count))
        print("Alış yapıldı.")

#main()
buy_op()

# READ ME
# python main.py --symbol vidz
# python main.py --symbol vidz
# python main.py --symbol bcp
