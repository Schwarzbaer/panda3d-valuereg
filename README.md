panda3d-valuereg
================

You've got a bunch of variables, and you would like callbacks to be
called when their values change? As in, called *immediately*, so you
won't have to wait for the event manager to run? Maybe that's a global
set of variables, too, like a game's difficulty settings?

`panda3d-valuereg` to the rescue!


Usage
-----

    from valuereg import add_value_registry
    from valuereg import ValueListener


    # Call this *after* instantiating ShowBase; It adds
    # `base.value_registry` to it.
    add_value_registry()

    # One way to listen to changes in comfort is to implement a listener
    # class.
    class PrintingListener(ValueListener):
        def callback(self, key, value):
	    print(f'{key} -> {value}')

    # Now add a key to the registry.
    base.value_registry.add_values(dict(foo=0))

    # ...and create a listener, and register the key.
    lis = PrintingListener()
    lis.register('foo')

    # This should print `foo -> 3`
    base.value_registry.update(dict(foo=3))

    # And we can also stop listening to the changes.
    lis.unregister('foo')

But wait! There's more! Maybe you don't want your variables to be
global like that, or maybe you're not even using Panda3D (you
magnificient weirdo)! So just can ust create a registry yourself:

    from valuereg import ValueRegistry


    # BTW, we can pass the dict of initial values both to the registry
    # on creation, or to add_value_registry, using the `default_values`
    # keyword.
    reg = ValueRegistry(default_values=dict(foo=0))
    
    # ...but we also *have* to pass the registry to the listener.
    lis = PrintingListener(registry=reg)

But maybe you're not big on extending `ValueListener`, and would prefer
just calling methods instead? Go right ahead!

    # We need something to tell the registry "our" identity, so that we
    # can later unregister again, and the registry knows which callbacks
    # not to use anymore. This something can be any hashable object, as
    # long as it is unique.
    token = 0

    my_printer(key, value):
        print(f'{key} -> {value}')
    
    reg.register(token, my_printer, 'foo')


TODO
----

* Packaging
* Emit events (optionally)
* Loading / saving values from / to a file
