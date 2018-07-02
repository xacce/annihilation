from annihilation.config_utils import yaml_universal_options, yaml_value_to_args_kwargs
from annihilation.filters import base
import logging

logger = logging.getLogger(__name__)


class FilterCollection:
    def __init__(self, filters):
        self._collection = []
        for options in filters:
            filter_name, filter_options = yaml_universal_options(options)
            if not hasattr(base, filter_name):
                logger.critical('Filter %s not found', filter_name)
            a, kw = yaml_value_to_args_kwargs(filter_options)
            self._collection.append(getattr(base, filter_name)(*a, **kw))

    def pre_check(self, item):
        return all([x.pre_check(item) for x in self._collection])

    def post_check(self, item):
        return all([x.post_check(item) for x in self._collection])

    @property
    def is_empty(self):
        return len(self._collection) == 0
