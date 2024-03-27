# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Action(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    type = models.TextField()
    model = models.ForeignKey('ReportCard', models.DO_NOTHING)
    name = models.CharField(max_length=254)
    description = models.TextField(blank=True, null=True)
    parameters = models.TextField(blank=True, null=True)
    parameter_mappings = models.TextField(blank=True, null=True)
    visualization_settings = models.TextField(blank=True, null=True)
    public_uuid = models.CharField(unique=True, max_length=36, blank=True, null=True)
    made_public_by = models.ForeignKey('CoreUser', models.DO_NOTHING, related_name="made_public_actions", blank=True, null=True)
    creator = models.ForeignKey('CoreUser', models.DO_NOTHING, related_name="created_actions", blank=True, null=True)
    archived = models.BooleanField()
    entity_id = models.CharField(unique=True, max_length=21, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'action'


class Activity(models.Model):
    id = models.IntegerField(primary_key=True)
    topic = models.CharField(max_length=32)
    timestamp = models.DateTimeField()
    user = models.ForeignKey('CoreUser', models.DO_NOTHING, blank=True, null=True)
    model = models.CharField(max_length=16, blank=True, null=True)
    model_id = models.IntegerField(blank=True, null=True)
    database_id = models.IntegerField(blank=True, null=True)
    table_id = models.IntegerField(blank=True, null=True)
    custom_id = models.CharField(max_length=48, blank=True, null=True)
    details = models.TextField()

    class Meta:
        managed = False
        db_table = 'activity'


class ApplicationPermissionsRevision(models.Model):
    id = models.IntegerField(primary_key=True)
    before = models.TextField()
    after = models.TextField()
    user = models.ForeignKey('CoreUser', models.DO_NOTHING)
    created_at = models.DateTimeField()
    remark = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'application_permissions_revision'


class BookmarkOrdering(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey('CoreUser', models.DO_NOTHING)
    type = models.CharField(max_length=255)
    item_id = models.IntegerField()
    ordering = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'bookmark_ordering'
        unique_together = (('user', 'type', 'item_id'), ('user', 'ordering'),)


class CardBookmark(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey('CoreUser', models.DO_NOTHING)
    card = models.ForeignKey('ReportCard', models.DO_NOTHING)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'card_bookmark'
        unique_together = (('user', 'card'),)


class CardLabel(models.Model):
    id = models.IntegerField(primary_key=True)
    card = models.ForeignKey('ReportCard', models.DO_NOTHING)
    label = models.ForeignKey('Label', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'card_label'
        unique_together = (('card', 'label'),)


class Collection(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField()
    description = models.TextField(blank=True, null=True)
    color = models.CharField(max_length=7)
    archived = models.BooleanField()
    location = models.CharField(max_length=254)
    personal_owner = models.OneToOneField('CoreUser', models.DO_NOTHING, blank=True, null=True)
    slug = models.CharField(max_length=254)
    namespace = models.CharField(max_length=254, blank=True, null=True)
    authority_level = models.CharField(max_length=255, blank=True, null=True)
    entity_id = models.CharField(unique=True, max_length=21, blank=True, null=True)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'collection'


class CollectionBookmark(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey('CoreUser', models.DO_NOTHING)
    collection = models.ForeignKey(Collection, models.DO_NOTHING)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'collection_bookmark'
        unique_together = (('user', 'collection'),)


class CollectionPermissionGraphRevision(models.Model):
    id = models.IntegerField(primary_key=True)
    before = models.TextField()
    after = models.TextField()
    user = models.ForeignKey('CoreUser', models.DO_NOTHING)
    created_at = models.DateTimeField()
    remark = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'collection_permission_graph_revision'


class ComputationJob(models.Model):
    id = models.IntegerField(primary_key=True)
    creator = models.ForeignKey('CoreUser', models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    type = models.CharField(max_length=254)
    status = models.CharField(max_length=254)
    context = models.TextField(blank=True, null=True)
    ended_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'computation_job'


class ComputationJobResult(models.Model):
    id = models.IntegerField(primary_key=True)
    job = models.ForeignKey(ComputationJob, models.DO_NOTHING)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    permanence = models.CharField(max_length=254)
    payload = models.TextField()

    class Meta:
        managed = False
        db_table = 'computation_job_result'


class CoreSession(models.Model):
    id = models.CharField(primary_key=True, max_length=254)
    user = models.ForeignKey('CoreUser', models.DO_NOTHING)
    created_at = models.DateTimeField()
    anti_csrf_token = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'core_session'


class CoreUser(models.Model):
    id = models.IntegerField(primary_key=True)
    email = models.TextField(unique=True)  # This field type is a guess.
    first_name = models.CharField(max_length=254, blank=True, null=True)
    last_name = models.CharField(max_length=254, blank=True, null=True)
    password = models.CharField(max_length=254, blank=True, null=True)
    password_salt = models.CharField(max_length=254, blank=True, null=True)
    date_joined = models.DateTimeField()
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    is_active = models.BooleanField()
    reset_token = models.CharField(max_length=254, blank=True, null=True)
    reset_triggered = models.BigIntegerField(blank=True, null=True)
    is_qbnewb = models.BooleanField()
    google_auth = models.BooleanField()
    ldap_auth = models.BooleanField()
    login_attributes = models.TextField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    sso_source = models.CharField(max_length=254, blank=True, null=True)
    locale = models.CharField(max_length=5, blank=True, null=True)
    is_datasetnewb = models.BooleanField()
    settings = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'core_user'


class DashboardBookmark(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(CoreUser, models.DO_NOTHING)
    dashboard = models.ForeignKey('ReportDashboard', models.DO_NOTHING)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'dashboard_bookmark'
        unique_together = (('user', 'dashboard'),)


class DashboardFavorite(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(CoreUser, models.DO_NOTHING)
    dashboard = models.ForeignKey('ReportDashboard', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'dashboard_favorite'
        unique_together = (('user', 'dashboard'),)


class DashboardcardSeries(models.Model):
    id = models.IntegerField(primary_key=True)
    dashboardcard = models.ForeignKey('ReportDashboardcard', models.DO_NOTHING)
    card = models.ForeignKey('ReportCard', models.DO_NOTHING)
    position = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'dashboardcard_series'


class DataMigrations(models.Model):
    id = models.CharField(primary_key=True, max_length=254)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'data_migrations'


# class Databasechangelog(models.Model):
#     identifier = models.CharField(max_length=255)
#     author = models.CharField(max_length=255)
#     filename = models.CharField(max_length=255)
#     dateexecuted = models.DateTimeField()
#     orderexecuted = models.IntegerField()
#     exectype = models.CharField(max_length=10)
#     md5sum = models.CharField(max_length=35, blank=True, null=True)
#     description = models.CharField(max_length=255, blank=True, null=True)
#     comments = models.CharField(max_length=255, blank=True, null=True)
#     tag = models.CharField(max_length=255, blank=True, null=True)
#     liquibase = models.CharField(max_length=20, blank=True, null=True)
#     contexts = models.CharField(max_length=255, blank=True, null=True)
#     labels = models.CharField(max_length=255, blank=True, null=True)
#     deployment_id = models.CharField(max_length=10, blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'databasechangelog'
#         unique_together = (('identifier', 'author', 'filename'),)


# class Databasechangeloglock(models.Model):
#     id = models.IntegerField(primary_key=True)
#     locked = models.BooleanField()
#     lockgranted = models.DateTimeField(blank=True, null=True)
#     lockedby = models.CharField(max_length=255, blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'databasechangeloglock'


class Dependency(models.Model):
    id = models.IntegerField(primary_key=True)
    model = models.CharField(max_length=32)
    model_id = models.IntegerField()
    dependent_on_model = models.CharField(max_length=32)
    dependent_on_id = models.IntegerField()
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'dependency'


class Dimension(models.Model):
    id = models.IntegerField(primary_key=True)
    field = models.OneToOneField('MetabaseField', models.DO_NOTHING, related_name="field_dimensions")
    name = models.CharField(max_length=254)
    type = models.CharField(max_length=254)
    human_readable_field = models.ForeignKey('MetabaseField', models.DO_NOTHING, related_name="human_readable_field_dimensions", blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    entity_id = models.CharField(unique=True, max_length=21, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dimension'


class HttpAction(models.Model):
    action = models.OneToOneField(Action, models.DO_NOTHING, primary_key=True)
    template = models.TextField()
    response_handle = models.TextField(blank=True, null=True)
    error_handle = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'http_action'


class ImplicitAction(models.Model):
    action = models.ForeignKey(Action, models.DO_NOTHING)
    kind = models.TextField()

    class Meta:
        managed = False
        db_table = 'implicit_action'


class Label(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=254)
    slug = models.CharField(unique=True, max_length=254)
    icon = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'label'


class LoginHistory(models.Model):
    id = models.IntegerField(primary_key=True)
    timestamp = models.DateTimeField()
    user = models.ForeignKey(CoreUser, models.DO_NOTHING)
    session = models.ForeignKey(CoreSession, models.DO_NOTHING, blank=True, null=True)
    device_id = models.CharField(max_length=36)
    device_description = models.TextField()
    ip_address = models.TextField()

    class Meta:
        managed = False
        db_table = 'login_history'


class MetabaseDatabase(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    name = models.CharField(max_length=254)
    description = models.TextField(blank=True, null=True)
    details = models.TextField()
    engine = models.CharField(max_length=254)
    is_sample = models.BooleanField()
    is_full_sync = models.BooleanField()
    points_of_interest = models.TextField(blank=True, null=True)
    caveats = models.TextField(blank=True, null=True)
    metadata_sync_schedule = models.CharField(max_length=254)
    cache_field_values_schedule = models.CharField(max_length=254)
    timezone = models.CharField(max_length=254, blank=True, null=True)
    is_on_demand = models.BooleanField()
    options = models.TextField(blank=True, null=True)
    auto_run_queries = models.BooleanField()
    refingerprint = models.BooleanField(blank=True, null=True)
    cache_ttl = models.IntegerField(blank=True, null=True)
    initial_sync_status = models.CharField(max_length=32)
    creator = models.ForeignKey(CoreUser, models.DO_NOTHING, blank=True, null=True)
    settings = models.TextField(blank=True, null=True)
    dbms_version = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'metabase_database'


class MetabaseField(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    name = models.CharField(max_length=254)
    base_type = models.CharField(max_length=255)
    semantic_type = models.CharField(max_length=255, blank=True, null=True)
    active = models.BooleanField()
    description = models.TextField(blank=True, null=True)
    preview_display = models.BooleanField()
    position = models.IntegerField()
    table = models.ForeignKey('MetabaseTable', models.DO_NOTHING)
    parent = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)
    display_name = models.CharField(max_length=254, blank=True, null=True)
    visibility_type = models.CharField(max_length=32)
    fk_target_field_id = models.IntegerField(blank=True, null=True)
    last_analyzed = models.DateTimeField(blank=True, null=True)
    points_of_interest = models.TextField(blank=True, null=True)
    caveats = models.TextField(blank=True, null=True)
    fingerprint = models.TextField(blank=True, null=True)
    fingerprint_version = models.IntegerField()
    database_type = models.TextField()
    has_field_values = models.TextField(blank=True, null=True)
    settings = models.TextField(blank=True, null=True)
    database_position = models.IntegerField()
    custom_position = models.IntegerField()
    effective_type = models.CharField(max_length=255, blank=True, null=True)
    coercion_strategy = models.CharField(max_length=255, blank=True, null=True)
    nfc_path = models.CharField(max_length=254, blank=True, null=True)
    database_required = models.BooleanField()
    database_is_auto_increment = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'metabase_field'
        unique_together = (('table', 'parent', 'name'), ('table', 'name'),)


class MetabaseFieldvalues(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    values = models.TextField(blank=True, null=True)
    human_readable_values = models.TextField(blank=True, null=True)
    field = models.ForeignKey(MetabaseField, models.DO_NOTHING)
    has_more_values = models.BooleanField(blank=True, null=True)
    type = models.CharField(max_length=32)
    hash_key = models.TextField(blank=True, null=True)
    last_used_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'metabase_fieldvalues'


class MetabaseTable(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    name = models.CharField(max_length=254)
    description = models.TextField(blank=True, null=True)
    entity_type = models.CharField(max_length=254, blank=True, null=True)
    active = models.BooleanField()
    db = models.ForeignKey(MetabaseDatabase, models.DO_NOTHING)
    display_name = models.CharField(max_length=254, blank=True, null=True)
    visibility_type = models.CharField(max_length=254, blank=True, null=True)
    schema = models.CharField(max_length=254, blank=True, null=True)
    points_of_interest = models.TextField(blank=True, null=True)
    caveats = models.TextField(blank=True, null=True)
    show_in_getting_started = models.BooleanField()
    field_order = models.CharField(max_length=254)
    initial_sync_status = models.CharField(max_length=32)

    class Meta:
        managed = False
        db_table = 'metabase_table'
        unique_together = (('db', 'schema', 'name'), ('db', 'name'),)


class Metric(models.Model):
    id = models.IntegerField(primary_key=True)
    table = models.ForeignKey(MetabaseTable, models.DO_NOTHING)
    creator = models.ForeignKey(CoreUser, models.DO_NOTHING)
    name = models.CharField(max_length=254)
    description = models.TextField(blank=True, null=True)
    archived = models.BooleanField()
    definition = models.TextField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    points_of_interest = models.TextField(blank=True, null=True)
    caveats = models.TextField(blank=True, null=True)
    how_is_this_calculated = models.TextField(blank=True, null=True)
    show_in_getting_started = models.BooleanField()
    entity_id = models.CharField(unique=True, max_length=21, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'metric'


class MetricImportantField(models.Model):
    id = models.IntegerField(primary_key=True)
    metric = models.ForeignKey(Metric, models.DO_NOTHING)
    field = models.ForeignKey(MetabaseField, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'metric_important_field'
        unique_together = (('metric', 'field'),)


class ModerationReview(models.Model):
    id = models.IntegerField(primary_key=True)
    updated_at = models.DateTimeField()
    created_at = models.DateTimeField()
    status = models.CharField(max_length=255, blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    moderated_item_id = models.IntegerField()
    moderated_item_type = models.CharField(max_length=255)
    moderator_id = models.IntegerField()
    most_recent = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'moderation_review'


class NativeQuerySnippet(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(unique=True, max_length=254)
    description = models.TextField(blank=True, null=True)
    content = models.TextField()
    creator = models.ForeignKey(CoreUser, models.DO_NOTHING)
    archived = models.BooleanField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    collection = models.ForeignKey(Collection, models.DO_NOTHING, blank=True, null=True)
    entity_id = models.CharField(unique=True, max_length=21, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'native_query_snippet'


class ParameterCard(models.Model):
    id = models.IntegerField(primary_key=True)
    updated_at = models.DateTimeField()
    created_at = models.DateTimeField()
    card = models.ForeignKey('ReportCard', models.DO_NOTHING)
    parameterized_object_type = models.CharField(max_length=32)
    parameterized_object_id = models.IntegerField()
    parameter_id = models.CharField(max_length=36)
    entity_id = models.CharField(unique=True, max_length=21, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'parameter_card'
        unique_together = (('parameterized_object_id', 'parameterized_object_type', 'parameter_id'),)


class Permissions(models.Model):
    id = models.IntegerField(primary_key=True)
    object = models.CharField(max_length=254)
    group = models.ForeignKey('PermissionsGroup', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'permissions'
        unique_together = (('group', 'object'),)


class PermissionsGroup(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'permissions_group'


class PermissionsGroupMembership(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(CoreUser, models.DO_NOTHING)
    group = models.ForeignKey(PermissionsGroup, models.DO_NOTHING)
    is_group_manager = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'permissions_group_membership'
        unique_together = (('user', 'group'),)


class PermissionsRevision(models.Model):
    id = models.IntegerField(primary_key=True)
    before = models.TextField()
    after = models.TextField()
    user = models.ForeignKey(CoreUser, models.DO_NOTHING)
    created_at = models.DateTimeField()
    remark = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'permissions_revision'


class PersistedInfo(models.Model):
    id = models.IntegerField(primary_key=True)
    database = models.ForeignKey(MetabaseDatabase, models.DO_NOTHING)
    card = models.OneToOneField('ReportCard', models.DO_NOTHING)
    question_slug = models.TextField()
    table_name = models.TextField()
    definition = models.TextField(blank=True, null=True)
    query_hash = models.TextField(blank=True, null=True)
    active = models.BooleanField()
    state = models.TextField()
    refresh_begin = models.DateTimeField()
    refresh_end = models.DateTimeField(blank=True, null=True)
    state_change_at = models.DateTimeField(blank=True, null=True)
    error = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    creator = models.ForeignKey(CoreUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'persisted_info'


class Pulse(models.Model):
    id = models.IntegerField(primary_key=True)
    creator = models.ForeignKey(CoreUser, models.DO_NOTHING)
    name = models.CharField(max_length=254, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    skip_if_empty = models.BooleanField()
    alert_condition = models.CharField(max_length=254, blank=True, null=True)
    alert_first_only = models.BooleanField(blank=True, null=True)
    alert_above_goal = models.BooleanField(blank=True, null=True)
    collection = models.ForeignKey(Collection, models.DO_NOTHING, blank=True, null=True)
    collection_position = models.SmallIntegerField(blank=True, null=True)
    archived = models.BooleanField(blank=True, null=True)
    dashboard = models.ForeignKey('ReportDashboard', models.DO_NOTHING, blank=True, null=True)
    parameters = models.TextField()
    entity_id = models.CharField(unique=True, max_length=21, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pulse'


class PulseCard(models.Model):
    id = models.IntegerField(primary_key=True)
    pulse = models.ForeignKey(Pulse, models.DO_NOTHING)
    card = models.ForeignKey('ReportCard', models.DO_NOTHING)
    position = models.IntegerField()
    include_csv = models.BooleanField()
    include_xls = models.BooleanField()
    dashboard_card = models.ForeignKey('ReportDashboardcard', models.DO_NOTHING, blank=True, null=True)
    entity_id = models.CharField(unique=True, max_length=21, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pulse_card'


class PulseChannel(models.Model):
    id = models.IntegerField(primary_key=True)
    pulse = models.ForeignKey(Pulse, models.DO_NOTHING)
    channel_type = models.CharField(max_length=32)
    details = models.TextField()
    schedule_type = models.CharField(max_length=32)
    schedule_hour = models.IntegerField(blank=True, null=True)
    schedule_day = models.CharField(max_length=64, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    schedule_frame = models.CharField(max_length=32, blank=True, null=True)
    enabled = models.BooleanField()
    entity_id = models.CharField(unique=True, max_length=21, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pulse_channel'


class PulseChannelRecipient(models.Model):
    id = models.IntegerField(primary_key=True)
    pulse_channel = models.ForeignKey(PulseChannel, models.DO_NOTHING)
    user = models.ForeignKey(CoreUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'pulse_channel_recipient'


class QrtzBlobTriggers(models.Model):
    sched_name = models.OneToOneField('QrtzTriggers', models.DO_NOTHING, db_column='sched_name', primary_key=True)
    trigger_name = models.CharField(max_length=200)
    trigger_group = models.CharField(max_length=200)
    blob_data = models.BinaryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'qrtz_blob_triggers'
        unique_together = (('sched_name', 'trigger_name', 'trigger_group'),)


class QrtzCalendars(models.Model):
    sched_name = models.CharField(primary_key=True, max_length=120)
    calendar_name = models.CharField(max_length=200)
    calendar = models.BinaryField()

    class Meta:
        managed = False
        db_table = 'qrtz_calendars'
        unique_together = (('sched_name', 'calendar_name'),)


class QrtzCronTriggers(models.Model):
    sched_name = models.OneToOneField('QrtzTriggers', models.DO_NOTHING, db_column='sched_name', primary_key=True)
    trigger_name = models.CharField(max_length=200)
    trigger_group = models.CharField(max_length=200)
    cron_expression = models.CharField(max_length=120)
    time_zone_id = models.CharField(max_length=80, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'qrtz_cron_triggers'
        unique_together = (('sched_name', 'trigger_name', 'trigger_group'),)


class QrtzFiredTriggers(models.Model):
    sched_name = models.CharField(primary_key=True, max_length=120)
    entry_id = models.CharField(max_length=95)
    trigger_name = models.CharField(max_length=200)
    trigger_group = models.CharField(max_length=200)
    instance_name = models.CharField(max_length=200)
    fired_time = models.BigIntegerField()
    sched_time = models.BigIntegerField(blank=True, null=True)
    priority = models.IntegerField()
    state = models.CharField(max_length=16)
    job_name = models.CharField(max_length=200, blank=True, null=True)
    job_group = models.CharField(max_length=200, blank=True, null=True)
    is_nonconcurrent = models.BooleanField(blank=True, null=True)
    requests_recovery = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'qrtz_fired_triggers'
        unique_together = (('sched_name', 'entry_id'),)


class QrtzJobDetails(models.Model):
    sched_name = models.CharField(primary_key=True, max_length=120)
    job_name = models.CharField(max_length=200)
    job_group = models.CharField(max_length=200)
    description = models.CharField(max_length=250, blank=True, null=True)
    job_class_name = models.CharField(max_length=250)
    is_durable = models.BooleanField()
    is_nonconcurrent = models.BooleanField()
    is_update_data = models.BooleanField()
    requests_recovery = models.BooleanField()
    job_data = models.BinaryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'qrtz_job_details'
        unique_together = (('sched_name', 'job_name', 'job_group'),)


class QrtzLocks(models.Model):
    sched_name = models.CharField(primary_key=True, max_length=120)
    lock_name = models.CharField(max_length=40)

    class Meta:
        managed = False
        db_table = 'qrtz_locks'
        unique_together = (('sched_name', 'lock_name'),)


class QrtzPausedTriggerGrps(models.Model):
    sched_name = models.CharField(primary_key=True, max_length=120)
    trigger_group = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'qrtz_paused_trigger_grps'
        unique_together = (('sched_name', 'trigger_group'),)


class QrtzSchedulerState(models.Model):
    sched_name = models.CharField(primary_key=True, max_length=120)
    instance_name = models.CharField(max_length=200)
    last_checkin_time = models.BigIntegerField()
    checkin_interval = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'qrtz_scheduler_state'
        unique_together = (('sched_name', 'instance_name'),)


class QrtzSimpleTriggers(models.Model):
    sched_name = models.OneToOneField('QrtzTriggers', models.DO_NOTHING, db_column='sched_name', primary_key=True)
    trigger_name = models.CharField(max_length=200)
    trigger_group = models.CharField(max_length=200)
    repeat_count = models.BigIntegerField()
    repeat_interval = models.BigIntegerField()
    times_triggered = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'qrtz_simple_triggers'
        unique_together = (('sched_name', 'trigger_name', 'trigger_group'),)


class QrtzSimpropTriggers(models.Model):
    sched_name = models.OneToOneField('QrtzTriggers', models.DO_NOTHING, db_column='sched_name', primary_key=True)
    trigger_name = models.CharField(max_length=200)
    trigger_group = models.CharField(max_length=200)
    str_prop_1 = models.CharField(max_length=512, blank=True, null=True)
    str_prop_2 = models.CharField(max_length=512, blank=True, null=True)
    str_prop_3 = models.CharField(max_length=512, blank=True, null=True)
    int_prop_1 = models.IntegerField(blank=True, null=True)
    int_prop_2 = models.IntegerField(blank=True, null=True)
    long_prop_1 = models.BigIntegerField(blank=True, null=True)
    long_prop_2 = models.BigIntegerField(blank=True, null=True)
    dec_prop_1 = models.DecimalField(max_digits=13, decimal_places=4, blank=True, null=True)
    dec_prop_2 = models.DecimalField(max_digits=13, decimal_places=4, blank=True, null=True)
    bool_prop_1 = models.BooleanField(blank=True, null=True)
    bool_prop_2 = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'qrtz_simprop_triggers'
        unique_together = (('sched_name', 'trigger_name', 'trigger_group'),)


class QrtzTriggers(models.Model):
    sched_name = models.OneToOneField(QrtzJobDetails, models.DO_NOTHING, db_column='sched_name', primary_key=True)
    trigger_name = models.CharField(max_length=200)
    trigger_group = models.CharField(max_length=200)
    job_name = models.CharField(max_length=200)
    job_group = models.CharField(max_length=200)
    description = models.CharField(max_length=250, blank=True, null=True)
    next_fire_time = models.BigIntegerField(blank=True, null=True)
    prev_fire_time = models.BigIntegerField(blank=True, null=True)
    priority = models.IntegerField(blank=True, null=True)
    trigger_state = models.CharField(max_length=16)
    trigger_type = models.CharField(max_length=8)
    start_time = models.BigIntegerField()
    end_time = models.BigIntegerField(blank=True, null=True)
    calendar_name = models.CharField(max_length=200, blank=True, null=True)
    misfire_instr = models.SmallIntegerField(blank=True, null=True)
    job_data = models.BinaryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'qrtz_triggers'
        unique_together = (('sched_name', 'trigger_name', 'trigger_group'),)


class Query(models.Model):
    query_hash = models.BinaryField(primary_key=True)
    average_execution_time = models.IntegerField()
    query = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'query'


class QueryAction(models.Model):
    action = models.OneToOneField(Action, models.DO_NOTHING, primary_key=True)
    database = models.ForeignKey(MetabaseDatabase, models.DO_NOTHING)
    dataset_query = models.TextField()

    class Meta:
        managed = False
        db_table = 'query_action'


class QueryCache(models.Model):
    query_hash = models.BinaryField(primary_key=True)
    updated_at = models.DateTimeField()
    results = models.BinaryField()

    class Meta:
        managed = False
        db_table = 'query_cache'


class QueryExecution(models.Model):
    id = models.IntegerField(primary_key=True)
    hash = models.BinaryField()
    started_at = models.DateTimeField()
    running_time = models.IntegerField()
    result_rows = models.IntegerField()
    native = models.BooleanField()
    context = models.CharField(max_length=32, blank=True, null=True)
    error = models.TextField(blank=True, null=True)
    executor_id = models.IntegerField(blank=True, null=True)
    card_id = models.IntegerField(blank=True, null=True)
    dashboard_id = models.IntegerField(blank=True, null=True)
    pulse_id = models.IntegerField(blank=True, null=True)
    database_id = models.IntegerField(blank=True, null=True)
    cache_hit = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'query_execution'


class ReportCard(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    name = models.CharField(max_length=254)
    description = models.TextField(blank=True, null=True)
    display = models.CharField(max_length=254)
    dataset_query = models.TextField()
    visualization_settings = models.TextField()
    creator = models.ForeignKey(CoreUser, models.DO_NOTHING, related_name="creator_report_cards")
    database = models.ForeignKey(MetabaseDatabase, models.DO_NOTHING)
    table = models.ForeignKey(MetabaseTable, models.DO_NOTHING, blank=True, null=True)
    query_type = models.CharField(max_length=16, blank=True, null=True)
    archived = models.BooleanField()
    collection = models.ForeignKey(Collection, models.DO_NOTHING, blank=True, null=True)
    public_uuid = models.CharField(unique=True, max_length=36, blank=True, null=True)
    made_public_by = models.ForeignKey(CoreUser, models.DO_NOTHING, blank=True, null=True, related_name="made_public_by_report_cards")
    enable_embedding = models.BooleanField()
    embedding_params = models.TextField(blank=True, null=True)
    cache_ttl = models.IntegerField(blank=True, null=True)
    result_metadata = models.TextField(blank=True, null=True)
    collection_position = models.SmallIntegerField(blank=True, null=True)
    dataset = models.BooleanField()
    entity_id = models.CharField(unique=True, max_length=21, blank=True, null=True)
    parameters = models.TextField(blank=True, null=True)
    parameter_mappings = models.TextField(blank=True, null=True)
    collection_preview = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'report_card'


class ReportCardfavorite(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    card = models.ForeignKey(ReportCard, models.DO_NOTHING)
    owner = models.ForeignKey(CoreUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'report_cardfavorite'
        unique_together = (('card', 'owner'),)


class ReportDashboard(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    name = models.CharField(max_length=254)
    description = models.TextField(blank=True, null=True)
    creator = models.ForeignKey(CoreUser, models.DO_NOTHING, related_name="creator_report_dashboards")
    parameters = models.TextField()
    points_of_interest = models.TextField(blank=True, null=True)
    caveats = models.TextField(blank=True, null=True)
    show_in_getting_started = models.BooleanField()
    public_uuid = models.CharField(unique=True, max_length=36, blank=True, null=True)
    made_public_by = models.ForeignKey(CoreUser, models.DO_NOTHING, related_name="made_public_by_report_dashboards", blank=True, null=True)
    enable_embedding = models.BooleanField()
    embedding_params = models.TextField(blank=True, null=True)
    archived = models.BooleanField()
    position = models.IntegerField(blank=True, null=True)
    collection = models.ForeignKey(Collection, models.DO_NOTHING, blank=True, null=True)
    collection_position = models.SmallIntegerField(blank=True, null=True)
    cache_ttl = models.IntegerField(blank=True, null=True)
    entity_id = models.CharField(unique=True, max_length=21, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'report_dashboard'


class ReportDashboardcard(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    size_x = models.IntegerField()
    size_y = models.IntegerField()
    row = models.IntegerField()
    col = models.IntegerField()
    card = models.ForeignKey(ReportCard, models.DO_NOTHING, blank=True, null=True)
    dashboard = models.ForeignKey(ReportDashboard, models.DO_NOTHING)
    parameter_mappings = models.TextField()
    visualization_settings = models.TextField()
    entity_id = models.CharField(unique=True, max_length=21, blank=True, null=True)
    action = models.ForeignKey(Action, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'report_dashboardcard'


class Revision(models.Model):
    id = models.IntegerField(primary_key=True)
    model = models.CharField(max_length=16)
    model_id = models.IntegerField()
    user = models.ForeignKey(CoreUser, models.DO_NOTHING)
    timestamp = models.DateTimeField()
    object = models.TextField()
    is_reversion = models.BooleanField()
    is_creation = models.BooleanField()
    message = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'revision'


class Sandboxes(models.Model):
    id = models.IntegerField(primary_key=True)
    group = models.ForeignKey(PermissionsGroup, models.DO_NOTHING)
    table = models.ForeignKey(MetabaseTable, models.DO_NOTHING)
    card = models.ForeignKey(ReportCard, models.DO_NOTHING, blank=True, null=True)
    attribute_remappings = models.TextField(blank=True, null=True)
    permission = models.ForeignKey(Permissions, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sandboxes'
        unique_together = (('table', 'group'),)


class Secret(models.Model):
    id = models.IntegerField(primary_key=True)
    version = models.IntegerField()
    creator = models.ForeignKey(CoreUser, models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(blank=True, null=True)
    name = models.CharField(max_length=254)
    kind = models.CharField(max_length=254)
    source = models.CharField(max_length=254, blank=True, null=True)
    value = models.BinaryField()

    class Meta:
        managed = False
        db_table = 'secret'
        unique_together = (('id', 'version'),)


class Segment(models.Model):
    id = models.IntegerField(primary_key=True)
    table = models.ForeignKey(MetabaseTable, models.DO_NOTHING)
    creator = models.ForeignKey(CoreUser, models.DO_NOTHING)
    name = models.CharField(max_length=254)
    description = models.TextField(blank=True, null=True)
    archived = models.BooleanField()
    definition = models.TextField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    points_of_interest = models.TextField(blank=True, null=True)
    caveats = models.TextField(blank=True, null=True)
    show_in_getting_started = models.BooleanField()
    entity_id = models.CharField(unique=True, max_length=21, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'segment'


class Setting(models.Model):
    key = models.CharField(primary_key=True, max_length=254)
    value = models.TextField()

    class Meta:
        managed = False
        db_table = 'setting'


class TaskHistory(models.Model):
    id = models.IntegerField(primary_key=True)
    task = models.CharField(max_length=254)
    db_id = models.IntegerField(blank=True, null=True)
    started_at = models.DateTimeField()
    ended_at = models.DateTimeField()
    duration = models.IntegerField()
    task_details = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'task_history'


class Timeline(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    icon = models.CharField(max_length=128)
    collection = models.ForeignKey(Collection, models.DO_NOTHING, blank=True, null=True)
    archived = models.BooleanField()
    creator = models.ForeignKey(CoreUser, models.DO_NOTHING)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    default = models.BooleanField()
    entity_id = models.CharField(unique=True, max_length=21, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'timeline'


class TimelineEvent(models.Model):
    id = models.IntegerField(primary_key=True)
    timeline = models.ForeignKey(Timeline, models.DO_NOTHING)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    timestamp = models.DateTimeField()
    time_matters = models.BooleanField()
    timezone = models.CharField(max_length=255)
    icon = models.CharField(max_length=128)
    archived = models.BooleanField()
    creator = models.ForeignKey(CoreUser, models.DO_NOTHING)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'timeline_event'


class ViewLog(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(CoreUser, models.DO_NOTHING, blank=True, null=True)
    model = models.CharField(max_length=16)
    model_id = models.IntegerField()
    timestamp = models.DateTimeField()
    metadata = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'view_log'
