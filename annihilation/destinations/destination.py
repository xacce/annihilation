class Destination(object):
    def __init__(self, _id):
        self._id = _id

    @property
    def id(self):
        return self._id


class BaseSpawnedObject(object):
    def __init__(self, raw_data):
        self._raw_data = raw_data
        self._lazy_actions = []

    def get_from_raw(self, k):
        return self._raw_data.get(k)

    def save_lazy(self):
        for action in self._lazy_actions:
            action.run()

    def set(self, k, v):
        raise NotImplementedError()

    def get(self, k):
        raise NotImplementedError()

    def set_m2m(self, field_name, instances):
        raise NotImplementedError()

    def get_out_id(self):
        raise NotImplementedError()

    @property
    def out(self):
        raise NotImplementedError()


class BaseLazyM2MAction(object):
    def run(self):
        raise NotImplementedError()


class LazyM2MActionClassic(BaseLazyM2MAction):
    def __init__(self, out, field, related_instances):
        self._out = out
        self._field = field
        self._related_instances = related_instances

    def run(self):
        getattr(self._out, self._field).add(*[x.get_out_id() for x in self._related_instances])


class BaseCollection(object):
    pass


class SpawnableBaseCollection(BaseCollection):
    def __init__(self):
        self._spawned = []

    def reject(self, spawned_object):
        self._spawned.remove(spawned_object)

    def spawn(self, raw_data):
        spawned = self._spawn(raw_data)
        self._spawned.append(spawned)
        return spawned

    def _spawn(self, raw_data):
        raise NotImplementedError()

    def save(self):
        raise NotImplementedError()

    def _save_lazy(self):
        raise NotImplementedError()

    def __iter__(self):
        for o in self._spawned:
            yield o
