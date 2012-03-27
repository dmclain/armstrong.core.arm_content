import urlparse

from django import template
from armstrong.core.arm_content.images.sorl import get_preset_thumbnail
from armstrong.core.arm_content.images.presets import get_preset_args

register = template.Library()


@register.filter
def thumbnail(value, arg):
    return get_preset_thumbnail(value, arg).url

@register.filter
def render_video(value, arg):
    if arg.find('=') == -1:
        args = get_preset_args(arg)
    else:
        args = urlparse.parse_qs(arg)
    return value.backend.embed(value, **args)
