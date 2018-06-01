import json
import logging

from websocket import WebSocketApp

CMD_TYPE_LOGIN = 'login'
CMD_TYPE_SUB = 'sub'
CMD_TYPE_UNSUB = 'unsub'

logging.basicConfig(level=logging.DEBUG)


class WebSocketRequest(object):
    def __init__(self, cmd=None, **kwargs):
        self.data = '' if cmd is None else self.__make_data(cmd=cmd, **kwargs)

    @staticmethod
    def __make_data(cmd, **kwargs):
        value = json.dumps(kwargs)
        data = json.dumps({'cmd': cmd, 'value': value})
        return data

    def login(self, method, path, headers):
        self.data = self.__make_data(cmd=CMD_TYPE_LOGIN, method=method, path=path, headers=headers)
        return self

    def sub(self, room_id):
        self.data = self.__make_data(cmd=CMD_TYPE_SUB, roomid=room_id)
        return self

    def unsub(self, room_id):
        self.data = self.__make_data(cmd=CMD_TYPE_SUB, roomid=room_id)
        return self


class WsBase(WebSocketApp):
    def __init__(self, url, reqs, **kwargs):
        self.reqs = self.format_reqs(reqs)
        super(WsBase, self).__init__(url=url, on_open=self.on_open, on_message=self.on_message, **kwargs)

    @staticmethod
    def format_reqs(reqs):
        if reqs is None:
            return []

        elif isinstance(reqs, dict):
            reqs = reqs.values()

        return [req for req in reqs if isinstance(req, WebSocketRequest)]

    def on_open(self, ws):
        for req in self.reqs:
            ws.send(req.data)

    def on_message(self, ws, message):
        logging.debug('receive message, message={}'.format(message))


if __name__ == '__main__':
    url = 'wss://openapiws.dragonex.io/ws'
    room_ids = ['market-quote-multi-buy-coin-{}'.format(coin_id) for coin_id in [101, 103, 104]]

    reqs = [WebSocketRequest().sub(room_id) for room_id in room_ids]

    ws = WsBase(url=url, reqs=reqs)
    ws.run_forever()
