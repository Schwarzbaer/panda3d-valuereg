class ValueRegistry:
    def __init__(self, default_values=None):
        if default_values is None:
            default_values = {}
        self.values = default_values
        self.callbacks = {key: {} for key in default_values}

    def add_values(self, value_dict):
        assert not any(k in self.values for k in value_dict)
        self.values.update(value_dict)
        self.callbacks.update({key: {} for key in value_dict})

    def register(self, registrar, callback, key):
        self.callbacks[key][registrar] = callback

    def unregister(self, registrar, key):
        del self.callbacks[key][registrar]

    def update(self, key, value):
        self.values[key] = value
        if key in self.callbacks:
            for registrar, callback in self.callbacks[key].items():
                callback(key, value)


class ValueListener:
    def __init__(self, registry=None):
        if registry is None:
            registry = base.value_registry
        self.registry = registry

    def register(self, key):
        self.registry.register(self, self.callback, key)

    def unregister(self, key):
        self.registry.unregister(self, key)

    def callback(self, key, value):
        print(value)


def add_value_registry(default_values=None):
    base.value_registry = ValueRegistry(
        default_values=default_values,
    )
