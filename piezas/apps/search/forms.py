import os
from django import forms
from django.forms.extras.widgets import SelectDateWidget
from oscar.core.loading import get_model
from django.core.urlresolvers import reverse
from django.forms.models import formset_factory, inlineformset_factory
from django.forms.formsets import BaseFormSet
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import pgettext_lazy
from django.utils.safestring import mark_safe
from smart_selects.form_fields import ChainedModelChoiceField
from piezas.apps.catalogue import models
from datetime import date

from ajaximage.widgets import AjaxImageEditor as CoreAjaxImageEditor, HTML

class AjaxImageEditor(CoreAjaxImageEditor):
    def render(self, name, value, attrs=None):
        final_attrs = self.build_attrs(attrs)
        element_id = final_attrs.get('id')

        kwargs = {'upload_to': self.upload_to,
                  'max_width': self.max_width,
                  'max_height': self.max_height,
                  'crop': self.crop}

        upload_url = reverse('ajaximage', kwargs=kwargs)
        file_path = value if value else ''

        # use FieldFile.url - get url using storage backend
        file_url = value if value else ''
        if not file_url.startswith('/media/'):
            file_url = '/media/'+file_url

        file_name = os.path.basename(file_url)

        output = HTML.format(upload_url=upload_url,
                             file_url=file_url,
                             file_name=file_name,
                             file_path=file_path,
                             element_id=element_id,
                             name=name)
        return mark_safe(unicode(output))

Product = get_model('catalogue', 'Product')
Brand = get_model('catalogue', 'Brand')
SearchItemRequest = get_model('catalogue', 'SearchItemRequest')
SearchRequest = get_model('catalogue', 'SearchRequest')
Bodywork = get_model('catalogue', 'Bodywork')
Engine = get_model('catalogue', 'Engine')
Piece = get_model('catalogue', 'Product')
Category = get_model('catalogue', 'Category')

class SearchCreationForm(forms.Form):
    brand = forms.ModelChoiceField(label=_('Brand'), required=True, queryset = Brand.objects.all())
    model = ChainedModelChoiceField(label=_('Model'), required=True, app_name='catalogue', model_name='Model', chain_field='brand', model_field='brand', show_all=False, auto_choose=False)
    version = ChainedModelChoiceField(label=_('Version'), required=True, app_name='catalogue', model_name='Version', chain_field='model', model_field='model', show_all=False, auto_choose=False)
    bodywork = forms.ModelChoiceField(label=_('Bodywork'), required=True, queryset = Bodywork.objects.all())
    engine = forms.ModelChoiceField(label=_('Engine'), required=True, queryset = Engine.objects.all())
    frameref = forms.CharField(label=_('Frame reference'), max_length=255, required=False)


class SearchCreationFormItem(forms.Form):
    category = forms.ModelChoiceField(label=_('Category'), required=True, queryset = Category.objects.all(), widget=forms.Select(attrs={'class':'category'}))
    piece = forms.ModelChoiceField(label=_('Product'), required=True, queryset = Product.objects.all(), widget=forms.Select(attrs={'class':'piece'}))
    quantity = forms.IntegerField(label=_('Quantity'), required=True, initial=1)
    picture = forms.ImageField(widget=AjaxImageEditor(upload_to='searchpictures', max_width=800, max_height=600, crop=1))
    comments = forms.CharField(label=_('Comments'), required=False, widget=forms.Textarea(attrs={'style':'height:50px;width:200px'}))


class SearchItemRequestFormSet(BaseFormSet):
    pass


class SearchConfirmForm(forms.Form):
    comments = forms.CharField(label=_('Comments'), required=False, widget=forms.Textarea(attrs={'style':'height:50px;width:200px'}))
    expiration_date = forms.DateField(label=_('Expiration date'), required=False,
        widget=forms.TextInput(attrs={'class':'datepicker'}))

    def clean_expiration_date(self):
        data = self.cleaned_data['expiration_date']
        # check if is greater than today
        if data and data<=date.today():
            raise forms.ValidationError(_('Expiration date must be greater than today'))
        return data

SearchCreationFormSet = formset_factory(SearchCreationFormItem, formset=SearchItemRequestFormSet, extra=10)


class SearchRequestSearchForm(forms.Form):
    date_from = forms.DateField(
        required=False, label=_('From'))
    date_to = forms.DateField(
        required=False, label=_('To'))

    def clean(self):
        if self.is_valid() and not any([self.cleaned_data['date_from'],
                                        self.cleaned_data['date_to']]):
            raise forms.ValidationError(_("At least one field is required."))
        return super(SearchRequestSearchForm, self).clean()

    def description(self):
        """
        Uses the form's data to build a useful description of what orders
        are listed.
        """
        if not self.is_bound or not self.is_valid():
            return _('All search requests')
        else:
            date_from = self.cleaned_data['date_from']
            date_to = self.cleaned_data['date_to']
            return self._searchrequests_description(date_from, date_to)

    def _searchrequests_description(self, date_from, date_to, order_number):
        if date_from and date_to:
            desc = _('Search requests expiring between %(date_from)s and '
                     '%(date_to)s')
        elif date_from:
            desc = _('Search requests expiring since %(date_from)s')
        elif date_to:
            desc = _('Serach requests not expiring until %(date_to)s')
        else:
            return None
        params = {
            'date_from': date_from,
            'date_to': date_to,
        }
        return desc % params

    def get_filters(self):
        date_from = self.cleaned_data['date_from']
        date_to = self.cleaned_data['date_to']
        kwargs = {}
        if date_from and date_to:
            kwargs['expiration_date__range'] = [date_from, date_to]
        elif date_from and not date_to:
            kwargs['expiration_date__gt'] = date_from
        elif not date_from and date_to:
            kwargs['expiration_date__lt'] = date_to
        return kwargs


class QuoteCreationForm(forms.ModelForm):
    class Meta:
        model = SearchRequest
        exclude = ('brand', 'model', 'version', 'bodywork', 'engine', 'frameref', 'comments',
            'expiration_date', 'date_created', 'date_updated', 'state', 'owner')

    quote_comments = forms.CharField(label=_('Comments for the quote'), required=False,
        widget=forms.Textarea())
    warranty_days = forms.IntegerField(label=_('Warranty days'), required=True)
    shipping_days = forms.IntegerField(label=_('Shipping days'), required=True)

class QuoteItemCreationForm(forms.ModelForm):
    class Meta:
        model = SearchItemRequest

    category = forms.ModelChoiceField(label=_('Category'), queryset=models.Category.objects.all(),
        widget=forms.Select(attrs={'readonly':'readonly', 'disabled':'disabled'}))
    piece = forms.ModelChoiceField(label=_('Piece'), queryset=models.Product.objects.all(),
        widget=forms.Select(attrs={'readonly':'readonly', 'disabled':'disabled'}))
    comments = forms.CharField(label=_('Comments'), required=False,
        widget=forms.Textarea(attrs={'readonly':'readonly', 'disabled':'disabled'}))
    quantity = forms.IntegerField(label=_('Quantity'), widget=forms.TextInput(
        attrs={'readonly':'readonly', 'disabled':'disabled'}))
    served_quantity = forms.IntegerField(label=_('Served quantity'), widget=forms.NumberInput(
        attrs={'style':'width:50px;'}))
    base_total = forms.DecimalField(label=_('Base total excluding tax'), decimal_places=2,
        max_digits=12, widget=forms.NumberInput(attrs={'style':'width:100px;'}))
    shipping_total = forms.DecimalField(label=_('Shipping total excluding tax'),
        decimal_places=2, max_digits=12, widget=forms.NumberInput(attrs={'style':'width:100px;'}))
    quote_comments = forms.CharField(label=_('Comments for the quote'), required=False,
        widget=forms.Textarea())


InlineQuoteCreationFormSet = inlineformset_factory(SearchRequest, SearchItemRequest, form=QuoteItemCreationForm, extra=0)
