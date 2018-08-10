# -*- coding: utf-8 -*-

import time
import logging
from examples.python3.base import Base, InvalidParamsHttpResponse
from examples.python3.utils import check_is_all_digit


class DragonExV1(Base):
    def __init__(self, access_key, secret_key, host):
        super(DragonExV1, self).__init__(access_key=access_key, secret_key=secret_key, host=host)

    def create_new_token(self):
        path = '/api/v1/token/new/'
        data = {}
        return self.post(path, data)

    def token_status(self):
        path = '/api/v1/token/status/'
        data = {}
        return self.post(path, data)

    def ensure_token_enable(self, forever=False):
        http = self.token_status()
        if not http.ok:
            logging.debug('abnormal token status : token={}, code={}, msg={}'.format(self.token, http.code, http.msg))
            r = self.create_new_token()
            if r.ok:
                self.token = r.data['token']
                logging.debug('create new token succeed: token={}'.format(self.token))

            else:
                logging.debug('create token failed: code={}, msg={}'.format(r.code, r.msg))

        else:
            logging.debug('normal token status: token={}'.format(self.token))

        while forever:
            time.sleep(60)
            self.ensure_token_enable()

        return http

    def get_all_coins(self):
        path = '/api/v1/coin/all/'
        params = {}
        return self.get(path, params)

    def get_user_own_coins(self):
        path = '/api/v1/user/own/'
        data = {}
        return self.post(path, data)

    def get_all_symbos(self):
        path = '/api/v1/symbol/all/'
        params = {}
        return self.get(path, params)

    def get_market_kline(self, symbol_id, start_time=0, search_direction=2, count=10, kline_type=1):
        if not check_is_all_digit(symbol_id, start_time, search_direction, count, kline_type):
            return InvalidParamsHttpResponse

        path = '/api/v1/market/kline/'
        params = {'symbol_id': symbol_id, 'st': start_time, 'direction': search_direction, 'count': count,
                  'kline_type': kline_type}
        return self.get(path, params)

    def get_market_buy(self, symbol_id):
        if not check_is_all_digit(symbol_id):
            return InvalidParamsHttpResponse

        path = '/api/v1/market/buy/'
        params = {'symbol_id': symbol_id}
        return self.get(path, params)

    def get_market_sell(self, symbol_id):
        if not check_is_all_digit(symbol_id):
            return InvalidParamsHttpResponse

        path = '/api/v1/market/sell/'
        params = {'symbol_id': symbol_id}
        return self.get(path, params)

    def get_market_real(self, symbol_id):
        if not check_is_all_digit(symbol_id):
            return InvalidParamsHttpResponse

        path = '/api/v1/market/real/'
        params = {'symbol_id': symbol_id}
        return self.get(path, params)

    def add_order_buy(self, symbol_id, price, volume):
        if not check_is_all_digit(symbol_id):
            return InvalidParamsHttpResponse

        path = '/api/v1/order/buy/'
        data = {'symbol_id': symbol_id, 'price': '{}'.format(price), 'volume': '{}'.format(volume)}
        return self.post(path, data)

    def add_order_sell(self, symbol_id, price, volume):
        if not check_is_all_digit(symbol_id):
            return InvalidParamsHttpResponse

        path = '/api/v1/order/sell/'
        data = {'symbol_id': symbol_id, 'price': '{}'.format(price), 'volume': '{}'.format(volume)}
        return self.post(path, data)

    def cancel_order(self, symbol_id, order_id):
        if not check_is_all_digit(symbol_id, order_id):
            return InvalidParamsHttpResponse

        path = '/api/v1/order/cancel/'
        data = {'symbol_id': symbol_id, 'order_id': order_id}
        return self.post(path, data)

    def get_order_detail(self, symbol_id, order_id):
        if not check_is_all_digit(symbol_id, order_id):
            return InvalidParamsHttpResponse

        path = '/api/v1/order/detail/'
        data = {'symbol_id': symbol_id, 'order_id': order_id}
        return self.post(path, data)

    def get_user_order_history(self, symbol_id, search_direction=2, start_time=0, count=10, status=0):
        if not check_is_all_digit(symbol_id, search_direction, start_time, count, status):
            return InvalidParamsHttpResponse

        path = '/api/v1/order/history/'
        data = {'symbol_id': symbol_id, 'direction': search_direction, 'start': start_time, 'count': count,
                'status': status}
        return self.post(path, data)

    def get_user_deal_history(self, symbol_id, search_direction=2, start_time=0, count=10):
        if not check_is_all_digit(symbol_id, search_direction, start_time, count):
            return InvalidParamsHttpResponse

        path = '/api/v1/deal/history/'
        data = {'symbol_id': symbol_id, 'direction': search_direction, 'start': start_time, 'count': count}
        return self.post(path, data)

    def get_prepay_addr(self, coin_id):
        if not check_is_all_digit(coin_id):
            return InvalidParamsHttpResponse

        path = '/api/v1/coin/prepay/addr/'
        data = {'coin_id': coin_id}
        return self.post(path, data)

    def list_prepay_history(self, coin_id, page_num=1, page_size=10):
        if not check_is_all_digit(coin_id, page_num, page_size):
            return InvalidParamsHttpResponse

        path = '/api/v1/coin/prepay/history/'
        data = {'coin_id': coin_id, 'page_num': page_num,  'page_size': page_size}
        return self.post(path, data)

    def list_withdraw_addr(self, coin_id):
        if not check_is_all_digit(coin_id):
            return InvalidParamsHttpResponse

        path = '/api/v1/coin/withdraw/addr/list/'
        data = {'coin_id': coin_id}
        return self.post(path, data)

    def add_new_withdraw(self, coin_id, addr_id, volume):
        if not check_is_all_digit(coin_id, addr_id):
            return InvalidParamsHttpResponse

        path = '/api/v1/coin/withdraw/new/'
        data = {'coin_id': coin_id, 'addr_id': addr_id, 'volume': volume}
        return self.post(path, data)

    def list_withdraw_history(self, coin_id, page_num=1, page_size=10):
        if not check_is_all_digit(coin_id, page_num, page_size):
            return InvalidParamsHttpResponse

        path = '/api/v1/coin/withdraw/new/'
        data = {'coin_id': coin_id, 'page_num': page_num, 'page_size': page_size}
        return self.post(path, data)
