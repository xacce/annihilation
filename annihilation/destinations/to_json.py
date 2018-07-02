import json

from annihilation.destinations.destination import Destination, BaseSpawnedObject, SpawnableBaseCollection


class SpawnedObject(BaseSpawnedObject):
    def __init__(self, *args, **kwargs):
        super(SpawnedObject, self).__init__(*args, **kwargs)
        self._instance = {}

    def set(self, k, v):
        self._instance[k] = v

    def get(self, k):
        return self._instance[k]

    def set_m2m(self, field_name, instances):
        # TODO This method can using bulk_create with through model
        self._instance[field_name] = [x.out for x in instances]

    def get_out_id(self):
        return None

    @property
    def out(self):
        return self._instance


class Collection(SpawnableBaseCollection):
    def __init__(self, save_path):
        self._save_path = save_path
        super(Collection, self).__init__()

    def _spawn(self, raw_data):
        return SpawnedObject(raw_data)

    def save(self):
        with open(self._save_path, 'w') as f:
            f.write(json.dumps([x.out for x in self._spawned]))

    def _save_lazy(self):
        pass


class ToJson(Destination):
    def spawn_destination_collection(self, path, unique_field):
        return Collection(path)
