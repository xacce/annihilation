from annihilation.destinations.destination import Destination, LazyM2MActionClassic, BaseSpawnedObject, SpawnableBaseCollection
from distutils.version import StrictVersion


class SpawnedObject(BaseSpawnedObject):
    def __init__(self, model, *args, **kwargs):
        super(SpawnedObject, self).__init__(*args, **kwargs)
        self._instance = model()

    def set(self, k, v):
        setattr(self._instance, k, v)

    def get(self, k):
        return getattr(self._instance, k)

    def set_m2m(self, field_name, instances):
        # TODO This method can using bulk_create with through model
        self._lazy_actions.append(LazyM2MActionClassic(self.out, field_name, instances))

    def get_out_id(self):
        return self._instance.pk

    def set_out_id(self, id):
        self._instance.pk = id

    @property
    def out(self):
        return self._instance


def batch_save(model, spawned_objects):
    """
    Only Django >= 1.10 with postgres returned ids from batch operations
    """
    from django import get_version
    from django.db import router
    from django.db.transaction import get_connection
    if get_connection(router.db_for_write(model.__class__)).vendor == 'postgresql' and StrictVersion(get_version()) >= StrictVersion('1.10'):
        model.objects.bulk_create([x.out for x in spawned_objects])
        for spawned in spawned_objects:
            spawned.save_lazy()
    else:
        for spawned in spawned_objects:
            spawned.out.save()
            spawned.save_lazy()


class Collection(SpawnableBaseCollection):
    def __init__(self, model, unique_field_name):
        self.model = model
        self.unique_field_name = unique_field_name
        super(Collection, self).__init__()

    def _spawn(self, raw_data):
        o = SpawnedObject(self.model, raw_data)
        return o

    def save(self):
        # self.model.objects.all().delete()
        exists = self.model.objects.filter(**{'%s__in' % self.unique_field_name: [x.get(self.unique_field_name) for x in self._spawned]}).values_list(self.unique_field_name, 'pk')
        exists_unique = {x[0]: x[1] for x in exists}
        new_objects = []
        for spawned in self._spawned:
            unique_value = spawned.get(self.unique_field_name)
            if unique_value not in exists_unique:
                new_objects.append(spawned)
            else:
                spawned.set_out_id(exists_unique[unique_value])
        batch_save(self.model, new_objects)


class CurrentEnvironment(Destination):
    def spawn_destination_collection(self, model, unique_field):
        from django.apps import apps
        model = apps.get_model(*model.split('.'))
        return Collection(model, unique_field)
