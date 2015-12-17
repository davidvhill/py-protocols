Py protocols
============

Define protocol (abstraction, API) and register implementation on some type later.

```python
>>> import py_protocols as protocols


>>> AProtocol = protocols.define(
...     "Some test protocol",
...     foo='test foo function',
...     bar='test bar function',
... )

>>> protocols.is_implemented(int)
... False

>> protocols.register(AProtocol,
...     type=int,
...     foo=lambda _: 'foo on int',
...     bar=lambda _: 'bar on int',
... )

>>> protocols.is_implemented(int)
... True

>> protocols.register(AProtocol,
...     type=double,
...     foo=lambda _: 'foo on double',
...     bar=lambda _: 'bar on double',
... )

>>> AProtocol.foo(123)
... "foo on int"

>>> AProtocol.bar(123.1)
... "bar on double"

>>> class MyClass:
...     def foo(self):
...         return "foo on MyClass"
...
...     def bar(self):
...         return "bar on MyClass"

>>> protocols.is_implemented(MyClass)
... True

>>> my_instance = MyClass()

>>> AProtocol.bar(my_instance)
... "bar on MyClass"
```

Rationale
---------

Allow to create indepenedent abstraction and be explicit when using it.
Allow to tie abstraction implementation with arbitrary type.

This decompose polymorphism to four parts:

1) As a user of protocol I don't need to know how its implemented, but I'm explicit
about what abstraction I'm using.

2) At definition of type I don't need to know what abstraction type represents.

3) When implementing I'm in my onwn namespace and not type namespace.

4) At the end tie implementation and type.

I'm explicit about abstraction only at two points. When using and when tiing type with implementation.


Internals
---------

At the botom `functools.singledispatch` is used to dispatch. This module just provide suggar about it. Reason is that
`functools.singledispatch` has to be tied to some implementation. This module allow to create only definition of
an abstraction and create implementation later.


TODO
----

* better errors (so far errors are not as descriptive as they can be)
* suggar for defining implementations
