from django import forms
from django.http import QueryDict
from django.utils.translation import ugettext_lazy as _
from piezas.apps.catalogue.models import SEARCH_REQUEST_STATES, QUOTE_STATES

class SearchRequestSearchForm(forms.Form):
    searchrequest_number = forms.CharField(required=False, label=_("Search request number"))
    name = forms.CharField(required=False, label=_("Owner name"))

    status_choices = (('', '---------'),) + SEARCH_REQUEST_STATES
    state = forms.ChoiceField(choices=status_choices, label=_("Status"),
                               required=False)

    date_from = forms.DateField(required=False, label=_("Date from"))
    date_to = forms.DateField(required=False, label=_("Date to"))

    format_choices = (('html', _('HTML')),
                      ('csv', _('CSV')),)
    response_format = forms.ChoiceField(widget=forms.RadioSelect,
                                        required=False, choices=format_choices,
                                        initial='html',
                                        label=_("Get results as"))

    def __init__(self, *args, **kwargs):
        # ensure that 'response_format' is always set
        if 'data' in kwargs:
            data = kwargs['data']
            del(kwargs['data'])
        elif len(args) > 0:
            data = args[0]
            args = args[1:]
        else:
            data = None

        if data:
            if data.get('response_format', None) not in self.format_choices:
                # handle POST/GET dictionaries, whose are unmutable
                if isinstance(data, QueryDict):
                    data = data.dict()
                data['response_format'] = 'html'

        super(SearchRequestSearchForm, self).__init__(data, *args, **kwargs)


class QuoteSearchForm(forms.Form):
    quote_number = forms.CharField(required=False, label=_("Quote number"))
    name = forms.CharField(required=False, label=_("Owner name"))

    status_choices = (('', '---------'),) + QUOTE_STATES
    state = forms.ChoiceField(choices=status_choices, label=_("Status"),
                               required=False)

    date_from = forms.DateField(required=False, label=_("Date from"))
    date_to = forms.DateField(required=False, label=_("Date to"))

    format_choices = (('html', _('HTML')),
                      ('csv', _('CSV')),)
    response_format = forms.ChoiceField(widget=forms.RadioSelect,
                                        required=False, choices=format_choices,
                                        initial='html',
                                        label=_("Get results as"))

    def __init__(self, *args, **kwargs):
        # ensure that 'response_format' is always set
        if 'data' in kwargs:
            data = kwargs['data']
            del(kwargs['data'])
        elif len(args) > 0:
            data = args[0]
            args = args[1:]
        else:
            data = None

        if data:
            if data.get('response_format', None) not in self.format_choices:
                # handle POST/GET dictionaries, whose are unmutable
                if isinstance(data, QueryDict):
                    data = data.dict()
                data['response_format'] = 'html'

        super(QuoteSearchForm, self).__init__(data, *args, **kwargs)
