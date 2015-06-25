import numpy as np
import pandas as pd

from darkcore import *

df = pd.DataFrame(np.random.randn(3, 3))

class MyApp(Darkcore):

    def get_data(self, params):
        return df

    def get_chart(self, params):
        ax = self.get_data(params).plot(figsize=(4, 3))
        return ax


if __name__ == "__main__":

    app = MyApp('Sample App', use_CDN=True,
                contents = [TabPanel(name='tabgroup',
                    contents=[Tab(id='tab1', name='Tab1', contents='get_data'),
                              Tab(id='tab2', name='Tab2', contents='get_chart')])])
    app.run(port=5024)
