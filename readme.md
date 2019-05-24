 # cpython
 > python 比c++慢几倍到几十倍
 
 _效率：【开发效率，执行效率】_
 
 
## 执行效率低

```
1. 动态语言 一个变量指向的对象的类型在运行的时候才能确认，编译器做不了预测
2. 解释执行，不支持just in time compiler
3、一切皆对象 每个对象都需要维护引用计数
4、gil golable interpreter lock 多线程不能真正的并发 io密集的可用，cpu密集的只能多进程，在单线程中，gil也会有影响，python每执行100个操作码就会尝试线程切换（sys.getswitchinterval()）
5、gc：引用计数，标记清理和分代回收，每次gc的时候程序都会中断
```

## 优化（一切的优化都要基于profile）

1. 多线程：https://github.com/sumerc/yappi
2. 协程：https://github.com/ajdavis/GreenletProfiler
3. 禁用 Python 的 GC 机制后，Instagram 性能提升 10%：https://www.infoq.cn/article/disable-python-gc-mechanism-instagram-performance-increase
4. cython：http://docs.cython.org/en/latest/
5. gevent：http://hhkbp2.github.io/gevent-tutorial/
6. cookbook https://python3-cookbook.readthedocs.io/zh_CN/latest/

```
1、判断一个对象是否在一个集合里面 使用set
2、短路逻辑 把概率高的放在前面，减少比较
3、字符累加使用join

4、减少函数的调用层次
5、优化属性查找，频繁访问的可以做成局部变量

6、禁用gc，解决循环引用，不写 使用weakref
7、确定是单线程可以 设置更大的数值  getswitchinterval
8、使用slots 减少内存占用

9、避免咋for循环中使用点操作
```

## aio-http

```
on_loop_available:当loop以同步方式可用时被触发，因此任何非同步工作都要显式地使用应用loop。这是（当前）唯一的同步处理程序。

on_startup:在应用程序开始之前触发，这对于设定后台任务（如长轮询任务）非常有用。

on_teardown:在应用程序收到来自呼叫者的关闭信号且请求完成后触发。在这里，我们应该拆除我们建立的任何东西，并关闭到远端服务的长联机。

on_cleanup:在拆卸（teardown）完成后启动，允许最终的清理步骤执行，例如拆卸因为元件之间的依赖关系而无法在拆卸步骤清理的物件。
```