Py protocols
============

Define protocol (abstraction, API) and register implementation on some type later.

```python
import py_protocols as protocols

AProtocol = protocols.define(
    "Some test protocol",     # protocol documentation
    foo='test foo function',  # protocol function and its docstring
    bar='test bar function',  # function name should be verb
)

# is implemented test if protocol is implemened for given type
assert protocols.is_implemented(AProtocol, int) == False

# register some protocol implementation with given type
protocols.register(
    protocol=AProtocol,          # implement AProtocol
    type=int,                    # on type in
    foo=lambda _: 'foo on int',  # function and its implementation
    bar=lambda _: 'bar on int',  # all functions has to be implemented
)

assert protocols.is_implemented(AProtocol, int) == True

protocols.register(
    protocol=AProtocol,
    type=float,
    foo=lambda number: 'foo on double %.2f' % number,
    bar=lambda number, divisor: 'bar on double %.2f' % (number/divisor),
)

# fuction tied wiht int type was called
assert AProtocol.foo(123) == "foo on int"

# first argumet is passed to registered function at first position
assert AProtocol.foo(123.1) == "foo on double 123.10"

# any additional argument is passed to registered function a positional ...
assert AProtocol.bar(123.1, 2) == "bar on double 61.55"
# ... or named arguments
assert AProtocol.bar(123.1, divisor=2) == "bar on double 61.55"

class MyClass:
    def foo(self):
        return "foo on MyClass"

    def bar(self, divisor=2):
        return "bar with divisor %s on MyClass" % divisor

# protocol can be implemented by implementig protocol methods
assert protocols.is_implemented(AProtocol, MyClass) == True

my_instance = MyClass()

assert AProtocol.foo(my_instance) == "foo on MyClass"
assert AProtocol.bar(my_instance) == "bar with divisor 2 on MyClass"
assert AProtocol.bar(my_instance, 3) == "bar with divisor 3 on MyClass"
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

For now `protocols.define` creates class. But this is only for namespace and docstring. It may be replaced later.

TODO
----

* better errors (so far errors are not as descriptive as they can be)
* suggar for defining implementations
