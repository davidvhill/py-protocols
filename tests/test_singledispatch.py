import pytest

import py_protocols as protocols

MyProtocol = protocols.define(
    "Some test protocol",
    foo='test foo function',
    bar='test bar function',
)


##
class ClExplicit():
    '''Explicit protocol implementation.'''

protocols.register(
    protocol=MyProtocol,
    type=ClExplicit,
    foo=lambda _: 1,
    bar=lambda _: 2,
)


##
class ClExplicitInherited(ClExplicit):
    '''Inherited explicit protocol implementation'''


##
class ClExplicitInheritedOverride(ClExplicit):
    '''Override inherited explicit protocol implementation'''

protocols.register(
    protocol=MyProtocol,
    type=ClExplicitInheritedOverride,
    foo=lambda _: 3,
    bar=lambda _: 4,
)

##
class ClDuckType:
    '''Ducktyping protocol implementation'''
    def foo(self):
        return 5

    def bar(self):
        return 6


##
class ClDuckTypeInherited(ClDuckType):
    '''Inherited implementation'''
    pass


##
class ClDuckTypeOverride(ClDuckType):
    '''Explicit override ducktype implementation'''

protocols.register(
    protocol=MyProtocol,
    type=ClDuckTypeOverride,
    foo=lambda _: 7,
    bar=lambda _: 8,
)


def test_docstrigns():
    assert MyProtocol.__doc__ == "Some test protocol"
    assert MyProtocol.foo.__doc__ == 'test foo function'
    assert MyProtocol.bar.__doc__ == 'test bar function'


@pytest.mark.parametrize('obj, exp_foo, exp_bar', [
    (ClExplicit(), 1, 2),
    (ClExplicitInherited(), 1, 2),
    (ClExplicitInheritedOverride(), 3, 4),
    (ClDuckType(), 5, 6),
    (ClDuckTypeInherited(), 5, 6),
    (ClDuckTypeOverride(), 7, 8),
])
def test_dispatch(obj, exp_foo, exp_bar):
    foo = MyProtocol.foo(obj)
    bar = MyProtocol.bar(obj)
    assert foo == exp_foo
    assert bar == exp_bar


def test_exapmples():
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
