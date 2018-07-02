from annihilation.config_utils import get_field_name
from annihilation.filters.collection import FilterCollection
from annihilation.mappers.field import BaseField
from annihilation.mappers.mapper import Mapper


class Field(BaseField):
    def __init__(self, *args, **kwargs):
        super(Field, self).__init__(*args, **kwargs)
        self._tuners = []
        self._from_field = get_field_name(self._options).split('.')
        if isinstance(self._options, dict) and self._options.get('tuners'):
            self._prepare_tuners(self._options['tuners'])

    def set_value(self, spawned, field_name, source_item):
        value = next(source_item.walk(self._from_field[:]))
        if self._tuners:
            for tuner in self._tuners:
                value = tuner(value=value)

        spawned.set(field_name, value)


class UsingField(BaseField):
    def __init__(self, using, *args, **kwargs):
        super(UsingField, self).__init__(*args, **kwargs)
        self._using = using
        self._query = self._options['query'].split('.')
        self._compare_field = self._options.get('compare_field', self._query[-1])

    def set_value(self, spawned, field_name, source_item):
        ready_items = []
        for using_item in self._using.collection:
            l = using_item.get_from_raw(self._compare_field)
            if not l:
                continue

            for item in source_item.walk(self._query[:]):  # reiterable
                if item == l:
                    ready_items.append(using_item)

        if ready_items:
            getattr(spawned, 'set_{}'.format(self._options['setter']))(field_name, ready_items)


class PredefinedField(BaseField):
    def __init__(self, *args, **kwargs):
        super(PredefinedField, self).__init__(*args, **kwargs)
        self._value = self._options

    def set_value(self, spawned, field_name, source_item):
        spawned.set(field_name, self._value)


class FieldResolver(object):
    def __init__(self, mapping, using=None):
        self._using = using or {}
        self._fields = {}
        for to_field, from_options in mapping.items():
            self._fields[to_field] = self.auto_discover_field(from_options)

    def auto_discover_field(self, options):
        inst = None
        if isinstance(options, dict):
            if options.get('using'):
                inst = UsingField(options=options, using=self._using[options['using']])
            elif options.get('constance'):
                inst = PredefinedField(options=options.get('constance'))
        if not inst:
            inst = Field(options=options)
        return inst

    def apply(self, source_item, spawned):
        for field_name, field in self._fields.items():  # TODO repetative iterator
            field.set_value(spawned, field_name, source_item)


class Assoc(Mapper):
    def __init__(self, source, collection, mapping, filters=None, using=None):
        self._source = source
        self._collection = collection
        self._filters = FilterCollection(filters or [])
        self._mapping = FieldResolver(mapping, using)

    def convert(self):
        has_filters = not self._filters.is_empty
        for item in self._source:
            if has_filters and not self._filters.pre_check(item):
                continue
            spawned = self._collection.spawn(item)
            self._mapping.apply(item, spawned)
            if has_filters and not self._filters.post_check(spawned):
                self._collection.reject(spawned)
        self._collection.save()

    @property
    def source(self):
        return self._source

    @property
    def collection(self):
        return self._collection
