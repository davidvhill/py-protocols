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
        "Some test protocol",
        foo='test foo function',
        bar='test bar function',
    )

    assert protocols.is_implemented(AProtocol, int) == False

    protocols.register(AProtocol,
        type=int,
        foo=lambda _: 'foo on int',
        bar=lambda _: 'bar on int',
    )

    assert protocols.is_implemented(AProtocol, int) == True

    protocols.register(AProtocol,
        type=float,
        foo=lambda _: 'foo on double',
        bar=lambda _: 'bar on double',
    )

    assert AProtocol.foo(123) == "foo on int"

    assert AProtocol.bar(123.1) == "bar on double"

    class MyClass:
        def foo(self):
            return "foo on MyClass"

        def bar(self):
            return "bar on MyClass"

    assert protocols.is_implemented(AProtocol, MyClass) == True

    my_instance = MyClass()

    assert AProtocol.bar(my_instance) == "bar on MyClass"
