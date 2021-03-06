
import os

import numpy as np
import pandas as pd

import bottle

from darkcore.components import Component


current_dir = os.path.dirname(__file__)


class Darkcore(bottle.Bottle):

    def __init__(self, title='Darkcore', contents=[],
                 template='main.tpl', use_CDN=False):
        super(Darkcore, self).__init__()

        self.title = title

        self.contents = Component(contents)
        # attach reference to self
        self.contents.connect(self)

        self.template = os.path.join(current_dir, 'views', template)

        self.route('/', callback=self._render)

        self.use_CDN = use_CDN
        if not self.use_CDN:
            self.route('/js/<filename>', callback=self.js_static)
            self.route('/fonts/<filename>', callback=self.fonts_static)
            self.route('/css/<filename>', callback=self.css_static)

    def js_static(self, filename):
        return bottle.static_file(filename, root=os.path.join(current_dir, 'bootstrap', 'js'))

    def fonts_static(self, filename):
        return bottle.static_file(filename, root=os.path.join(current_dir, 'bootstrap', 'fonts'))

    def css_static(self, filename):
        return bottle.static_file(filename, root=os.path.join(current_dir, 'bootstrap', 'css'))

    @property
    def script_html(self):
        if self.use_CDN:
            return """    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css">
    <script src="https://code.jquery.com/jquery-1.11.3.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/js/bootstrap.min.js"></script>"""

        else:
            return """    <link href="/css/bootstrap.min.css" rel="stylesheet">
    <script src="/js/jquery-1.11.3.min.js"></script>
    <script src="/js/bootstrap.min.js"></script>"""

    def _render(self):
        return bottle.template(self.template, title=self.title,
                               script=self.script_html,
                               content=self.contents._repr_html_())

    def run(self, reloader=False, **kwargs):
        return super(Darkcore, self).run(reloader=reloader, **kwargs)


