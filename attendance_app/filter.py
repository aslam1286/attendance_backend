from django.db.models import Q
from django.http import JsonResponse
from django.views import View


class ListFilter(View):
    model = None
    fields = []
    search_fields = []
    ordering = []
    default_sortable_by = 'id'

    args = ()
    kwargs = {}

    def get_queryset(self, request):
        if not self.model:
            raise ValueError('Model should not be none.')
        return self.model.objects.all().values(*self.fields)

    def get_search_results(self, queryset, search_value=None):
        if search_value:
            queries = [Q(**{f + '__icontains': search_value}) for f in self.search_fields]
            q = Q()
            for query in queries:
                q = q | query
            queryset = queryset.filter(q)
        return queryset

    def get_ordering(self, queryset, sortable_by=None, ordering_by='asc'):
        try:
            sortable_by = self.ordering[int(sortable_by)]
        except (IndexError, TypeError, ValueError):
            sortable_by = self.default_sortable_by

        sortable_by = sortable_by if ordering_by == 'asc' else '-' + sortable_by
        queryset = queryset.order_by(sortable_by)
        return queryset

    def filter_queryset(self, request):
        search_value = request.GET.get('sSearch', None)
        sortable_by = request.GET.get('iSortCol_0', None)
        ordering_by = request.GET.get('sSortDir_0', 'asc')

        queryset = self.get_queryset(request)
        queryset = self.get_search_results(queryset, search_value)
        queryset = self.get_ordering(queryset, sortable_by, ordering_by)
        return queryset

    @staticmethod
    def pagination(queryset, page_length, page_start):
        return queryset[page_start:page_start + page_length]

    def get(self, request, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

        records_total = self.get_queryset(request).count()

        queryset = list(self.filter_queryset(request))
        records_filtered = len(queryset)

        page_length = int(request.GET.get('iDisplayLength', 32))
        page_start = int(request.GET.get('iDisplayStart', 0))
        queryset = self.pagination(queryset, page_length, page_start)

        return JsonResponse({
            'recordsTotal': records_total,
            'recordsFiltered': records_filtered,
            'data': queryset
        })
