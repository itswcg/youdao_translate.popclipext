# -*- coding: utf-8 -*-
import uuid
import requests
import hashlib
import time


class Translator:
    YOUDAO_URL = 'https://openapi.youdao.com/api'
    APP_KEY = ''
    APP_SECRET = ''

    def encrypt(self, signStr):
        hash_algorithm = hashlib.sha256()
        hash_algorithm.update(signStr.encode('utf-8'))
        return hash_algorithm.hexdigest()

    def truncate(self, q):
        if q is None:
            return None
        size = len(q)
        return q if size <= 20 else q[0:10] + str(size) + q[size - 10:size]

    def do_request(self, data):
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        return requests.post(self.YOUDAO_URL, data=data, headers=headers)

    def translate(self, text, f='auto', t='auto'):
        q = text

        data = {}
        data['from'] = f
        data['to'] = t
        data['signType'] = 'v3'
        curtime = str(int(time.time()))
        data['curtime'] = curtime
        salt = str(uuid.uuid1())
        signStr = self.APP_KEY + self.truncate(q) + salt + curtime + self.APP_SECRET
        sign = self.encrypt(signStr)
        data['appKey'] = self.APP_KEY
        data['q'] = q
        data['salt'] = salt
        data['sign'] = sign

        response = self.do_request(data).json()
        if response['errorCode'] == '0':
            return response['translation'][0]
        else:
            return response['errorCode']
