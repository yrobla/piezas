from django import forms
from django.db import models
from django.utils.translation import ugettext_lazy as _

from oscar.core.compat import get_user_model
from oscar.apps.customer.forms import EmailUserCreationForm
from oscar.apps.customer.utils import normalise_email
from piezas.apps.customuser.models import TYPE_CHOICES
from django_iban.forms import IBANFormField

User = get_user_model()

class PodEmailUserCreationForm(EmailUserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'type', 'cif', 'promotional_code')


class ProfileForm(forms.ModelForm):
    iban = IBANFormField(label=_('Bank number account (IBAN format)'), required=True)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        kwargs['instance'] = user
        super(ProfileForm, self).__init__(*args, **kwargs)
        if 'email' in self.fields:
            self.fields['email'].required = True

        if user and user.type=='customer':
            del self.fields['iban']

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
                   'user_permissions', 'groups', 'email', 'is_validated',
                   'cif', 'type')
