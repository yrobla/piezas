from django import forms
from oscar.core.loading import get_model
from django.utils.translation import ugettext_lazy as _
from smart_selects.form_fields import ChainedModelChoiceField

Brand = get_model('catalogue', 'Brand')
SearchProductRequest = get_model('catalogue', 'SearchProductRequest')
Bodywork = get_model('catalogue', 'Bodywork')
Engine = get_model('catalogue', 'Engine')

class SearchCreationForm(forms.ModelForm):
    class Meta:
        model = SearchProductRequest

    brand = forms.ModelChoiceField(label=_('Brand'), required=True, queryset = Brand.objects.all())
    model = ChainedModelChoiceField(label=_('Model'), required=True, app_name='catalogue', model_name='Model', chain_field='brand', model_field='brand', show_all=False, auto_choose=False)
    version = ChainedModelChoiceField(label=_('Version'), required=True, app_name='catalogue', model_name='Version', chain_field='model', model_field='model', show_all=False, auto_choose=False)
    bodywork = forms.ModelChoiceField(label=_('Bodywork'), required=True, queryset = Bodywork.objects.all())
    engine = forms.ModelChoiceField(label=_('Engine'), required=True, queryset = Engine.objects.all())
    frameref = forms.CharField(label=_('Frame reference'), max_length=255, required=False)
    comments = forms.CharField(label=_('Comments'), required=False, widget=forms.Textarea)
