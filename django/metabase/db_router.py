class MetabaseRouter:

    app_label = "metabase"
    metabase_db = "metabase"

    def db_for_read(self, model, **hints):
        """
        if reading a metabase model, read from the metabase db
        """
        if model._meta.app_label == self.app_label:
            return self.metabase_db
        return None

    def db_for_write(self, model, **hints):
        """
        if writing a metabase model instance, write to the metabase db
        """
        if model._meta.app_label == self.app_label:
            return self.metabase_db
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        if metabase migration, execute on metabase db
        """
        is_metabase_data_migration = hints.get("is_metabase_data_migration", False)
        if app_label == self.app_label:
            if is_metabase_data_migration:
                return True
            return False
        return None