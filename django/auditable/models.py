from django.db import models


class Auditable(models.Model):
    """
    Parent model class to provide timestamps and users involved
    in creating and updating the model
    """
    create_timestamp = models.DateTimeField(
        auto_now_add=True, blank=True, null=True
    )
    create_user = models.CharField(
        default="SYSTEM",
        max_length=130
    )
    update_timestamp = models.DateTimeField(
        auto_now=True, blank=True, null=True
    )
    update_user = models.CharField(
        max_length=130,
        null=True
    )

    # Supplemental mapping for base class
    db_column_supplemental_comments = {
        'id': 'Primary key'
    }

    class Meta:
        abstract = True


class Commentable(models.Model):
    """
    Parent model class to just add the comments.
    The Auditable class contains timestamp fields, this one is blank.
    """
    class Meta:
        abstract = True
