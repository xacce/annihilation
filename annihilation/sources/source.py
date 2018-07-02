from annihilation.utils import walker


class BaseSource(object):
    def __init__(self, _id):
        self._id = _id

    @property
    def id(self):
        return self._id


class DotPathWalkerDict(dict):
    def __init__(self, value):
        if not isinstance(value, dict):
            value = {'non_index_value': value}
        super(DotPathWalkerDict, self).__init__(value)

    def walk(self, paths):
        return walker(paths, self)


class DotPathBasedSourceMixin(object):
    def walk(self, paths):
        for k in walker(paths.split('.'), self.walkable_data):
            yield DotPathWalkerDict(k)

    @property
    def walkable_data(self):
        raise NotImplementedError
