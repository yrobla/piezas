import six

from django.core.exceptions import ObjectDoesNotExist
from django.views import generic
from django.db.models import Q
from django.http import HttpResponseRedirect, Http404
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string

from oscar.core.loading import get_classes, get_model
from oscar.views import sort_queryset
from oscar.views.generic import ObjectLookupView

(BrandForm,
 BrandSearchForm,
 ModelForm,
 ModelSearchForm) \
    = get_classes('dashboard.podcatalogue.forms',
                  ('BrandForm',
                   'BrandSearchForm',
                   'ModelForm',
                   'ModelSearchForm'))

Brand = get_model('catalogue', 'Brand')
Model = get_model('catalogue', 'Model')

# brand
class BrandListView(generic.ListView):
    """
    Dashboard view of the brand list.
    Supports the permission-based dashboard.
    """

    template_name = 'dashboard/podcatalogue/brand_list.html'
    model = Brand
    context_object_name = 'brands'
    form_class = BrandSearchForm
    description_template = _(u'Brands %(title_filter)s')
    paginate_by = 20
    recent_brands = 5

    def get_context_data(self, **kwargs):
        ctx = super(BrandListView, self).get_context_data(**kwargs)
        ctx['form'] = self.form
        if 'recently_edited' in self.request.GET:
            ctx['queryset_description'] \
                = _("Last %(num_brands)d edited brands") \
                % {'num_brands': self.recent_brands}
        else:
            ctx['queryset_description'] = self.description

        return ctx

    def get_queryset(self):
        """
        Build the queryset for this list
        """
        queryset = Brand.objects.base_queryset()
        queryset = self.apply_search(queryset)
        queryset = self.apply_ordering(queryset)

        return queryset

    def apply_ordering(self, queryset):
        if 'recently_edited' in self.request.GET:
            # Just show recently edited
            queryset = queryset.order_by('-date_updated')
            queryset = queryset[:self.recent_brands]
        else:
            # Allow sorting when all
            queryset = sort_queryset(queryset, self.request,
                                     ['name'], '-date_created')
        return queryset

    def apply_search(self, queryset):
        """
        Filter the queryset and set the description according to the search
        parameters given
        """
        description_ctx = {'title_filter': ''}

        self.form = self.form_class(self.request.GET)

        if not self.form.is_valid():
            self.description = self.description_template % description_ctx
            return queryset

        data = self.form.cleaned_data

        if data.get('name'):
            queryset = queryset.filter(
                name__icontains=data['name']).distinct()
            description_ctx['name_filter'] = _(
                " including an item with title matching '%s'") % data['name']

        self.description = self.description_template % description_ctx

        return queryset


class BrandListMixin(object):

    def get_success_url(self):
        return reverse("dashboard:catalogue-brand-list")


class BrandCreateView(BrandListMixin, generic.CreateView):
    template_name = 'dashboard/podcatalogue/brand_form.html'
    model = Brand
    form_class = BrandForm

    def get_context_data(self, **kwargs):
        ctx = super(BrandCreateView, self).get_context_data(**kwargs)
        ctx['title'] = _("Add a new brand")
        return ctx

    def get_success_url(self):
        messages.info(self.request, _("Brand created successfully"))
        return super(BrandCreateView, self).get_success_url()

    def get_initial(self):
        # set child category if set in the URL kwargs
        initial = super(BrandCreateView, self).get_initial()
        return initial


class BrandUpdateView(BrandListMixin, generic.UpdateView):
    template_name = 'dashboard/podcatalogue/brand_form.html'
    model = Brand
    form_class = BrandForm

    def get_context_data(self, **kwargs):
        ctx = super(BrandUpdateView, self).get_context_data(**kwargs)
        return ctx

    def get_success_url(self):
        messages.info(self.request, _("Brand updated successfully"))
        return super(BrandUpdateView, self).get_success_url()


class BrandDeleteView(BrandListMixin, generic.DeleteView):
    template_name = 'dashboard/podcatalogue/brand_delete.html'
    model = Brand

    def get_context_data(self, *args, **kwargs):
        ctx = super(BrandDeleteView, self).get_context_data(*args, **kwargs)
        return ctx

    def get_success_url(self):
        messages.info(self.request, _("Brand deleted successfully"))
        return super(BrandDeleteView, self).get_success_url()


class BrandCreateUpdateView(generic.UpdateView):
    """
    Dashboard view that bundles both creating and updating single products.
    Supports the permission-based dashboard.
    """

    template_name = 'dashboard/podcatalogue/brand_update.html'
    model = Brand
    context_object_name = 'brand'

    form_class = BrandForm

    def get_context_data(self, **kwargs):
        ctx = super(BrandCreateUpdateView, self).get_context_data(**kwargs)

        if self.object is None:
            ctx['title'] = _('Create new brand')
        else:
            ctx['title'] = ctx['brand'].name
        return ctx

    def forms_valid(self, form, formsets):
        """
        Save all changes and display a success url.
        """
        if not self.creating:
            # a just created product was already saved in process_all_forms()
            self.object = form.save()

        return HttpResponseRedirect(self.get_success_url())

    def forms_invalid(self, form, formsets):
        # delete the temporary product again
        if self.creating and self.object and self.object.pk is not None:
            self.object.delete()
            self.object = None

        messages.error(self.request,
                       _("Your submitted data was not valid - please "
                         "correct the errors below"))
        ctx = self.get_context_data(form=form, **formsets)
        return self.render_to_response(ctx)

    def get_url_with_querystring(self, url):
        url_parts = [url]
        if self.request.GET.urlencode():
            url_parts += [self.request.GET.urlencode()]
        return "?".join(url_parts)

    def get_object(self, queryset=None):
        """
        This parts allows generic.UpdateView to handle creating products as
        well. The only distinction between an UpdateView and a CreateView
        is that self.object is None. We emulate this behavior.
        Additionally, self.product_class is set.
        """
        self.creating = not 'pk' in self.kwargs
        if not self.creating:
            brand = super(BrandCreateUpdateView, self).get_object(queryset)
            return brand

    def get_success_url(self):
        msg = render_to_string(
            'dashboard/podcatalogue/messages/brand_saved.html',
            {
                'brand': self.object,
                'creating': self.creating,
            })
        messages.success(self.request, msg)
        url = reverse('dashboard:catalogue-brand-list')
        if self.request.POST.get('action') == 'continue':
            url = reverse('dashboard:catalogue-brand',
                          kwargs={"pk": self.object.id})
        return self.get_url_with_querystring(url)

# model
class BrandListMixin(object):

    def get_success_url(self):
        return reverse("dashboard:catalogue-model-list")

class ModelListView(generic.ListView):
    """
    Dashboard view of the brand list.
    Supports the permission-based dashboard.
    """

    template_name = 'dashboard/podcatalogue/model_list.html'
    model = Brand
    context_object_name = 'models'
    form_class = ModelSearchForm
    description_template = _(u'Models %(title_filter)s')
    paginate_by = 20
    recent_models = 5

    def get_context_data(self, **kwargs):
        ctx = super(ModelListView, self).get_context_data(**kwargs)
        ctx['form'] = self.form
        if 'recently_edited' in self.request.GET:
            ctx['queryset_description'] \
                = _("Last %(num_models)d edited models") \
                % {'num_models': self.recent_models}
        else:
            ctx['queryset_description'] = self.description

        return ctx

    def get_queryset(self):
        """
        Build the queryset for this list
        """
        queryset = Model.objects.base_queryset()
        queryset = self.apply_search(queryset)
        queryset = self.apply_ordering(queryset)

        return queryset

    def apply_ordering(self, queryset):
        if 'recently_edited' in self.request.GET:
            # Just show recently edited
            queryset = queryset.order_by('-date_updated')
            queryset = queryset[:self.recent_products]
        else:
            # Allow sorting when all
            queryset = sort_queryset(queryset, self.request,
                                     ['brand', 'name'], '-date_created')
        return queryset

    def apply_search(self, queryset):
        """
        Filter the queryset and set the description according to the search
        parameters given
        """
        description_ctx = {'title_filter': ''}

        self.form = self.form_class(self.request.GET)

        if not self.form.is_valid():
            self.description = self.description_template % description_ctx
            return queryset

        data = self.form.cleaned_data

        if data.get('brand'):
            queryset = queryset.filter(
                name__icontains=data['brand']).distinct()
            description_ctx['brand_filter'] = _(
                " including an item with brand matching '%s'") % data['brand']

        if data.get('name'):
            queryset = queryset.filter(
                name__icontains=data['name']).distinct()
            description_ctx['name_filter'] = _(
                " including an item with title matching '%s'") % data['name']

        self.description = self.description_template % description_ctx

        return queryset

class ModelCreateUpdateView(generic.UpdateView):
    """
    Dashboard view that bundles both creating and updating single products.
    Supports the permission-based dashboard.
    """

    template_name = 'dashboard/podcatalogue/model_update.html'
    model = Model
    context_object_name = 'model'

    form_class = ModelForm

    def get_context_data(self, **kwargs):
        ctx = super(ModelCreateUpdateView, self).get_context_data(**kwargs)

        if self.object is None:
            ctx['title'] = _('Create new model')
        else:
            ctx['title'] = ctx['model'].name
        return ctx

    def forms_valid(self, form, formsets):
        """
        Save all changes and display a success url.
        """
        if not self.creating:
            # a just created product was already saved in process_all_forms()
            self.object = form.save()

        return HttpResponseRedirect(self.get_success_url())

    def forms_invalid(self, form, formsets):
        # delete the temporary product again
        if self.creating and self.object and self.object.pk is not None:
            self.object.delete()
            self.object = None

        messages.error(self.request,
                       _("Your submitted data was not valid - please "
                         "correct the errors below"))
        ctx = self.get_context_data(form=form, **formsets)
        return self.render_to_response(ctx)

    def get_url_with_querystring(self, url):
        url_parts = [url]
        if self.request.GET.urlencode():
            url_parts += [self.request.GET.urlencode()]
        return "?".join(url_parts)

    def get_object(self, queryset=None):
        """
        This parts allows generic.UpdateView to handle creating products as
        well. The only distinction between an UpdateView and a CreateView
        is that self.object is None. We emulate this behavior.
        Additionally, self.product_class is set.
        """
        self.creating = not 'pk' in self.kwargs
        if not self.creating:
            model = super(ModelCreateUpdateView, self).get_object(queryset)
            return model

    def get_success_url(self):
        msg = render_to_string(
            'dashboard/podcatalogue/messages/model_saved.html',
            {
                'model': self.object,
                'creating': self.creating,
            })
        messages.success(self.request, msg)
        url = reverse('dashboard:catalogue-model-list')
        if self.request.POST.get('action') == 'continue':
            url = reverse('dashboard:catalogue-model',
                          kwargs={"pk": self.object.id})
        return self.get_url_with_querystring(url)

class ModelListMixin(object):

    def get_success_url(self):
        return reverse("dashboard:catalogue-model-list")


class ModelCreateView(ModelListMixin, generic.CreateView):
    template_name = 'dashboard/podcatalogue/model_form.html'
    model = Model
    form_class = ModelForm

    def get_context_data(self, **kwargs):
        ctx = super(ModelCreateView, self).get_context_data(**kwargs)
        ctx['title'] = _("Add a new model")
        return ctx

    def get_success_url(self):
        messages.info(self.request, _("Model created successfully"))
        return super(ModelCreateView, self).get_success_url()

    def get_initial(self):
        # set child category if set in the URL kwargs
        initial = super(ModelCreateView, self).get_initial()
        return initial


class ModelUpdateView(ModelListMixin, generic.UpdateView):
    template_name = 'dashboard/podcatalogue/brand_form.html'
    model = Brand
    form_class = BrandForm

    def get_context_data(self, **kwargs):
        ctx = super(BrandUpdateView, self).get_context_data(**kwargs)
        return ctx

    def get_success_url(self):
        messages.info(self.request, _("Brand updated successfully"))
        return super(BrandUpdateView, self).get_success_url()


class ModelDeleteView(ModelListMixin, generic.DeleteView):
    template_name = 'dashboard/podcatalogue/model_delete.html'
    model = Model

    def get_context_data(self, *args, **kwargs):
        ctx = super(ModelDeleteView, self).get_context_data(*args, **kwargs)
        return ctx

    def get_success_url(self):
        messages.info(self.request, _("Model deleted successfully"))
        return super(ModelDeleteView, self).get_success_url()
