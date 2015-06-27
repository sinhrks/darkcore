
import base64

import pandas as pd

import matplotlib.axes as axes
import matplotlib.figure as figure

from darkcore.components.component import Component


IMAGE_CLASSES = (axes.Axes, figure.Figure)


class Image(Component):

    template = """<img src="data:image/png;base64,{{ content }}" {{ !attributes }}>"""

    # * PIL Image
    # * Pillow Image

    @property
    def contents_html(self):
        if len(self.contents) != 1:
            raise ValueError

        content = self.contents[0]
        if isinstance(content, axes.Axes):
            content = content.get_figure()

        if isinstance(content, figure.Figure):
            buf = pd.compat.BytesIO()
            content.savefig(buf, format='png')
            buf.seek(0)
            data = buf.getvalue()
            data = base64.b64encode(data)
            return data
        else:
            raise ValueError

    @classmethod
    def _maybe_image(cls, content):
        if isinstance(content, IMAGE_CLASSES):
            return True
        return False
