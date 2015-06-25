
import pandas as pd
import bottle

from darkcore.components.component import Component


class List(Component):

    @property
    def _allowed_child(self):
        return ListButton

    template = """
        <div class="list-group">
         {{ !content }}
        </div>
        """

class ListButton(Component):

    @property
    def _allowed_parent(self):
        return List

    template = """<button type="button" class="list-group-item">{{ !content }}</button>"""


class TabPanel(Component):

    @property
    def _allowed_child(self):
        return Tab

    template = """      <ul {{ !attributes }} class="nav nav-tabs">
        {{ !tabs }}
        </ul>
        <div {{ !attributes }} class="tab-content">
        {{ !content }}
        </div>"""

    def _repr_html_(self):
        active_tab_num = 0
        contents = [c._repr_html_(active_tab_num == i) for i, c in enumerate(self.contents)]
        tabs, contents = zip(*contents)
        tabs = ''.join(tabs)
        contents = ''.join(contents)
        return bottle.template(self.template, tabs=tabs,
                               attributes=self.attributes_html,
                               content=contents)


class Tab(Component):

    @property
    def _allowed_parent(self):
        return TabPanel

    template = """          <div {{ !attributes }} class="{{ active }}" >
            {{ !content }}
            </div>"""

    def _repr_html_(self, active=False):
        if active:
            list_template = """<li class="active"><a href="#{{ id }}" data-toggle="tab">{{ name }}</a></li>"""
            active = 'tab-pane fade in active'
        else:
            list_template = """<li><a href="#{{id}}" data-toggle="tab">{{ name }}</a></li>"""
            active = 'tab-pane fade'

        id = self.attributes.get('id', None) # id must be used in main tab
        name = self.attributes.get('name', None)
        return (bottle.template(list_template, id=id, name=name),
                bottle.template(self.template, attributes=self.attributes_html,
                                content=self.contents_html, active=active))
