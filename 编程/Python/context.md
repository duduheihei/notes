## python中的__enter__ __exit__
[参考博客](https://www.cnblogs.com/flashBoxer/p/9664813.html)
在python中实现了__enter__和__exit__方法，即支持上下文管理器协议。上下文管理器就是支持上下文管理器协议的对象，它是为了with而生。当with语句在开始运行时，会在上下文管理器对象上调用 __enter__ 方法。with语句运行结束后，会在上下文管理器对象上调用 __exit__ 方法

