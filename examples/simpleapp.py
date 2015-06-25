import numpy as np
import pandas as pd

from darkcore import *


class MyApp(Darkcore):

    def df1(self, params):
        print(params)
        df = pd.DataFrame(np.random.randn(3, 3))
        return df

    def df2(self, params):
        df = pd.DataFrame(np.random.randn(5, 5))
        return df

    def chart(self, params):
        ax = self.df1(params).plot(figsize=(4, 3))
        return ax


if __name__ == "__main__":

    app = MyApp('Sample App', use_CDN=True,
                contents = [
                Text(name='text', contents='textinput'),
                Checkbox(name='check1', contents='check1', value=1),
                Checkbox(name='check2', contents='check2', value=1),
                Radio(name='radio2', contents='radio', value=1),
                List([ListButton('A'), ListButton('B')]),
                TabPanel(name='tabgroup',
                         contents=[Tab(id='tab1', name='Tab1', contents='df1'),
                                   Tab(id='tab2', name='Tab2', contents='df2'),
                                   Tab(id='tab3', name='Tab3', contents='chart')])])
    app.run(port=5020)
