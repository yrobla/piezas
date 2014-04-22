import os
from django import forms
from django.core.validators import MinValueValidator
from django.db.models.fields.files import ImageFieldFile
from django.forms.extras.widgets import SelectDateWidget
from oscar.core.loading import get_model
from django.core.urlresolvers import reverse
from django.forms.models import formset_factory, inlineformset_factory, BaseInlineFormSet
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
        if isinstance(value, ImageFieldFile):
            file_url = value.url
        else:
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
    name = forms.CharField(label=_('Search name'), required=False)
    brand = forms.ModelChoiceField(label=_('Brand'), required=True, queryset = Brand.objects.all())
    model = ChainedModelChoiceField(label=_('Model'), required=True, app_name='catalogue', model_name='Model', chain_field='brand', model_field='brand', show_all=False, auto_choose=False)
    version = ChainedModelChoiceField(label=_('Version'), required=True, app_name='catalogue', model_name='Version', chain_field='model', model_field='model', show_all=False, auto_choose=False)
    bodywork = forms.ModelChoiceField(label=_('Bodywork'), required=True, queryset = Bodywork.objects.all())
    engine = forms.ModelChoiceField(label=_('Engine'), required=True, queryset = Engine.objects.all())
    frameref = forms.CharField(label=_('Frame reference'), max_length=255, required=False)

    picture1 = forms.CharField(label=_('Picture #1'),  widget=AjaxImageEditor(upload_to='searchpictures', max_width=800, max_height=600, crop=1), required=False)
    picture2 = forms.CharField(label=_('Picture #2'), widget=AjaxImageEditor(upload_to='searchpictures', max_width=800, max_height=600, crop=1), required=False)
    picture3 = forms.CharField(label=_('Picture #3'), widget=AjaxImageEditor(upload_to='searchpictures', max_width=800, max_height=600, crop=1), required=False)
    picture4 = forms.CharField(label=_('Picture #4'), widget=AjaxImageEditor(upload_to='searchpictures', max_width=800, max_height=600, crop=1), required=False)
    picture5 = forms.CharField(label=_('Picture #5'), widget=AjaxImageEditor(upload_to='searchpictures', max_width=800, max_height=600, crop=1), required=False)
    picture6 = forms.CharField(label=_('Picture #6'), widget=AjaxImageEditor(upload_to='searchpictures', max_width=800, max_height=600, crop=1), required=False)
    picture7 = forms.CharField(label=_('Picture #7'), widget=AjaxImageEditor(upload_to='searchpictures', max_width=800, max_height=600, crop=1), required=False)
    picture8 = forms.CharField(label=_('Picture #8'), widget=AjaxImageEditor(upload_to='searchpictures', max_width=800, max_height=600, crop=1), required=False)
    picture9 = forms.CharField(label=_('Picture #9'), widget=AjaxImageEditor(upload_to='searchpictures', max_width=800, max_height=600, crop=1), required=False)
    picture10 = forms.CharField(label=_('Picture #10'), widget=AjaxImageEditor(upload_to='searchpictures', max_width=800, max_height=600, crop=1), required=False)


class SearchCreationFormItem(forms.Form):
    category = forms.ModelChoiceField(label=_('Category'), required=True, queryset = Category.objects.all(), widget=forms.Select(attrs={'class':'category'}))
    piece = forms.ModelChoiceField(label=_('Product'), required=True, queryset = Product.objects.all(), widget=forms.Select(attrs={'class':'piece'}))
    quantity = forms.IntegerField(label=_('Quantity'), required=True, initial=1)
    picture = forms.ImageField(widget=AjaxImageEditor(upload_to='searchpictures', max_width=800, max_height=600, crop=1), required=False)
    comments = forms.CharField(label=_('Comments'), required=False, widget=forms.Textarea(attrs={'style':'height:50px;width:200px'}))


class SearchItemRequestFormSet(BaseFormSet):
    pass


class SearchConfirmForm(forms.Form):
    comments = forms.CharField(label=_('Comments'), required=False, widget=forms.Textarea(attrs={'style':'height:50px;width:200px'}))

SearchCreationFormSet = formset_factory(SearchCreationFormItem, formset=SearchItemRequestFormSet, extra=50)


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


class QuoteCreationForm(forms.ModelForm):
    class Meta:
        model = SearchRequest
        exclude = ('brand', 'model', 'version', 'bodywork', 'engine', 'frameref', 'comments',
            'date_created', 'date_updated', 'state', 'owner',
            'latitude', 'longitude', 'picture1', 'picture2', 'picture3', 'picture4',
            'picture5', 'picture6', 'picture7', 'picture8', 'picture9', 'picture10')

    quote_comments = forms.CharField(label=_('Comments for the quote'), required=False,
        widget=forms.Textarea())
    warranty_days = forms.IntegerField(label=_('Warranty days'), required=True, validators=[MinValueValidator(0)])
    shipping_days = forms.IntegerField(label=_('Shipping days'), required=True, validators=[MinValueValidator(0)])
    shipping_total_excl_tax = forms.DecimalField(label=_('Shipping total excluding tax'),
        decimal_places=2, max_digits=12, validators=[MinValueValidator(0)], initial=0)

    def clean(self):
        cleaned_data = super(QuoteCreationForm, self).clean()

        # validate formset
        max = self.data['searchitemrequest_set-INITIAL_FORMS']
        for i in range(int(max)):
            original_quantity = self.data['searchitemrequest_set-%d-quantity' % i]
            served_quantity = self.data['searchitemrequest_set-%d-served_quantity' % i]
            base_total = float(self.data['searchitemrequest_set-%d-base_total' % i])
            if not served_quantity.isdigit() or served_quantity<0:
                # error
                raise forms.ValidationError(_('Served quantity must be greater than 0'))
            if served_quantity>original_quantity:
                raise forms.ValidationError(_('Served quantity must be at maximum the requested quantity'))
            if served_quantity>0 and base_total<=0:
                raise forms.ValidationError(_("Base amount for served pieces must be greater than 0. If you don't want to serve this piece, please set the quantity to 0."))

        return cleaned_data
    
class QuoteItemCreationForm(forms.ModelForm):
    class Meta:
        model = SearchItemRequest

    category = forms.CharField(label=_('Category'), required=False,
        widget=forms.TextInput(attrs={'readonly':'readonly'}))
    piece = forms.CharField(label=_('Piece'), required=False,
        widget=forms.TextInput(attrs={'readonly':'readonly'}))
    picture = forms.ImageField(widget=AjaxImageEditor(upload_to='searchpictures',
        max_width=800, max_height=600, crop=1))
    answers = forms.CharField(label=_('Details'), required=False,
        widget=forms.Textarea(attrs={'style':'width:250px;height:200px;','readonly':'readonly'}))
    comments = forms.CharField(label=_('Comments'), required=False,
        widget=forms.Textarea(attrs={'readonly':'readonly'}))
    quantity = forms.IntegerField(label=_('Quantity'),
        widget=forms.TextInput(attrs={'readonly':'readonly'}))
    served_quantity = forms.IntegerField(label=_('Served quantity'), widget=forms.NumberInput(
        attrs={'style':'width:50px;'}))

    served_quantity = forms.IntegerField(label=_('Served quantity'), widget=forms.NumberInput(
        attrs={'style':'width:50px;'}))
    base_total = forms.DecimalField(label=_('Base total excluding tax'), decimal_places=2,
        max_digits=12, widget=forms.NumberInput(attrs={'style':'width:100px;'}), initial=0)
    quote_comments = forms.CharField(label=_('Comments for the quote'), required=False,
        widget=forms.Textarea())
    quote_picture = forms.ImageField(widget=AjaxImageEditor(upload_to='quotepictures',
        max_width=800, max_height=600, crop=1))

InlineQuoteCreationFormSet = inlineformset_factory(SearchRequest, SearchItemRequest, form=QuoteItemCreationForm, extra=0)
