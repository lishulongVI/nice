# -*- coding: utf-8 -*-
"""
@contact: lishulong.never@gmail.com
@time: 2019/5/24 上午11:51
"""
import yaml
import aioredis
import trafaret
from aiohttp import web


def load_conf(f_name):
    """
    rt模式下，python在读取文本时会自动把\r\n转换成\n.
    wt模式下，Python写文件时会用\r\n来表示换行。
    :param f_name:
    :return:
    """
    with open(file=f_name, mode='rt') as file:
        # https://github.com/yaml/pyyaml/wiki/PyYAML-yaml.load(input)-Deprecation
        return yaml.load(file, Loader=yaml.SafeLoader)


async def init_redis(conf, loop):
    pool = await aioredis.create_redis_pool(
        address='redis://{}:{}'.format(conf['host'], conf['port']),
        password=conf['password'],
        db=conf['db'],
        minsize=conf['minsize'],
        maxsize=conf['maxsize'],
        loop=loop
    )
    return pool


CHARS = 'abcdefghijkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789'


def encode(num, alphabet=CHARS):
    """
    进制转换
    :param num:
    :param alphabet:
    :return:
    """
    if num == 0:
        return alphabet[0]
    arr = []
    base = len(alphabet)
    while num:
        num, rem = divmod(num, base)
        arr.append(alphabet[rem])
    arr.reverse()
    return ''.join(arr)


ShortifyRequest = trafaret.Dict({
    trafaret.Key('url'): trafaret.URL
})


def fetch_url(data):
    """
    url 验证
    :param data:
    :return:
    """
    try:
        data = ShortifyRequest(data)
        return data['url']
    except trafaret.DataError:
        raise web.HTTPBadRequest()


if __name__ == '__main__':
    print(encode(123456))
    print(encode(123457))
