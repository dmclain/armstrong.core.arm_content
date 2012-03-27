import urllib2

from .base import BaseVideoBackend


class VimeoBackend(BaseVideoBackend):
    type = "vimeo"

    def prepare(self, embed):
        if not getattr(embed, "raw_url", False):
            return

        url = urllib2.urlparse.urlparse(embed.raw_url)
        if url.netloc[-9:] != "vimeo.com":
            return

        embed.url = url
        embed.id = url.path.lstrip("/")
        return True
