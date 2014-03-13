from django import forms
from django.core.exceptions import ValidationError, MultipleObjectsReturned
from django.forms.models import inlineformset_factory
from django.utils.translation import ugettext_lazy as _
from treebeard.forms import MoveNodeForm, movenodeform_factory

from oscar.core.utils import slugify
from oscar.core.loading import get_class, get_model
from oscar.forms.widgets import ImageInput

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
