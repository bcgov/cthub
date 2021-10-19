"""
Manager for Team Model
Further reading:
https://docs.djangoproject.com/en/3.1/topics/db/managers/
"""
from django.db.models import Manager


class TeamManager(Manager):
    """
    This enables us to allow custom queryset, define "natural keys"
    and other things we want to do with the Team model without writing it
    on the serializer or viewset level.
    """
    def get_by_natural_key(self, t_code):
        """
        Allows us to reference a record from the Team Model by team code
        instead of Primary Key.
        Sample use of natural key: allow fixtures to refer to the team code
        instead of the primary key
        """
        return self.get(t_code=t_code)
