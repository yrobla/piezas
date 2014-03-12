from django import forms
from django.core.exceptions import ValidationError, MultipleObjectsReturned
from django.forms.models import inlineformset_factory
from django.utils.translation import ugettext_lazy as _
from treebeard.forms import MoveNodeForm, movenodeform_factory

from oscar.core.utils import slugify
from oscar.core.loading import get_class, get_model
from oscar.forms.widgets import ImageInput

Brand = get_model('catalogue', 'Brand')


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
