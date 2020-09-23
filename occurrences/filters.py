from django_filters import FilterSet, CharFilter
from occurrences.models import Occurrence


class OccurrenceFilter(FilterSet):
    author = CharFilter(field_name='author__username', lookup_expr='icontains')
    category = CharFilter(field_name='category__type', lookup_expr='icontains')

    class Meta:
        model = Occurrence
        fields = ('author', 'category')
