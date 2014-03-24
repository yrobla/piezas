from oscar.apps.dashboard.users.views import IndexView as CoreIndexView
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.translation import ugettext_lazy as _

class IndexView(CoreIndexView):
    actions = ('make_active', 'make_inactive', 'make_valid', 'make_invalid',)
    template_name = 'dashboard/users/index.html'
    checkbox_object_name = 'user'

    def make_valid(self, request, users):
        return self._change_users_valid_status(users, True)

    def make_invalid(self, request, users):
        return self._change_users_valid_status(users, False)

    def _change_users_valid_status(self, users, value):
        for user in users:
            if not user.is_superuser:
                user.is_validated = value
                user.save()
        messages.info(self.request, _("Users' status successfully changed"))
        return HttpResponseRedirect(reverse(self.current_view))
