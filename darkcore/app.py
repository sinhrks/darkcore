
import os

import numpy as np
import pandas as pd

import bottle

from components import Component


current_dir = os.path.dirname(__file__)


class Darkcore(bottle.Bottle):

    def __init__(self, title, contents=[], template='main.tpl'):
        super(Darkcore, self).__init__()

        self.title = title
        if not isinstance(contents, list):
            contents = [contents]
        self.contents = contents

        # attach reference to self
        for c in self.contents:
            c.connect(self, container=None)

        self.template = os.path.join(current_dir, 'views', template)

        self.route('/', callback=self._render)
        self.route('/js/<filename>', callback=self.js_static)
        self.route('/fonts/<filename>', callback=self.fonts_static)
        self.route('/css/<filename>', callback=self.css_static)

    def js_static(self, filename):
        return bottle.static_file(filename, root=os.path.join(current_dir, 'bootstrap', 'js'))

    def fonts_static(self, filename):
        return bottle.static_file(filename, root=os.path.join(current_dir, 'bootstrap', 'fonts'))

    def css_static(self, filename):
        return bottle.static_file(filename, root=os.path.join(current_dir, 'bootstrap', 'css'))

    def _render(self):
        content = [self._render_content(c) for c in self.contents]
        content = ''.join(content)
        return bottle.template(self.template, title=self.title, content=content)

    def _render_content(self, content):
        if isinstance(content, Component):
            return content._repr_html_()
        else:
            return 'UNKNOWN'

    def run(self, reloader=False, **kwargs):
        return super(Darkcore, self).run(reloader=reloader, **kwargs)


