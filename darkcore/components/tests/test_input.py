
import pandas as pd
import pandas.util.testing as tm

import darkcore


class TestInputCommon(tm.TestCase):

    inputs = [darkcore.Checkbox, darkcore.Radio, darkcore.Text]

    def test_validation(self):
        for input in self.inputs:

            # no required attributes
            with tm.assertRaises(ValueError):
                input('contents', x='1')

            # attributes not allowed
            with tm.assertRaises(ValueError):
                input('contents', form='xx')

            with tm.assertRaises(ValueError):
                input('type', form='xx')


class TestCheckbox(tm.TestCase):

    def test_html(self):
        c = darkcore.Checkbox('contents1', name='input1', value='xxx')
        expected = ('<label><input type="checkbox" name="input1" '
                    'value="xxx" form="darkcore">contents1</label>')
        self.assertEqual(c._repr_html_(), expected)


class TestRadio(tm.TestCase):

    def test_html(self):
        c = darkcore.Radio('contents1', name='input1', value='xxx')
        expected = ('<label><input type="radio" name="input1" '
                    'value="xxx" form="darkcore">contents1</label>')
        self.assertEqual(c._repr_html_(), expected)


class TestText(tm.TestCase):

    def test_validation(self):
        with tm.assertRaises(ValueError):
            d = {'class': 1}
            darkcore.Text('contents', **d)

    def test_html(self):
        c = darkcore.Text('contents1', name='input1', value='xxx')
        expected = ('<input type="text" class="form-control" '
                    'name="input1" value="xxx" form="darkcore">')
        self.assertEqual(c._repr_html_(), expected)


if __name__ == '__main__':
    import nose

    nose.runmodule(argv=[__file__, '-vvs', '-x', '--pdb', '--pdb-failure'],
                   # '--with-coverage', '--cover-package=pandas.core'],
                   exit=False)
