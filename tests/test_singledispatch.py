import pytest

import py_protocols as p

P = p.define(
    "Some test protocol",
    foo='test foo function',
    bar='test bar function',
)


##
class ClExplicit():
    '''Explicit protocol implementation.'''

p.register(P,
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

p.register(P,
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

p.register(P,
    type=ClDuckTypeOverride,
    foo=lambda _: 7,
    bar=lambda _: 8,
)


def test_docstrigns():
    assert P.__doc__ == "Some test protocol"
    assert P.foo.__doc__ == 'test foo function'
    assert P.bar.__doc__ == 'test bar function'


@pytest.mark.parametrize('obj, exp_foo, exp_bar', [
    (ClExplicit(), 1, 2),
    (ClExplicitInherited(), 1, 2),
    (ClExplicitInheritedOverride(), 3, 4),
    (ClDuckType(), 5, 6),
    (ClDuckTypeInherited(), 5, 6),
    (ClDuckTypeOverride(), 7, 8),
])
def test_dispatch(obj, exp_foo, exp_bar):
    foo = P.foo(obj)
    bar = P.bar(obj)
    assert foo == exp_foo
    assert bar == exp_bar

