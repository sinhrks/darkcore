
import pandas as pd
from darkcore.components.component import Component


class Input(Component):
    _attributes_mandatory = ['name']
    _attributes_prohibited = ['type', 'form']


class Checkbox(Input):

    template = """
    <input type="checkbox" {{ !attributes }} form="darkcore"> {{ content }}
    """


class Radio(Input):

    template = """
    <input type="radio" {{ !attributes }} form="darkcore"> {{ content }}
    """


class Text(Input):

    template = """
    <input type="text" class="form-control" {{ !attributes }} form="darkcore">
    """