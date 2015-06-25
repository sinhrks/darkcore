
import pandas as pd
import pandas.util.testing as tm

import darkcore


class TestImage(tm.TestCase):

    def test_image_detection(self):
        df = pd.DataFrame({'A':[1, 2, 3]})
        ax = df.plot()

        self.assertTrue(darkcore.Image._maybe_image(ax))
        self.assertTrue(darkcore.Image._maybe_image(ax.get_figure()))
        self.assertFalse(darkcore.Image._maybe_image('not_image'))

    def test_image_implement(self):
        df = pd.DataFrame({'A':[1, 2, 3]})
        ax = df.plot(figsize=(3, 3))

        im = darkcore.Image(ax)
        # because output is very long, test the first part
        expected = ('iVBORw0KGgoAAAANSUhEUgAAAPAAAADwCAYAAAA+VemSAAAABHNCSVQICA'
                    'gIfAhkiAAAAAlwSFlzAAAMTQAADE0B0s6tTgAAHf9JREFUeJzt3X9QVNfZ'
                    'B/DvIlA0Cygd47YTaxRNkxiHmVIr0Wga08QfNWgaE0iNdTQaoU6Lbt6JiI'
                    'nBRKLbNpNQG4lKgxJjgpOObKSMq4CR6eiK2gmxo8wI+oczFeJUWJYf6yLs'
                    '+8fN4gK7y+7lnnvOgeczk5nAXvZ+OePDvXvvuecxnDp1ygNCiJQieAcghK'
                    'hHBUyIxKiACZEYFTAhEqMCJkRiVMCESIwKmBCJUQETIjEqYEIkRgVMiMSo')
        self.assertTrue(im.contents_html.startswith(expected))


if __name__ == '__main__':
    import nose

    nose.runmodule(argv=[__file__, '-vvs', '-x', '--pdb', '--pdb-failure'],
                   # '--with-coverage', '--cover-package=pandas.core'],
                   exit=False)
