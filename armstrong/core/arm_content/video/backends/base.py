from django.template.loader import get_template
from django.template import Context

from .helpers import inject_defaults


class BaseVideoBackend(object):
    type = 'base'
    
    @inject_defaults
    def embed(self, embed, width=None, height=None, layout='default', **kwargs):
        template = get_template('embedded_video/%s/%s.html' % (self.type, layout))
        kwargs['embed'] = embed
        kwargs['width'] = width
        kwargs['height'] = height
        context = Context(kwargs)
        return template.render(context)