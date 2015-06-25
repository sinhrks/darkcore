
import pandas as pd
import pandas.util.testing as tm

import darkcore


class TestList(tm.TestCase):

    def test_validation(self):
        t = darkcore.Text(name='text', contents='input')
        self.assertRaises(ValueError, darkcore.List, name='group', contents=[t])


class TestTab(tm.TestCase):

    def test_validation(self):
        t = darkcore.Text(name='text', contents='input')
        self.assertRaises(ValueError, darkcore.TabPanel, name='group', contents=[t])

        tabs = darkcore.TabPanel(name='group', contents=[darkcore.Tab(name='x', contents='cont1')])
        expected = """      <ul name="group" class="nav nav-tabs">
        <li class="active"><a href="#None" data-toggle="tab">x</a></li>
        </ul>
        <div name="group" class="tab-content">
                  <div name="x" class="tab-pane fade in active" >
            cont1
            </div>
        </div>"""
        self.assertEqual(tabs._repr_html_(), expected)

        tabs = darkcore.TabPanel(name='group', contents=[darkcore.Tab(name='x', contents='cont1'),
                                                         darkcore.Tab(name='y', contents='cont2')])
        expected = """       <ul name="group" class="nav nav-tabs">
        <li class="active"><a href="#None" data-toggle="tab">x</a></li><li><a href="#None" data-toggle="tab">y</a></li>
        </ul>
        <div name="group" class="tab-content">
                  <div name="x" class="tab-pane fade in active" >
            cont1
            </div>          <div name="y" class="tab-pane fade" >
            cont2
            </div>
        </div>"""
        self.assertEqual(tabs._repr_html_(), expected)


if __name__ == '__main__':
    import nose

    nose.runmodule(argv=[__file__, '-vvs', '-x', '--pdb', '--pdb-failure'],
                   # '--with-coverage', '--cover-package=pandas.core'],
                   exit=False)
