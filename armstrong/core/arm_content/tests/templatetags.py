from ._utils import *
import datetime
from django.db import models
from django import template
from taggit.managers import TaggableManager

from .arm_content_support.models import SimpleVideoModel

from armstrong.core.arm_content.templatetags import content_helpers


class ThumbnailTestCase(ArmContentTestCase):
    def test_thumbnail_filter(self):
        thumb_url = "http://example.com/thumbnail_url.jpg"
        obj = { 'image': "image"}
        t = template.Template("{% load content_helpers %}{{ obj.image|thumbnail:'thumb_size' }}")

        thumbnail_result = fudge.Fake()
        thumbnail_result.has_attr(url=thumb_url)

        get_preset_thumbnail = fudge.Fake()
        get_preset_thumbnail.expects_call().\
                with_args("image", u'thumb_size').\
                returns(thumbnail_result)
        with fudge.patcher.patched_context(content_helpers, 
                    'get_preset_thumbnail',
                    get_preset_thumbnail):
            result = t.render(template.Context({'obj': obj}))
        self.assertEqual(result, thumb_url)
        fudge.verify()


class RenderVideoTestCase(ArmContentTestCase):
    def test_render_video_filter(self):
        obj = SimpleVideoModel(source="http://www.youtube.com/watch?v=oHg5SJYRHA0")
        t = template.Template("{% load content_helpers %}{{ obj.source|render_video:'qvga' }}")
        result = t.render(template.Context({'obj': obj}))
        self.assertEqual(result,
            '<iframe title="YouTube video player" width="320" height="240" '
            'src="http://www.youtube.com/embed/oHg5SJYRHA0" frameborder="0" '
            'allowfullscreen></iframe>')

    def test_render_video_filter_with_args(self):
        obj = SimpleVideoModel(source="http://www.youtube.com/watch?v=oHg5SJYRHA0")
        t = template.Template("{% load content_helpers %}{{ obj.source|render_video:'layout=nonstandard&foo=1&bar=2' }}")
        result = t.render(template.Context({'obj': obj}))
        self.assertEqual(result, u'12')
