# -*- coding: utf-8 -*-
"""
@contact: lishulong.never@gmail.com
@time: 2019/5/22 下午3:49
"""
import sys
import gc

if __name__ == '__main__':
    print(sys.getswitchinterval())
    sys.setswitchinterval(0.01)

    gc.disable()
    gc.set_threshold(0)