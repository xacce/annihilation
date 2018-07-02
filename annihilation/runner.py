from itertools import repeat

from annihilation.config_utils import get_yaml_class_instances, get_yaml_config_as_class_object, yaml_universal_options, yaml_value_to_args_kwargs
import logging
import funcsigs

logger = logging.getLogger(__name__)


class AnnihilationRunner:
    def __init__(self, config):
        self._RESERVED_KEYS = ['class']
        self._config = config

    def run(self):
        sources = get_yaml_class_instances(config=self._config['sources'], reserved_fields=self._RESERVED_KEYS)
        self._destinations = get_yaml_class_instances(config=self._config['destinations'], reserved_fields=self._RESERVED_KEYS)
        decomposers = {}

        for decomposer_name, data in self._config['decomposers'].items():
            decomposer_path = data.pop('mapper')
            source_name, source_path = data['source'].split('.', 1)
            source = sources[source_name]
            DecomposerClass = get_yaml_config_as_class_object(decomposer_path)
            if not DecomposerClass:
                continue
            kwargs = dict()
            kwargs['using'] = {}
            kwargs['source'] = list(source.walk(source_path))
            # kwargs['destinations'] = destination.spawn_destination_collection(destination_path, data['unique_field'])
            kwargs['collection'] = self._load_collection(data['destination'])
            for using in data.get('using', []):
                kwargs['using'][using] = decomposers[using]
            for key in list(funcsigs.signature(DecomposerClass.__init__).parameters.keys())[1:]:
                if key not in kwargs and key in data:
                    kwargs[key] = data[key]
            s = DecomposerClass(**kwargs)
            decomposers[decomposer_name] = s
            s.convert()
            logger.info('%s Done.', decomposer_name)

    def _load_collection(self, options):
        name = list(options.keys())[0]
        return self._destinations[name].spawn_destination_collection(**options[name])
