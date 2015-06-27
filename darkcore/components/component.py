
import pandas as pd
import bottle


class Component(object):

    # class name allowed as container (parent)
    _allowed_container = object

    # class name allowed as contents (child)
    _allowed_child = object

    # list of mandatory attribute names
    _attributes_mandatory = []

    # list of prohibited attribute names
    _attributes_prohibited = []

    def __init__(self, contents, **attributes):
        if not isinstance(contents, list):
            # contents must be a list
            contents = [contents]
        self.contents = contents
        for c in self.contents:
            self._validate_child(c)
            if isinstance(c, Component):
                c.container = self
                c._validate_container(self)

        self.attributes = attributes
        self._validate_attributes()

        # Reference to Bottle app. It can be None
        # if no need to retrieve rendering object via app methods
        self.app = None

    def _validate_attributes(self):
        for attr in self._attributes_mandatory:
            if attr not in self.attributes:
                msg = '{0} needs "{1}" attribute'
                raise ValueError(msg.format(self.__class__.__name__, attr))

        for attr in self._attributes_prohibited:
            if attr in self.attributes:
                msg = '{0} cannot accept "{1}" attribute'
                raise ValueError(msg.format(self.__class__.__name__, attr))

    def _validate_container(self, container):
        """Check container (parent) is None or allowed instance"""
        if container is None:
            return container
        elif isinstance(container, self._allowed_container):
            return container
        else:
            msg = '{0} can only take {1} as a container'
            raise ValueError(msg.format(self.__class__.__name__,
                                        self._allowed_contaner))

    def _validate_child(self, child):
        """Check contents (child) is None or allowed instance"""
        if child is None:
            return child
        elif isinstance(child, self._allowed_child):
            return child
        else:
            msg = '{0} can only take {1} as children'
            raise ValueError(msg.format(self.__class__.__name__,
                                        self._allowed_child))

    def connect(self, app):
        """Add reference to app and container"""
        self.app = app
        for c in self.contents:
            if isinstance(c, Component):
                c.connect(app)

    @property
    def _param_args(self):
        """parameters retrieved from request.params"""
        return bottle.request.params.dict

    @property
    def template(self):
        # draw contents as it is
        return '{{ !content }}'

    @property
    def attributes_html(self):
        """Return html representations of attributes in the main tag"""

        # guarantee the attribute sort order
        keys = sorted(pd.compat.iterkeys(self.attributes))
        attrs = ['{0}="{1}"'.format(k, self.attributes[k]) for k in keys]
        return ' '.join(attrs)

    @property
    def contents_html(self):
        """Return html representations of contents between the main tag"""
        contents = [self._render_children(c) for c in self.contents]
        return ' '.join(contents)

    def _render_children(self, content, **kwargs):
        if hasattr(content, 'to_html'):
            if isinstance(content, pd.DataFrame):
                return content.to_html(classes='table table-striped')
            else:
                return content.to_html()
        elif hasattr(content, '_repr_html_'):
            return content._repr_html_(**kwargs)

        elif isinstance(content, pd.compat.string_types):
            if not self.app is None and hasattr(self.app, content):
                c = getattr(self.app, content)(self._param_args)
                return self._render_children(c)
            else:
                return content

        # ToDo: callable

        from darkcore.components.image import Image

        if Image._maybe_image(content):
            return Image(content)._repr_html_()
        else:
            return content

    def _repr_html_(self, **kwargs):
        return bottle.template(self.template, content=self.contents_html,
                               attributes=self.attributes_html, **kwargs)
