from annihilation.sources.source import BaseSource, DotPathBasedSourceMixin

import feedparser


class Rss(DotPathBasedSourceMixin, BaseSource):
    def __init__(self, url, **kwargs):
        super(Rss, self).__init__(**kwargs)
        self._url = url
        self._feed = feedparser.parse(self._url)

    @property
    def walkable_data(self):
        return self._feed
