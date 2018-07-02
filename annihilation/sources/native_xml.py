from annihilation.sources.source import BaseSource, DotPathBasedSourceMixin

import xmltodict
import requests
import logging

logger = logging.getLogger(__name__)


class Xml(DotPathBasedSourceMixin, BaseSource):
    def __init__(self, url, **kwargs):
        super(Xml, self).__init__(**kwargs)
        self._url = url
        try:
            response = requests.get(self._url)
        except requests.RequestException:
            logger.exception()
        self._data = xmltodict.parse(response.content)

    @property
    def walkable_data(self):
        return self._data
