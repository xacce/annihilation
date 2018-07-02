from functools import partial
from importlib import import_module
from annihilation import tuners
import logging

logger = logging.getLogger(__name__)

RESERVED_SOURCE_CONFIG_KEYS = ['class']


def get_yaml_class_instances(config, reserved_fields=None):
    instances = {}

    for class_id, class_config in config.items():
        instance = get_yaml_config_as_class_instance(class_id, class_config, reserved_fields)
        if instance:
            instances[class_id] = instance
    return instances


def get_yaml_config_as_class_instance(_id, config, reserved_fields=None):
    if reserved_fields is None:
        reserved_fields = []

    SourceClass = get_yaml_config_as_class_object(config['class'])
    if not SourceClass:
        return False
    try:
        source = SourceClass(_id=_id, **dict(filter(lambda x: x[0] not in reserved_fields, config.items())))
    except TypeError as e:
        logger.exception('Not all kwargs provided for source %s', _id)
        return False

    return source


def get_yaml_config_as_class_object(path):
    path, class_name = path.rsplit('.', 1)

    try:
        package = import_module(path)
    except ImportError:
        logger.error('Source %s not found', path)
        return False
    try:
        SourceClass = getattr(package, class_name)
        return SourceClass
    except AttributeError:
        logger.error('Source %s not found in %s', class_name, path)
        return False


def yaml_universal_options(raw_options):
    if isinstance(raw_options, dict):
        key = list(raw_options.keys())[0]
        options = raw_options[key]
    else:
        key = raw_options
        options = []

    return key, options


def yaml_value_to_args_kwargs(value):
    print(value, 3333)
    if isinstance(value, dict):
        return [], value
    if isinstance(value, list):
        a = []
        kw = {}
        for item in value:
            if isinstance(item, dict):
                kw.update(item)
            else:
                a.append(item)
        return a, kw
    return [value], {}


def get_field_name(options):
    return options['from'] if isinstance(options, dict) else options

# def yaml_universal_class_list(self, raw_options):
#     classes = []
#     for raw_option in raw_options:
#         name, options = yaml_universal_options(raw_option)
#         obj = self._resolve_tuner(name)
#         if not fn:
#             continue
#         a, kw = yaml_value_to_args_kwargs(tuner_options)
#
#         self._tuners.append(partial(fn, *a, **kw))
#
#
# def _resolve_tuner(self, tuner_path):
#     # TODO loada user tuners
#     paths = tuner_path.split('.')
#     tuner_fn = getattr(BASE_TUNNERS_LIBRARY, paths[-1], None)
#     if not tuner_fn:
#         logger.critical('Tuner %s not found', tuner_path)
#         return None
#     return tuner_fn
