# -*- coding: utf-8 -*-

import os
import base64
import datetime
import hashlib
import hmac
import json
import logging

import requests

from examples.python3.error_codes import CODE_OK, CODE_SERVER_ERROR, CODE_INVALID_PARAMS

logging.basicConfig(level=logging.DEBUG)

GMT_FORMAT = '%a, %d %b %Y %H:%M:%S GMT'


class Base(object):
    def __init__(self, access_key, secret_key, host):
        self.access_key = access_key
        self.secret_key = secret_key
        self.host = host

    @staticmethod
    def __format_response(response: requests.Response):
        status_code = response.status_code
        if status_code != 200:
            logging.debug('http request failed, status_code={}'.format(response))
            return HTTPResponse(ok=False, body=response.text)

        return HTTPResponse(ok=True, body=response.text)

    def url(self, path):
        return '{}{}'.format(self.host, path)

    def get(self, path, params=None, headers=None):
        url = self.url(path)

        if headers is None:
            headers = self.default_headers(method='GET', path=path)

        rsp = requests.get(url=url, params=params, headers=headers)
        return self.__format_response(response=rsp)

    def post(self, path, data=None, headers=None):
        url = self.url(path)
        if isinstance(data, dict):
            data = json.dumps(data)

        if headers is None:
            headers = self.default_headers(method='POST', path=path, data=data)

        rsp = requests.post(url=url, data=data, headers=headers)
        return self.__format_response(response=rsp)

    def default_headers(self, method, path, data=None):
        headers = {
            'Date': datetime.datetime.utcnow().strftime(GMT_FORMAT),
            'Content-Type': 'application/json',
            'token': self.token,
            'dragonex-atruth': 'DragonExIsTheBest'  # 此字段非必须
        }

        if data is not None:
            headers.update({'Content-Sha1': self.sha1(data)})

        auth = self.auth(method=method, path=path, headers=headers)
        headers.update({"Auth": auth})
        return headers

    @staticmethod
    def sha1(data):
        if not isinstance(data, (bytes, bytearray)):
            data = bytes(data, encoding='utf-8')
        h = hashlib.sha1()
        h.update(data)
        return h.hexdigest()

    def auth(self, method, path, headers):
        new_headers = {}
        for k, v in headers.items():
            new_headers[k.lower()] = v

        content_md5 = new_headers.get('content-sha1', '')
        content_type = new_headers.get('content-type', '')
        date = new_headers.get('date', '')

        dra_headers = ['{}:{}'.format(k, v) for k, v in new_headers.items() if k.startswith('dragonex-')]
        dra_headers.sort()
        can_headers = '{}\n'.format('\n'.join(dra_headers)) if dra_headers else ''

        str_to_sign = '\n'.join([method.upper(), content_md5, content_type, date, can_headers]) + path
        sign = self.sign(str_to_sign, self.secret_key)

        auth = '{}:{}'.format(self.access_key, sign)
        return auth

    @staticmethod
    def sign(string_to_sign, secret_key):
        h = hmac.new(bytes(secret_key, encoding='utf-8'), bytes(string_to_sign, encoding='utf-8'),
                     digestmod=hashlib.sha1).digest()
        return base64.b64encode(h).decode('utf-8')

    @property
    def token_file(self):
        return os.path.join(os.curdir, '{}.token'.format(self.access_key))

    @property
    def token(self):
        if not os.path.exists(self.token_file):
            return ''

        with open(self.token_file, 'r') as f:
            return f.read()

    @token.setter
    def token(self, token):
        token = token.decode('utf-8') if isinstance(token, bytes) else token
        with open(self.token_file, 'w') as f:
            f.write(token)


class HTTPResponse(object):
    def __init__(self, ok, body):
        if isinstance(body, dict):
            d = body

        elif isinstance(body, (bytes, bytearray, str)):
            body = body.decode('utf-8') if isinstance(body, (bytes, bytearray)) else body
            try:
                d = json.loads(body)

            except Exception as e:
                logging.error('err={}, body={}'.format(e, body))
                d = {'code': CODE_SERVER_ERROR, 'msg': 'error return', 'data': {}}

        else:
            d = {'code': CODE_SERVER_ERROR, 'msg': 'error return', 'data': {}}

        self._code = d.get('code', 0)
        self._msg = d.get('msg')
        self._data = d.get('data')
        self._ok = True if self.code == CODE_OK else False

    @property
    def ok(self):
        return self._ok

    @ok.setter
    def ok(self, ok):
        self._ok = ok

    @property
    def code(self):
        return self._code

    @code.setter
    def code(self, code):
        self._code = code

    @property
    def msg(self):
        return self._msg

    @msg.setter
    def msg(self, msg):
        self._msg = msg

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        self._data = data


InvalidParamsHttpResponse = HTTPResponse(ok=False,
                                         body={'code': CODE_INVALID_PARAMS, 'msg': 'invalid params', 'data': {}})
