from django import forms
from django.core.exceptions import ValidationError, MultipleObjectsReturned
from django.forms.models import inlineformset_factory
from django.utils.translation import ugettext_lazy as _
from treebeard.forms import MoveNodeForm, movenodeform_factory

from oscar.core.utils import slugify
from oscar.core.loading import get_class, get_model
from oscar.forms.widgets import ImageInput
from oscar.apps.dashboard.catalogue.forms import _attr_text_field, _attr_textarea_field, \
    _attr_integer_field, _attr_boolean_field, _attr_float_field, _attr_date_field, \
    _attr_option_field, _attr_multi_option_field, _attr_entity_field, _attr_numeric_field, \
    _attr_file_field, _attr_image_field

Product = get_model('catalogue', 'Product')
ProductQuestion = get_model('catalogue', 'ProductQuestion')
Brand = get_model('catalogue', 'Brand')
Model = get_model('catalogue', 'Model')
Version = get_model('catalogue', 'Version')
Bodywork = get_model('catalogue', 'Bodywork')
Engine = get_model('catalogue', 'Engine')


# brand
class BrandForm(forms.ModelForm):
    """
    Form to create a brand
    """
    class Meta:
        model = Brand

    name = forms.CharField(max_length=255, required=True, label=_('Name'))


class BrandSearchForm(forms.Form):
    name = forms.CharField(max_length=255, required=False, label=_('Name'))

    def clean(self):
        cleaned_data = super(BrandSearchForm, self).clean()
        cleaned_data['name'] = cleaned_data['name'].strip()
        return cleaned_data

# model
class ModelForm(forms.ModelForm):
    """
    Form to create a brand
    """
    class Meta:
        model = Model

    brand = forms.ModelChoiceField(required=True, label=_('Brand'), queryset=Brand.objects.all())
    name = forms.CharField(max_length=255, required=True, label=_('Name'))


class ModelSearchForm(forms.Form):
    brand = forms.ModelChoiceField(required=False, label=_('Brand'), queryset=Brand.objects.all())
    name = forms.CharField(max_length=255, required=False, label=_('Name'))

    def clean(self):
        cleaned_data = super(ModelSearchForm, self).clean()
        cleaned_data['name'] = cleaned_data['name'].strip()
        return cleaned_data

# version
class VersionForm(forms.ModelForm):
    """
    Form to create a brand
    """
    class Meta:
        model = Version

    model = forms.ModelChoiceField(required=True, label=_('Model'), queryset=Model.objects.all())
    name = forms.CharField(max_length=255, required=True, label=_('Name'))


class VersionSearchForm(forms.Form):
    model = forms.ModelChoiceField(required=False, label=_('Model'), queryset=Model.objects.all())
    name = forms.CharField(max_length=255, required=False, label=_('Name'))

    def clean(self):
        cleaned_data = super(VersionSearchForm, self).clean()
        cleaned_data['name'] = cleaned_data['name'].strip()
        return cleaned_data

# bodywork
class BodyworkForm(forms.ModelForm):
    """
    Form to create a brand
    """
    class Meta:
        model = Bodywork

    name = forms.CharField(max_length=255, required=True, label=_('Name'))


class BodyworkSearchForm(forms.Form):
    name = forms.CharField(max_length=255, required=False, label=_('Name'))

    def clean(self):
        cleaned_data = super(BodyworkSearchForm, self).clean()
        cleaned_data['name'] = cleaned_data['name'].strip()
        return cleaned_data

# engine
class EngineForm(forms.ModelForm):
    """
    Form to create a brand
    """
    class Meta:
        model = Engine

    name = forms.CharField(max_length=255, required=True, label=_('Name'))


class EngineSearchForm(forms.Form):
    name = forms.CharField(max_length=255, required=False, label=_('Name'))

    def clean(self):
        cleaned_data = super(EngineSearchForm, self).clean()
        cleaned_data['name'] = cleaned_data['name'].strip()
        return cleaned_data

# product
class ProductForm(forms.ModelForm):
    FIELD_FACTORIES = {
        "text": _attr_text_field,
        "richtext": _attr_textarea_field,
        "integer": _attr_integer_field,
        "boolean": _attr_boolean_field,
        "float": _attr_float_field,
        "date": _attr_date_field,
        "option": _attr_option_field,
        "multi_option": _attr_multi_option_field,
        "entity": _attr_entity_field,
        "numeric": _attr_numeric_field,
        "file": _attr_file_field,
        "image": _attr_image_field,
    }

    class Meta:
        model = Product
        exclude = ('slug', 'score', 'product_class',
                   'recommended_products', 'product_options',
                   'attributes', 'categories', 'parent',
                   'related_products', 'is_discountable')

    def __init__(self, product_class, data=None, *args, **kwargs):
        self.product_class = product_class
        super(ProductForm, self).__init__(data, *args, **kwargs)

        # Set the initial value of the is_group field.  This isn't watertight:
        # if the product is intended to be a parent product but doesn't have
        # any variants then we can't distinguish it from a standalone product
        # and this checkbox won't have the right value.  This will be addressed
        # in #693
        instance = kwargs.get('instance', None)
        parent = None
        related_products = None

        if 'title' in self.fields:
            self.fields['title'].widget = forms.TextInput(
                attrs={'autocomplete': 'off'})


    def save(self):
        object = super(ProductForm, self).save(commit=False)
        object.product_class = self.product_class
        object.save()
        self.save_m2m()
        return object

class ProductQuestionForm(forms.ModelForm):
    text = forms.CharField(label=_('Question title'), max_length=255, required=False,
                           widget=forms.TextInput(attrs={'size':255, 'style':'width:250px;'}))
    options = forms.CharField(label=_('Options separated by pipes'), max_length=1024, required=False,
                              widget=forms.TextInput(attrs={'size':500, 'style':'width:750px;'}))

    def clean(self):
        cleaned_data = super(ProductQuestionForm, self).clean()
        if 'text' in cleaned_data and 'type' in cleaned_data and cleaned_data['type']=='list':
            if 'options' not in cleaned_data or not cleaned_data['options']:
                raise forms.ValidationError(_('You must fill the options separated by pipes'))
        return cleaned_data


ProductQuestionsFormSet = inlineformset_factory(
    Product, ProductQuestion, form=ProductQuestionForm, extra=1, fields=('text', 'type', 'options'))
