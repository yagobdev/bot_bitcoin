import websocket
import ssl
import json

import bitstamp.client
import credenciais

def cliente(): 
    return bitstamp.client.Trading(username=credenciais.USERNAME, key=credenciais.KEY, secret=credenciais.SECRET)    


def comprar_btc(quantidade):
    tranding_client = cliente()
    tranding_client.buy_market_order(quantidade)


def vender_btc(quantidade):
    tranding_client = cliente()
    tranding_client.sell_market_order(quantidade)


def ao_abrir(ws):
    print('Abriu a conexão')
    json_subscribe = '''
{
    "event": "bts:subscribe",
    "data": {
        "channel": "live_trades_btcusd"
    }
}
'''
    ws.send(json_subscribe) 


def on_close(ws, close_status_code, close_msg):
    print(f"Conexão fechada: {close_status_code} - {close_msg}")


def erro(ws, error):
    print('Deu error')        


def ao_receber_mensagem(ws, mensagem):
    msg = json.loads(mensagem)
    if msg.get('event') != 'trade':
        return
    price = msg['data']['price']
    print(price)
    if price > 71500:
        vender_btc(price)
    elif price < 70500:
        comprar_btc(price)
    else:
        print('Aguardar')    



if __name__ == '__main__':
    ws = websocket.WebSocketApp('wss://ws.bitstamp.net',
                                on_open=ao_abrir,
                                on_close=on_close,
                                on_error=erro,
                                on_message=ao_receber_mensagem)
    
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})  
