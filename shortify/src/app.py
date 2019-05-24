# -*- coding: utf-8 -*-
"""
@contact: lishulong.never@gmail.com
@time: 2019/5/24 上午11:38
"""
import asyncio
import logging
import pathlib
import aiohttp_jinja2
import jinja2
from aiohttp import web

from shortify.src.routes import setup_routes
from shortify.src.utils import load_conf, init_redis
from shortify.src.views import SiteHandler

STATIC_PATH = pathlib.Path(__file__).parent.parent
TEMPLATE_PATH = pathlib.Path(__file__).parent.parent / 'template'
CONF = load_conf(pathlib.Path(__file__).parent.parent / 'conf' / 'config.yml')


async def set_redis(app: web.Application, loop: asyncio.AbstractEventLoop):
    """
    初始化redis 链接池
    :param app:
    :param loop:
    :return:
    """
    pool = await init_redis(loop=loop, conf=CONF['redis'])

    async def close_redis(app):
        redis_poll = app['redis_poll']
        redis_poll.close()
        await redis_poll.wait_closed()

    # 设置关闭信号触发后关闭链接
    app.on_cleanup.append(close_redis)
    app['redis_poll'] = pool
    return pool


async def setup_ji_jia(app: web.Application):
    """
    初始化jinjia模版引擎
    :param app:
    :return:
    """
    load = jinja2.FileSystemLoader(str(TEMPLATE_PATH))
    jinja_env = aiohttp_jinja2.setup(app=app, loader=load)
    return jinja_env


async def init_app(loop: asyncio.AbstractEventLoop):
    """
    初始化app
    :param loop:
    :return:
    """
    app = web.Application()
    await setup_ji_jia(app=app)
    redis_pool = await set_redis(app=app, loop=loop)
    hander = SiteHandler(redis_pool=redis_pool, conf=CONF)
    setup_routes(app=app, handler=hander, project_root=STATIC_PATH)
    return app, CONF['host'], CONF['port']


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    loop = asyncio.get_event_loop()
    app, host, port = loop.run_until_complete(init_app(loop=loop))
    web.run_app(app=app, host=host, port=port)
