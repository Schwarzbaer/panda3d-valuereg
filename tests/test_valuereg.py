import pytest

from valuereg import ValueRegistry
from valuereg import ValueListener
from valuereg import add_value_registry


@pytest.fixture
def fake_base():
    class FakeBase:
        value_registry = None
    __builtins__['base'] = FakeBase()


class RememberingListener(ValueListener):
    def __init__(self, *args, **kwargs):
        self.current_value = None
        super().__init__(*args, **kwargs)

    def callback(self, key, value):
        assert key == 'foo'
        self.current_value = value


def test_use_on_base(fake_base):
    vals = dict(
        foo=0,
    )
    add_value_registry()
    base.value_registry.add_values(vals)
    lis = RememberingListener()

    base.value_registry.update('foo', 1)
    assert lis.current_value is None

    lis.register('foo')
    base.value_registry.update('foo', 3)
    assert lis.current_value == 3

    lis.unregister('foo')
    base.value_registry.update('foo', 5)
    assert lis.current_value == 3


def test_use_without_base():
    vals = dict(
        foo=0,
    )
    reg = ValueRegistry(vals)
    lis = RememberingListener(registry=reg)

    reg.update('foo', 1)
    assert lis.current_value is None

    lis.register('foo')
    reg.update('foo', 3)
    assert lis.current_value == 3

    lis.unregister('foo')
    reg.update('foo', 5)
    assert lis.current_value == 3
