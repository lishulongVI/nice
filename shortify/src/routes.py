# -*- coding: utf-8 -*-
"""
@contact: lishulong.never@gmail.com
@time: 2019/5/24 下午2:44
"""


def setup_routes(app, handler, project_root):
    """
    建立路由规则
    :param app:
    :param handler:
    :param project_root:
    :return:
    """
    router = app.router

    router.add_get('/', handler.index, name='index')
    router.add_post('/shortify', handler.shortify, name='short')
    router.add_get('/{short_id}', handler.redirect, name='redirect')
    router.add_static('/static/', path='{}/{}'.format(project_root, 'static'),name='static')
