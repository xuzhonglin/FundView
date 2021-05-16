#!/usr/bin/env python
# _*_coding:utf-8_*_

"""
@Time     : 2021/5/16 17:18
@Author   : colinxu
@File     : coin-core.py
@Desc     : 
"""
import json

import websocket

try:
    import thread
except ImportError:
    import _thread as thread
import time


def on_message(ws, message):
    print(message)


def on_error(ws, error):
    print(error)


def on_close(ws):
    print("### closed ###")


def on_open(ws):
    def run(*args):
        payload = {"op": "subscribe", "args": ["spot/ticker:ETH-USDT", "spot/candle60s:ETH-USDT"]}
        ws.send(json.dumps(payload))

    thread.start_new_thread(run, ())


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://real.coinall.ltd:8443/ws/v3/public",
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.run_forever()
