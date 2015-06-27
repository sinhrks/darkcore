
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
        expected = pd.compat.str_to_bytes('iVBORw0KGgoAAAANSUhEUgAAASwAAAEsC'
                                          'AYAAAB5fY51AAAABHNCSVQICAg')
        self.assertTrue(im.contents_html.startswith(expected))


if __name__ == '__main__':
    import nose

    nose.runmodule(argv=[__file__, '-vvs', '-x', '--pdb', '--pdb-failure'],
                   # '--with-coverage', '--cover-package=pandas.core'],
                   exit=False)
