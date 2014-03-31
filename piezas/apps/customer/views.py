from oscar.core.loading import get_class, get_profile_class, get_classes
from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.db.models import get_model
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import logout as auth_logout, login as auth_login
from django.views.generic import (TemplateView, ListView, DetailView,
                                  CreateView, UpdateView, DeleteView,
                                  FormView, RedirectView)
from django.http import HttpResponseRedirect, Http404
from oscar.apps.customer.views import ProfileView as CoreProfileView
from oscar.core.compat import get_user_model
import forms

from piezas.apps.address.forms import UserAddressForm

PageTitleMixin, RegisterUserMixin = get_classes(
    'customer.mixins', ['PageTitleMixin', 'RegisterUserMixin'])
EmailAuthenticationForm, EmailUserCreationForm, ProfileForm = get_classes(
    'customer.forms', ['EmailAuthenticationForm', 'PodEmailUserCreationForm',
                       'ProfileForm'])

ProfileForm = forms.ProfileForm
User = get_user_model()
UserAddress = get_model('address', 'useraddress')

class PodAccountAuthView(RegisterUserMixin, TemplateView):
    """
    This is actually a slightly odd double form view
    """
    template_name = 'customer/login_registration.html'
    login_prefix, registration_prefix = 'login', 'registration'
    login_form_class = EmailAuthenticationForm
    registration_form_class = EmailUserCreationForm
    redirect_field_name = 'next'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
        return super(PodAccountAuthView, self).get(
            request, *args, **kwargs)
    def get_context_data(self, *args, **kwargs):
        ctx = super(PodAccountAuthView, self).get_context_data(*args, **kwargs)
        ctx.update(kwargs)

        # Don't pass request as we don't want to trigger validation of BOTH
        # forms.
        if 'login_form' not in kwargs:
            ctx['login_form'] = self.get_login_form()
        if 'registration_form' not in kwargs:
            ctx['registration_form'] = self.get_registration_form()
        return ctx

    def get_login_form(self, request=None):
        return self.login_form_class(**self.get_login_form_kwargs(request))

    def get_login_form_kwargs(self, request=None):
        kwargs = {}
        kwargs['host'] = self.request.get_host()
        kwargs['prefix'] = self.login_prefix
        kwargs['initial'] = {
            'redirect_url': self.request.GET.get(self.redirect_field_name, ''),
        }
        if request and request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': request.POST,
                'files': request.FILES,
            })
        return kwargs
    def get_registration_form(self, request=None):
        return self.registration_form_class(
            **self.get_registration_form_kwargs(request))

    def get_registration_form_kwargs(self, request=None):
        kwargs = {}
        kwargs['host'] = self.request.get_host()
        kwargs['prefix'] = self.registration_prefix
        kwargs['initial'] = {
            'redirect_url': reverse('customer:profile-update'),
        }
        if request and request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': request.POST,
                'files': request.FILES,
            })
        return kwargs

    def post(self, request, *args, **kwargs):
        # Use the name of the submit button to determine which form to validate
        if u'login_submit' in request.POST:
            return self.validate_login_form()
        elif u'registration_submit' in request.POST:
            return self.validate_registration_form()
        return self.get(request)

    def validate_login_form(self):
        form = self.get_login_form(self.request)
        if form.is_valid():
            auth_login(self.request, form.get_user())
            return HttpResponseRedirect(form.cleaned_data['redirect_url'])
        ctx = self.get_context_data(login_form=form)
        return self.render_to_response(ctx)

    def validate_registration_form(self):
        form = self.get_registration_form(self.request)
        if form.is_valid():
            self.register_user(form)
            return HttpResponseRedirect(form.cleaned_data['redirect_url'])

        ctx = self.get_context_data(registration_form=form)
        return self.render_to_response(ctx)


class ProfileView(CoreProfileView):
    def get_profile_fields(self, user):
        field_data = []

        # Check for custom user model
        for field_name in User._meta.additional_fields:
            if field_name == 'iban' and user.type == 'customer':
                continue

            field_data.append(
                self.get_model_field_data(user, field_name))
        # Check for profile class
        profile_class = get_profile_class()
        if profile_class:
            try:
                profile = profile_class.objects.get(user=user)
            except ObjectDoesNotExist:
                profile = profile_class(user=user)
            field_names = [f.name for f in profile._meta.local_fields]
            for field_name in field_names:
                if field_name in ('user', 'id'):
                    continue
                field_data.append(
                    self.get_model_field_data(profile, field_name))

        return field_data


class ProfileUpdateView(PageTitleMixin, FormView):
    form_class = ProfileForm
    template_name = 'customer/profile/profile_form.html'
    communication_type_code = 'EMAIL_CHANGED'
    page_title = _('Edit Profile')
    active_tab = 'profile'

    def get_form_kwargs(self):
        kwargs = super(ProfileUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        # Grab current user instance before we save form.  We may need this to
        # send a warning email if the email address is changed.
        try:
            old_user = User.objects.get(id=self.request.user.id)
        except User.DoesNotExist:
            old_user = None

        form.save()

        messages.success(self.request, _("Profile updated"))

        # if no address, redirect to new address, if not, redirect to success
        try:
            address = UserAddress.objects.filter(user = self.request.user.id).count()
            if address > 0:
                return HttpResponseRedirect(self.get_success_url())
            else:
                return HttpResponseRedirect(reverse('customer:address-create'))
        except:
            return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('customer:profile-view')

# retrieves shipping address for user, if it has it
def get_shipping_address(user):
    try:
        address = UserAddress.objects.get(user=user, is_default_for_shipping=True)
        return address
    except:
        return None

class AddressCreateView(PageTitleMixin, CreateView):
    form_class = UserAddressForm
    model = UserAddress
    template_name = 'customer/address/address_form.html'
    active_tab = 'addresses'
    page_title = _('Add a new address')

    def get_form_kwargs(self):
        kwargs = super(AddressCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        if get_shipping_address(self.request.user) is None:
            kwargs['initial']['is_default_for_shipping'] = True
        return kwargs

    def get_context_data(self, **kwargs):
        ctx = super(AddressCreateView, self).get_context_data(**kwargs)
        ctx['title'] = _('Add a new address')
        return ctx

    def get_success_url(self):
        messages.success(self.request,
                         _("Address '%s' created") % self.object.summary)
        return reverse('customer:address-list')

