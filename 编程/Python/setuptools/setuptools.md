[tutorial](https://setuptools.pypa.io/en/latest/userguide/index.html)
[知乎:花了两天，终于把 Python 的 setup.py 给整明白了](https://zhuanlan.zhihu.com/p/276461821)

## [Module和Package](https://docs.python.org/3/glossary.html#term-package)
[参考知乎:python的import机制，package，自定义package等](https://zhuanlan.zhihu.com/p/449210363)
Module是python的基本单元可以被import，常见的py文件，文件夹都可以被import。package一定是module，module不一定是packagez.主要看import module后，module有没有__path__属性。有__path__属性的是package。package又分为常规包和命名空间包，常规包文件夹包含__init__.py文件，命名空间包不包含，二者import时存在差异。通常自己写库都需要写__init__.py函数，可以减少不必要的麻烦
An object that serves as an organizational unit of Python code. Modules have a namespace containing arbitrary Python objects. Modules are loaded into Python by the process of importing.  
A Python module which can contain submodules or recursively, subpackages. Technically, a package is a Python module with an __path__ attribute.

## Implicit Namespace Packages
[官方介绍](https://peps.python.org/pep-0420/)
Namespace packages are a mechanism for splitting a single Python package across multiple directories on disk