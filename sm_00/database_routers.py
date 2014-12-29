from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
 
 
class AppSpecificDBRouter(object):
    def _get_app_name(self):
        if not hasattr(self, 'app_name'):
            raise ImproperlyConfigured("Set `app_name`")
        return self.app_name
 
    def _get_db_name(self):
        if not hasattr(self, 'db_name'):
            raise ImproperlyConfigured("Set `db_name`")
        return self.db_name
 
    def _settings_has_db(self, db_name):
        return db_name in settings.DATABASES
 
    def _get_db(self, model):
        app_name = self._get_app_name()
        db_name = self._get_db_name()
 
        if not self._settings_has_db(db_name):
            return None
        if model._meta.app_label == app_name:
            return db_name
        return None
 
    def db_for_read(self, model, **hints):
        return self._get_db(model)
 
    def db_for_write(self, model, **hints):
        return self._get_db(model)
 
    def allow_relation(self, obj1, obj2, **hints):
        app_name = self._get_app_name()
        db_name = self._get_db_name()
 
        if not self._settings_has_db(db_name):
            return None
        if (obj1._meta.app_label == app_name and
                obj2._meta.app_label == app_name):
            return True
        return None
 
    def allow_syncdb(self, db, model):
        app_name = self._get_app_name()
        db_name = self._get_db_name()
 
        if not self._settings_has_db(db_name):
            return None
        if db == db_name:
            return model._meta.app_label == app_name
        elif model._meta.app_label == app_name:
            return False
        return None

