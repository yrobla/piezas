from django import forms
from django.db import models
from django.utils.translation import ugettext_lazy as _

from oscar.core.compat import get_user_model
from oscar.apps.customer.forms import EmailUserCreationForm
from piezas.models import TYPE_CHOICES

User = get_user_model()

class PodEmailUserCreationForm(EmailUserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'type', 'cif', 'promotional_code')

    #type = forms.ChoiceField(_('Customer type'), choices=TYPE_CHOICES)
    #cif = forms.CharField(_('CIF'), max_length=9)
    #promotional_code = forms.CharField(_('Promotional code'), max_length=50)


class ProfileForm(forms.ModelForm):

    type = forms.ChoiceField(label=_('Customer type'), widget=forms.Select(attrs={'readonly':'readonly', 'disabled':'disabled'}), choices=TYPE_CHOICES)
    cif = forms.CharField(label=_('CIF'), widget=forms.TextInput(attrs={'readonly':'readonly', 'disabled':'disabled'}))

    def __init__(self, user, *args, **kwargs):
        self.user = user
        kwargs['instance'] = user
        super(ProfileForm, self).__init__(*args, **kwargs)
        if 'email' in self.fields:
            self.fields['email'].required = True

    def clean_email(self):
        """
        Make sure that the email address is aways unique as it is
        used instead of the username. This is necessary because the
        unique-ness of email addresses is *not* enforced on the model
        level in ``django.contrib.auth.models.User``.
        """
        email = normalise_email(self.cleaned_data['email'])
        if User._default_manager.filter(
                email=email).exclude(id=self.user.id).exists():
            raise ValidationError(
                _("A user with this email address already exists"))
        return email

    class Meta:
        model = User
        exclude = ('username', 'password', 'is_staff', 'is_superuser',
                   'is_active', 'last_login', 'date_joined',
                   'user_permissions', 'groups')
