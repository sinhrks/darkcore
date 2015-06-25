
class TestPandasDelegate(tm.TestCase):

    def setUp(self):
        pass

    def test_invalida_delgation(self):
        # these show that in order for the delegation to work
        # the _delegate_* methods need to be overriden to not raise a TypeError

        class Delegator(object):
            _properties = ['foo']
            _methods = ['bar']

            def _set_foo(self, value):
                self.foo = value

            def _get_foo(self):
                return self.foo

            foo = property(_get_foo, _set_foo, doc="foo property")

            def bar(self, *args, **kwargs):
                """ a test bar method """
                pass

        class Delegate(PandasDelegate):
            def __init__(self, obj):
                self.obj = obj
        Delegate._add_delegate_accessors(delegate=Delegator,
                                         accessors=Delegator._properties,
                                         typ='property')
        Delegate._add_delegate_accessors(delegate=Delegator,
                                         accessors=Delegator._methods,
                                         typ='method')

        delegate = Delegate(Delegator())

        def f():
            delegate.foo
        self.assertRaises(TypeError, f)
        def f():
            delegate.foo = 5
        self.assertRaises(TypeError, f)
        def f():
            delegate.foo()
        self.assertRaises(TypeError, f)


if __name__ == '__main__':
    import nose

    nose.runmodule(argv=[__file__, '-vvs', '-x', '--pdb', '--pdb-failure'],
                   # '--with-coverage', '--cover-package=pandas.core'],
                   exit=False)
