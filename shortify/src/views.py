# -*- coding: utf-8 -*-
"""
@contact: lishulong.never@gmail.com
@time: 2019/5/24 下午2:25
"""
import aiohttp_jinja2
from aiohttp import web

from shortify.src.utils import fetch_url, encode


class SiteHandler:
    def __init__(self, redis_pool, conf):
        self._redis = redis_pool
        self._conf = conf

    @aiohttp_jinja2.template('index.html')
    async def index(self, request):
        return {}

    @aiohttp_jinja2.template('time.html')
    async def shortify(self, request):
        data = await request.json()
        url = fetch_url(data=data)
        index = await self._redis.incr('shortify:count')
        path = encode(num=index)
        await self._redis.set('shortify:{}'.format(path), url)
        host = self._conf['host']
        port = self._conf['port']
        url_ = f'http://{host}:{port}/{path}'
        return web.json_response({'url': url_})

    async def redirect(self, request):
        short_id = request.match_info['short_id']
        location = await self._redis.get('shortify:{}'.format(short_id))
        if not location:
            raise web.HTTPNotFound()
        return web.HTTPFound(location=location.decode())
