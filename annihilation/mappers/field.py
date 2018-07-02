from functools import partial
from annihilation import tuners as BASE_TUNNERS_LIBRARY

from annihilation.config_utils import yaml_value_to_args_kwargs, yaml_universal_options
import logging

logger = logging.getLogger(__name__)


class BaseField(object):
    # Todo move tuners to mixins
    def __init__(self, options):
        self._options = options

    def _prepare_tuners(self, tuners):
        self._tuners = []
        for options in tuners:
            tuner_name, tuner_options = yaml_universal_options(options)
            fn = self._resolve_tuner(tuner_name)
            if not fn:
                continue
            a, kw = yaml_value_to_args_kwargs(tuner_options)

            self._tuners.append(partial(fn, *a, **kw))

    def _resolve_tuner(self, tuner_path):
        # TODO loada user tuners
        paths = tuner_path.split('.')
        tuner_fn = getattr(BASE_TUNNERS_LIBRARY, paths[-1], None)
        if not tuner_fn:
            logger.critical('Tuner %s not found', tuner_path)
            return None
        return tuner_fn
