"""
Copied from https://github.com/encode/django-rest-framework/issues/1005
This is to support ordering by nested fields without needing to add
custom coding per Model
"""
from typing import List, Tuple
from rest_framework.filters import OrderingFilter
from django.db.models import Field, Model, QuerySet


class RelatedOrderingFilter(OrderingFilter):
    _max_related_depth = 2

    @staticmethod
    def _get_verbose_name(field: Field, non_verbose_name: str) -> str:
        return field.verbose_name \
            if hasattr(field, 'verbose_name') \
            else non_verbose_name.replace('_', ' ')

    def _retrieve_all_related_fields(
            self,
            fields: Tuple[Field],
            model: Model,
            depth: int = 0
    ) -> List[tuple]:
        valid_fields = []
        if depth > self._max_related_depth:
            return valid_fields
        for field in fields:
            if field.related_model and field.related_model != model:
                rel_fields = self._retrieve_all_related_fields(
                    field.related_model._meta.get_fields(),
                    field.related_model,
                    depth + 1
                )
                for rel_field in rel_fields:
                    valid_fields.append((
                        f'{field.name}__{rel_field[0]}',
                        self._get_verbose_name(field, rel_field[1])
                    ))
            else:
                valid_fields.append((
                    field.name,
                    self._get_verbose_name(field, field.name),
                ))
        return valid_fields

    def get_valid_fields(
            self,
            queryset: QuerySet,
            view,
            context: dict = None
    ) -> List[tuple]:
        valid_fields = getattr(view, 'ordering_fields', self.ordering_fields)
        if not valid_fields == '__all_related__':
            if not context:
                context = {}
            valid_fields = super().get_valid_fields(queryset, view, context)
        else:
            valid_fields = [
                *self._retrieve_all_related_fields(
                    queryset.model._meta.get_fields(),
                    queryset.model
                ),
                *[(key, key.title().split('__'))
                    for key in queryset.query.annotations]
            ]
        return valid_fields
