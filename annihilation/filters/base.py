import datetime


class Filter:
    def pre_check(self, source_item):
        """
        Filtering native source item (before convertation)
        :param source_item:
        :return:
        """
        return True

    def post_check(self, spawned_object):
        """
        FIltering after convertation
        :param spawned_object:
        :return:
        """
        return True


class required(Filter):
    def __init__(self, *fields):
        self._fields = fields

    def pre_check(self, source_item):
        for field_name in self._fields:
            value = source_item.walk(field_name)
            if not value:
                return False
        return True


class pre_contains(Filter):
    def __init__(self, field, contains):
        self._field = field.split('.')
        self._contains = contains

    def pre_check(self, source_item):
        for value in source_item.walk(self._field[:]):
            if value == self._contains:
                return True
        return False


class timedelta(Filter):
    def __init__(self, field, seconds):
        self._seconds = seconds
        self._stamp = datetime.datetime.now() - datetime.timedelta(seconds=seconds)
        self._field = field

    def post_check(self, spawned_object):
        value = spawned_object.get(self._field)
        if not value:
            return False
        return value > self._stamp
