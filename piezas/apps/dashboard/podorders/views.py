import six

from django.core.urlresolvers import reverse
from django.utils.datastructures import SortedDict
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView
from django.utils.translation import ugettext_lazy as _

from oscar.core.loading import get_model
from oscar.core.utils import format_datetime
from oscar.views import sort_queryset
from oscar.views.generic import BulkEditMixin
from oscar.apps.dashboard.reports.csv_utils import CsvUnicodeWriter

import forms

SearchRequest = get_model('catalogue', 'SearchRequest')

class SearchrequestListView(BulkEditMixin, ListView):
    model = SearchRequest
    context_object_name = 'searchrequests'
    template_name = 'dashboard/orders/searchrequest_list.html'
    form_class = forms.SearchRequestSearchForm
    desc_template = _("%(main_filter)s %(name_filter)s"
                      "%(date_filter)s"
                      "%(state_filter)s")
    paginate_by = 25
    description = ''
    actions = ('download_selected_searchrequests',)
    current_view = 'dashboard:order-searchrequest-list'

    def dispatch(self, request, *args, **kwargs):
        self.base_queryset = SearchRequest._default_manager.all().order_by('-date_created')
        return super(SearchrequestListView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if 'searchrequest_number' in request.GET and request.GET.get(
                'response_format', 'html') == 'html':
            # Redirect to Order detail page if valid order number is given
            try:
                id = request.GET['searchrequest_number']
                if id.isdigit():
                    searchrequest = self.base_queryset.get(
                        id=request.GET['searchrequest_number'])
                else:
                    return super(SearchrequestListView, self).get(request, *args, **kwargs)
            except SearchRequest.DoesNotExist:
                pass
            else:
                url = reverse('dashboard:searchrequest-detail',
                              kwargs={'number': searchrequest.id})
                return HttpResponseRedirect(url)
        return super(SearchrequestListView, self).get(request, *args, **kwargs)

    def get_desc_context(self, data=None):  # noqa (too complex (16))
        """Update the title that describes the queryset"""
        desc_ctx = {
            'main_filter': _('All search requests'),
            'name_filter': '',
            'date_filter': '',
            'state_filter': '',
        }

        if 'searchrequest_state' in self.request.GET:
            state = self.request.GET['searchrequest_state']
            if state.lower() == 'none':
                desc_ctx['main_filter'] = _("Search requests without an state")
            else:
                desc_ctx['main_filter'] = _("Search requests with state '%s'") % state
        if data is None:
            return desc_ctx

        if data['searchrequest_number']:
            desc_ctx['main_filter'] = _('Search requests with number starting with'
                                        ' "%(searchrequest_number)s"') % data

        if data['name']:
            desc_ctx['name_filter'] = _(" with user name matching"
                                        " '%(name)s'") % data

        if data['date_from'] and data['date_to']:
            desc_ctx['date_filter'] \
                = _(" placed between %(start_date)s and %(end_date)s") \
                % {'start_date': format_datetime(data['date_from']),
                   'end_date': format_datetime(data['date_to'])}
        elif data['date_from']:
            desc_ctx['date_filter'] = _(" placed since %s") \
                % format_datetime(data['date_from'])
        elif data['date_to']:
            date_to = data['date_to'] + datetime.timedelta(days=1)
            desc_ctx['date_filter'] = _(" placed before %s") \
                % format_datetime(date_to)

        if data['state']:
            desc_ctx['state_filter'] = _(" with status %(state)s") % data

        return desc_ctx

    def get_queryset(self):
        """
        Build the queryset for this list.
        """
        queryset = sort_queryset(self.base_queryset, self.request,
                                 ['id', ])

        # Look for shortcut query filters
        if 'searchrequest_state' in self.request.GET:
            self.form = self.form_class()
            state = self.request.GET['searchrequest_state']
            if state.lower() == 'none':
                state = None
            self.description = self.desc_template % self.get_desc_context()
            return self.base_queryset.filter(state=state)

        if 'searchrequest_number' not in self.request.GET:
            self.description = self.desc_template % self.get_desc_context()
            self.form = self.form_class()
            return queryset

        self.form = self.form_class(self.request.GET)
        if not self.form.is_valid():
            return queryset

        data = self.form.cleaned_data

        if data['searchrequest_number']:
            queryset = self.base_queryset.filter(
                id__istartswith=data['searchrequest_number'])

        if data['name']:
            # If the value is two words, then assume they are first name and
            # last name
            parts = data['name'].split()

            if len(parts) == 1:
                parts = [data['name'], data['name']]
            else:
                parts = [parts[0], parts[1:]]

            filter = Q(owner__first_name__istartswith=parts[0])
            filter |= Q(owner__last_name__istartswith=parts[1])

            queryset = queryset.filter(filter).distinct()

        if data['date_from'] and data['date_to']:
            # Add 24 hours to make search inclusive
            date_to = data['date_to'] + datetime.timedelta(days=1)
            queryset = queryset.filter(date_created__gte=data['date_from'])
            queryset = queryset.filter(date_created__lt=date_to)
        elif data['date_from']:
            queryset = queryset.filter(date_created__gte=data['date_from'])
        elif data['date_to']:
            date_to = data['date_to'] + datetime.timedelta(days=1)
            queryset = queryset.filter(date_created__lt=date_to)

        if data['state']:
            queryset = queryset.filter(state=data['state'])

        self.description = self.desc_template % self.get_desc_context(data)
        return queryset

    def get_context_data(self, **kwargs):
        ctx = super(SearchrequestListView, self).get_context_data(**kwargs)
        ctx['queryset_description'] = self.description
        ctx['form'] = self.form
        return ctx

    def is_csv_download(self):
        return self.request.GET.get('response_format', None) == 'csv'

    def get_paginate_by(self, queryset):
        return None if self.is_csv_download() else self.paginate_by

    def render_to_response(self, context, **response_kwargs):
        if self.is_csv_download():
            return self.download_selected_searchrequests(
                self.request,
               context['object_list'])
        return super(SearchrequestListView, self).render_to_response(
            context, **response_kwargs)

    def get_download_filename(self, request):
        return 'searchrequests.csv'

    def download_selected_searchrequests(self, request, searchrequests):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=%s' \
            % self.get_download_filename(request)
        writer = CsvUnicodeWriter(response, delimiter=',')

        meta_data = (('id', _('Search request number')),
                     ('num_items', _('Number of items')),
                     ('state', _('Status')),
                     ('search_type', _('Search type')),
                     ('owner', _('Owner')),
                     ('creation_date', _('Creation date')),
                     ('expiration_date', _('Expiration date')),
                     )
        columns = SortedDict()
        for k, v in meta_data:
            columns[k] = v

        writer.writerow(columns.values())
        for searchrequest in searchrequests:
            row = columns.copy()
            row['id'] = searchrequest.id
            row['creation_date'] = format_datetime(searchrequest.date_created, 'DATETIME_FORMAT')
            if searchrequest.expiration_date is not None:
                row['expiration_date'] = format_datetime(searchrequest.expiration_date, 'DATETIME_FORMAT')
            else:
                row['expiration_date'] = ''

            row['state'] = searchrequest.state
            row['search_type'] = searchrequest.search_type
            row['num_items'] = searchrequest.num_items
            row['owner'] = searchrequest.owner.email

            encoded_values = [six.text_type(value).encode('utf8')
                              for value in row.values()]
            writer.writerow(encoded_values)
        return response
