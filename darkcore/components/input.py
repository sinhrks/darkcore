
import pandas as pd

from darkcore.components.component import Component


class Input(Component):
    _attributes_mandatory = ['name']
    _attributes_prohibited = ['type', 'form']


class Checkbox(Input):

    template = """<label><input type="checkbox" {{ !attributes }} form="darkcore">{{ content }}</label>"""


class Radio(Input):

    template = """<label><input type="radio" {{ !attributes }} form="darkcore">{{ content }}</label>"""


class Text(Input):
    _attributes_prohibited = ['type', 'form', 'class']

    template = """<input type="text" class="form-control" {{ !attributes }} form="darkcore">"""

