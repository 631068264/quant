#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 2019-04-05 10:15
@annotation = ''
"""


# class SingletonType(type):
#     _instances = {}
#
#     def __call__(cls, *args, **kwargs):
#         if cls not in cls._instances:
#             cls._instances[cls] = super(SingletonType,
#                                         cls).__call__(*args, **kwargs)
#         return cls._instances[cls]
#
# class BaseController(object):
#     _singleton = None
#     def __new__(cls, *a, **k):
#         if not cls._singleton:
#             cls._singleton = object.__new__(cls, *a, **k)
#         return cls._singleton
#
#
# class A(BaseController):
#     pass
#
#
# a = A()
# b = A()
# print(a is b)

# class Computer:
#     def __init__(self, name):
#         self.name = name
#
#     def __str__(self):
#         return 'the {} computer'.format(self.name)
#
#     def execute(self):
#         """ call by client code """
#         return 'execute a program'
#
#
# class Synthesizer:
#     def __init__(self, name):
#         self.name = name
#
#     def __str__(self):
#         return 'the {} synthesizer'.format(self.name)
#
#     def play(self):
#         return 'is playing an electroinc song'
#
#
# class Human:
#     def __init__(self, name):
#         self.name = name
#
#     def __str__(self):
#         return 'the {} human'.format(self.name)
#
#     def speak(self):
#         return 'says hello'
#
#
# class Adapter:
#     def __init__(self, obj, adapted_methods):
#         """ 不使用继承，使用__dict__属性实现适配器模式 """
#         self.obj = obj
#         self.__dict__.update(adapted_methods)
#
#     def __str__(self):
#         return str(self.obj)
#
#
# # 适配器使用示例
# def main():
#     objs = [Computer('Asus')]
#     synth = Synthesizer('moog')
#     objs.append(Adapter(synth, dict(execute=synth.play)))
#     human = Human('Wnn')
#     objs.append(Adapter(human, dict(execute=human.speak)))
#
#     for o in objs:
#         # 用统一的execute适配不同对象的方法，这样在无需修改源对象的情况下就实现了不同对象方法的适配
#         print('{} {}'.format(str(o), o.execute()))
#
#
# if __name__ == "__main__":
#     main()

# class Event:
#     def __init__(self, name):
#         self.name = name
#
#     def __str__(self):
#         return self.name
#
#
# class Widget:
#
#     """Docstring for Widget. """
#
#     def __init__(self, parent=None):
#         self.parent = parent
#
#     def handle(self, event):
#         handler = 'handle_{}'.format(event)
#         if hasattr(self, handler):
#             method = getattr(self, handler)
#             method(event)
#         elif self.parent:
#             self.parent.handle(event)
#         elif hasattr(self, 'handle_default'):
#             self.handle_default(event)
#
#
# class MainWindow(Widget):
#     def handle_close(self, event):
#         print('MainWindow: {}'.format(event))
#
#     def handle_default(self, event):
#         print('MainWindow: Default {}'.format(event))
#
#
# class SendDialog(Widget):
#     def handle_paint(self, event):
#         print('SendDialog: {}'.format(event))
#
#
# class MsgText(Widget):
#     def handle_down(self, event):
#         print('MsgText: {}'.format(event))
#
#
# def main():
#     mw = MainWindow()
#     sd = SendDialog(mw)    # parent是mw
#     msg = MsgText(sd)
#
#     for e in ('down', 'paint', 'unhandled', 'close'):
#         evt = Event(e)
#         print('\nSending event -{}- to MainWindow'.format(evt))
#         mw.handle(evt)
#         print('Sending event -{}- to SendDialog'.format(evt))
#         sd.handle(evt)
#         print('Sending event -{}- to MsgText'.format(evt))
#         msg.handle(evt)
#
# if __name__ == "__main__":
#     main()

# class Publisher:
#     def __init__(self):
#         self.observers = []
#
#     def add(self, observer):
#         if observer not in self.observers:
#             self.observers.append(observer)
#         else:
#             print('Failed to add : {}').format(observer)
#
#     def remove(self, observer):
#         try:
#             self.observers.remove(observer)
#         except ValueError:
#             print('Failed to remove : {}').format(observer)
#
#     def notify(self):
#         [o.notify_by(self) for o in self.observers]
#
# class DefaultFormatter(Publisher):
#     def __init__(self, name):
#         super().__init__()
#         self.name = name
#         self._data = 0
#
#     def __str__(self):
#         return "{}: '{}' has data = {}".format(
#             type(self).__name__, self.name, self._data)
#
#     @property
#     def data(self):
#         return self._data
#
#     @data.setter
#     def data(self, new_value):
#         try:
#             self._data = int(new_value)
#         except ValueError as e:
#             print('Error: {}'.format(e))
#         else:
#             self.notify()    # data 在被合法赋值以后会执行notify
#
#
# class HexFormatter:
#     """ 订阅者 """
#     def notify_by(self, publisher):
#         print("{}: '{}' has now hex data = {}".format(
#             type(self).__name__, publisher.name, hex(publisher.data)))
#
#
# class BinaryFormatter:
#     """ 订阅者 """
#     def notify_by(self, publisher):
#         print("{}: '{}' has now bin data = {}".format(
#             type(self).__name__, publisher.name, bin(publisher.data)))
#
#
# if __name__ == "__main__":
#     df = DefaultFormatter('test1')
#     print(df)
#     print()
#     hf = HexFormatter()
#     df.add(hf)
#     df.data = 3
#     print(df)
#
#     print()
#     bf = BinaryFormatter()
#     df.add(bf)
#     df.data = 21
#     print(df)

# class Context:
#     def __init__(self):
#         self.input = ""
#         self.output = ""
#
#
# class AbstractExpression:
#     def Interpret(self, context):
#         pass
#
#
# class Expression(AbstractExpression):
#     def Interpret(self, context):
#         print("terminal interpret")
#
#
# class NonterminalExpression(AbstractExpression):
#     def Interpret(self, context):
#         print("Nonterminal interpret")
#
#
# if __name__ == "__main__":
#     context = ""
#     c = []
#     c = c + [Expression()]
#     c = c + [NonterminalExpression()]
#     c = c + [Expression()]
#     c = c + [Expression()]
#     for a in c:
#         a.Interpret(context)

class Node(object):
    pass


class A(Node):
    pass


class B(Node):


    pass


class C(A, B):
    pass


class Visitor(object):
    def visit(self, node, *args, **kwargs):
        meth = None
        for cls in node.__class__.__mro__:
            meth_name = 'visit_' + cls.__name__
            meth = getattr(self, meth_name, None)
            if meth:
                break

            if not meth:
                meth = self.generic_visit
            return meth(node, *args, **kwargs)

    def generic_visit(self, node, *args, **kwargs):
        print('generic_visit ' + node.__class__.__name__)

    def visit_B(self, node, *args, **kwargs):
        print('visit_B ' + node.__class__.__name__)


a = A()
b = B()
c = C()
visitor = Visitor()
# visitor.visit(a)
visitor.visit(b)
# visitor.visit(c)

class Test(object):
    @staticmethod
    def foo():
        pass

    def bar(self):
        pass
import inspect
print(inspect.isfunction(Test.bar))
print(inspect.isfunction(Test.foo))