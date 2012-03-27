import urllib2

from .base import BaseVideoBackend


class YouTubeBackend(BaseVideoBackend):
    type = "YouTube"

    def prepare(self, embed):
        embed.url = urllib2.urlparse.urlparse(embed.raw_url)
        embed.id = urllib2.urlparse.parse_qs(embed.url.query)['v'][0]
