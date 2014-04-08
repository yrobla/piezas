import six

from django.core.exceptions import ObjectDoesNotExist
from django.views import generic
from django.db.models import Q
from django.http import HttpResponseRedirect, Http404
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string

from oscar.core.loading import get_class, get_classes, get_model
from oscar.views import sort_queryset
from oscar.views.generic import ObjectLookupView
from oscar.apps.dashboard.catalogue.views import ProductCreateUpdateView as CoreProductCreateUpdateView

from forms import ProductQuestionsFormSet


(	BrandForm,
 BrandSearchForm,
 ModelForm,
 ModelSearchForm,
 VersionForm,
 VersionSearchForm,
 BodyworkForm,
 BodyworkSearchForm,
 EngineForm,
 EngineSearchForm) \
    = get_classes('dashboard.podcatalogue.forms',
                  ('BrandForm',
                   'BrandSearchForm',
                   'ModelForm',
                   'ModelSearchForm',
                   'VersionForm',
                   'VersionSearchForm',
                   'BodyworkForm',
                   'BodyworkSearchForm',
                   'EngineForm',
                   'EngineSearchForm'))

ProductForm = get_class('dashboard.podcatalogue.forms', 'ProductForm')
ProductCategoryFormSet = get_class('dashboard.catalogue.forms', 'ProductCategoryFormSet')
ProductQuestionsFormSet = ProductQuestionsFormSet

Product = get_model('catalogue', 'Product')
ProductQuestion = get_model('catalogue', 'ProductQuestion')
ProductClass = get_model('catalogue', 'ProductClass')
Brand = get_model('catalogue', 'Brand')
Model = get_model('catalogue', 'Model')
Version = get_model('catalogue', 'Version')
Bodywork = get_model('catalogue', 'Bodywork')
Engine = get_model('catalogue', 'Engine')

# brand
class BrandListMixin(object):

    def get_success_url(self):
        return reverse("dashboard:catalogue-brand-list")


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
class ModelListMixin(object):

    def get_success_url(self):
        return reverse("dashboard:catalogue-model-list")

class ModelListView(generic.ListView):
    """
    Dashboard view of the model list.
    Supports the permission-based dashboard.
    """

    template_name = 'dashboard/podcatalogue/model_list.html'
    model = Model
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
            queryset = queryset[:self.recent_models]
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
                brand=data['brand']).distinct()
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
    template_name = 'dashboard/podcatalogue/model_form.html'
    model = Model
    form_class = ModelForm

    def get_context_data(self, **kwargs):
        ctx = super(ModelUpdateView, self).get_context_data(**kwargs)
        return ctx

    def get_success_url(self):
        messages.info(self.request, _("Model updated successfully"))
        return super(ModelUpdateView, self).get_success_url()


class ModelDeleteView(ModelListMixin, generic.DeleteView):
    template_name = 'dashboard/podcatalogue/model_delete.html'
    model = Model

    def get_context_data(self, *args, **kwargs):
        ctx = super(ModelDeleteView, self).get_context_data(*args, **kwargs)
        return ctx

    def get_success_url(self):
        messages.info(self.request, _("Model deleted successfully"))
        return super(ModelDeleteView, self).get_success_url()

# version
class VersionListMixin(object):

    def get_success_url(self):
        return reverse("dashboard:catalogue-version-list")

class VersionListView(generic.ListView):
    """
    Dashboard view of the version list.
    Supports the permission-based dashboard.
    """

    template_name = 'dashboard/podcatalogue/version_list.html'
    model = Version
    context_object_name = 'versions'
    form_class = VersionSearchForm
    description_template = _(u'Versions %(title_filter)s')
    paginate_by = 20
    recent_versions = 5

    def get_context_data(self, **kwargs):
        ctx = super(VersionListView, self).get_context_data(**kwargs)
        ctx['form'] = self.form
        if 'recently_edited' in self.request.GET:
            ctx['queryset_description'] \
                = _("Last %(num_versions)d edited versions") \
                % {'num_versions': self.recent_versions}
        else:
            ctx['queryset_description'] = self.description

        return ctx

    def get_queryset(self):
        """
        Build the queryset for this list
        """
        queryset = Version.objects.base_queryset()
        queryset = self.apply_search(queryset)
        queryset = self.apply_ordering(queryset)

        return queryset

    def apply_ordering(self, queryset):
        if 'recently_edited' in self.request.GET:
            # Just show recently edited
            queryset = queryset.order_by('-date_updated')
            queryset = queryset[:self.recent_versions]
        else:
            # Allow sorting when all
            queryset = sort_queryset(queryset, self.request,
                                     ['model', 'name'], '-date_created')
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

        if data.get('model'):
            queryset = queryset.filter(
                model=data['model']).distinct()
            description_ctx['model_filter'] = _(
                " including an item with model matching '%s'") % data['model']

        if data.get('name'):
            queryset = queryset.filter(
                name__icontains=data['name']).distinct()
            description_ctx['name_filter'] = _(
                " including an item with title matching '%s'") % data['name']

        self.description = self.description_template % description_ctx

        return queryset

class VersionCreateUpdateView(generic.UpdateView):
    """
    Dashboard view that bundles both creating and updating single products.
    Supports the permission-based dashboard.
    """

    template_name = 'dashboard/podcatalogue/version_update.html'
    model = Version
    context_object_name = 'version'

    form_class = VersionForm

    def get_context_data(self, **kwargs):
        ctx = super(VersionCreateUpdateView, self).get_context_data(**kwargs)

        if self.object is None:
            ctx['title'] = _('Create new version')
        else:
            ctx['title'] = ctx['version'].name
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
            model = super(VersionCreateUpdateView, self).get_object(queryset)
            return model

    def get_success_url(self):
        msg = render_to_string(
            'dashboard/podcatalogue/messages/version_saved.html',
            {
                'version': self.object,
                'creating': self.creating,
            })
        messages.success(self.request, msg)
        url = reverse('dashboard:catalogue-version-list')
        if self.request.POST.get('action') == 'continue':
            url = reverse('dashboard:catalogue-version',
                          kwargs={"pk": self.object.id})
        return self.get_url_with_querystring(url)


class VersionCreateView(VersionListMixin, generic.CreateView):
    template_name = 'dashboard/podcatalogue/version_form.html'
    model = Version
    form_class = VersionForm

    def get_context_data(self, **kwargs):
        ctx = super(VersionCreateView, self).get_context_data(**kwargs)
        ctx['title'] = _("Add a new version")
        return ctx

    def get_success_url(self):
        messages.info(self.request, _("Version created successfully"))
        return super(VersionCreateView, self).get_success_url()

    def get_initial(self):
        # set child category if set in the URL kwargs
        initial = super(VersionCreateView, self).get_initial()
        return initial


class VersionUpdateView(VersionListMixin, generic.UpdateView):
    template_name = 'dashboard/podcatalogue/version_form.html'
    model = Version
    form_class = VersionForm

    def get_context_data(self, **kwargs):
        ctx = super(VersionUpdateView, self).get_context_data(**kwargs)
        return ctx

    def get_success_url(self):
        messages.info(self.request, _("Version updated successfully"))
        return super(VersionUpdateView, self).get_success_url()


class VersionDeleteView(VersionListMixin, generic.DeleteView):
    template_name = 'dashboard/podcatalogue/version_delete.html'
    model = Version

    def get_context_data(self, *args, **kwargs):
        ctx = super(VersionDeleteView, self).get_context_data(*args, **kwargs)
        ctx['content'] = ctx['version']
        return ctx

    def get_success_url(self):
        messages.info(self.request, _("Version deleted successfully"))
        return super(VersionDeleteView, self).get_success_url()

# bodywork
class BodyworkListMixin(object):

    def get_success_url(self):
        return reverse("dashboard:catalogue-bodywork-list")

class BodyworkListView(generic.ListView):
    """
    Dashboard view of the version list.
    Supports the permission-based dashboard.
    """

    template_name = 'dashboard/podcatalogue/bodywork_list.html'
    model = Bodywork
    context_object_name = 'bodyworks'
    form_class = BodyworkSearchForm
    description_template = _(u'Bodyworks %(title_filter)s')
    paginate_by = 20
    recent_bodyworks = 5

    def get_context_data(self, **kwargs):
        ctx = super(BodyworkListView, self).get_context_data(**kwargs)
        ctx['form'] = self.form
        if 'recently_edited' in self.request.GET:
            ctx['queryset_description'] \
                = _("Last %(num_bodyworks)d edited bodyworks") \
                % {'num_bodyworks': self.recent_bodyworks}
        else:
            ctx['queryset_description'] = self.description

        return ctx

    def get_queryset(self):
        """
        Build the queryset for this list
        """
        queryset = Bodywork.objects.base_queryset()
        queryset = self.apply_search(queryset)
        queryset = self.apply_ordering(queryset)

        return queryset

    def apply_ordering(self, queryset):
        if 'recently_edited' in self.request.GET:
            # Just show recently edited
            queryset = queryset.order_by('-date_updated')
            queryset = queryset[:self.recent_bodyworks]
        else:
            # Allow sorting when all
            queryset = sort_queryset(queryset, self.request,
                                     ['name',], '-date_created')
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

class BodyworkCreateUpdateView(generic.UpdateView):
    """
    Dashboard view that bundles both creating and updating single products.
    Supports the permission-based dashboard.
    """

    template_name = 'dashboard/podcatalogue/bodywork_update.html'
    model = Bodywork
    context_object_name = 'bodywork'

    form_class = BodyworkForm

    def get_context_data(self, **kwargs):
        ctx = super(BodyworkCreateUpdateView, self).get_context_data(**kwargs)

        if self.object is None:
            ctx['title'] = _('Create new bodywork')
        else:
            ctx['title'] = ctx['bodywork'].name
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
            model = super(BodyworkCreateUpdateView, self).get_object(queryset)
            return model

    def get_success_url(self):
        msg = render_to_string(
            'dashboard/podcatalogue/messages/bodywork_saved.html',
            {
                'bodywork': self.object,
                'creating': self.creating,
            })
        messages.success(self.request, msg)
        url = reverse('dashboard:catalogue-bodywork-list')
        if self.request.POST.get('action') == 'continue':
            url = reverse('dashboard:catalogue-bodywork',
                          kwargs={"pk": self.object.id})
        return self.get_url_with_querystring(url)


class BodyworkCreateView(BodyworkListMixin, generic.CreateView):
    template_name = 'dashboard/podcatalogue/bodywork_form.html'
    model = Bodywork
    form_class = BodyworkForm

    def get_context_data(self, **kwargs):
        ctx = super(BodyworkCreateView, self).get_context_data(**kwargs)
        ctx['title'] = _("Add a new bodywork")
        return ctx

    def get_success_url(self):
        messages.info(self.request, _("Bodywork created successfully"))
        return super(BodyworkCreateView, self).get_success_url()

    def get_initial(self):
        # set child category if set in the URL kwargs
        initial = super(BodyworkCreateView, self).get_initial()
        return initial


class BodyworkUpdateView(BodyworkListMixin, generic.UpdateView):
    template_name = 'dashboard/podcatalogue/bodywork_form.html'
    model = Bodywork
    form_class = BodyworkForm

    def get_context_data(self, **kwargs):
        ctx = super(BodyworkUpdateView, self).get_context_data(**kwargs)
        return ctx

    def get_success_url(self):
        messages.info(self.request, _("Bodywork updated successfully"))
        return super(BodyworkUpdateView, self).get_success_url()


class BodyworkDeleteView(BodyworkListMixin, generic.DeleteView):
    template_name = 'dashboard/podcatalogue/bodywork_delete.html'
    model = Bodywork

    def get_context_data(self, *args, **kwargs):
        ctx = super(BodyworkDeleteView, self).get_context_data(*args, **kwargs)
        return ctx

    def get_success_url(self):
        messages.info(self.request, _("Bodywork deleted successfully"))
        return super(BodyworkDeleteView, self).get_success_url()

# engine
class EngineListMixin(object):

    def get_success_url(self):
        return reverse("dashboard:catalogue-engine-list")

class EngineListView(generic.ListView):
    """
    Dashboard view of the version list.
    Supports the permission-based dashboard.
    """

    template_name = 'dashboard/podcatalogue/engine_list.html'
    model = Engine
    context_object_name = 'engines'
    form_class = EngineSearchForm
    description_template = _(u'Engines %(title_filter)s')
    paginate_by = 20
    recent_engines = 5

    def get_context_data(self, **kwargs):
        ctx = super(EngineListView, self).get_context_data(**kwargs)
        ctx['form'] = self.form
        if 'recently_edited' in self.request.GET:
            ctx['queryset_description'] \
                = _("Last %(num_engines)d edited engines") \
                % {'num_engines': self.recent_engines}
        else:
            ctx['queryset_description'] = self.description

        return ctx

    def get_queryset(self):
        """
        Build the queryset for this list
        """
        queryset = Engine.objects.base_queryset()
        queryset = self.apply_search(queryset)
        queryset = self.apply_ordering(queryset)

        return queryset

    def apply_ordering(self, queryset):
        if 'recently_edited' in self.request.GET:
            # Just show recently edited
            queryset = queryset.order_by('-date_updated')
            queryset = queryset[:self.recent_engines]
        else:
            # Allow sorting when all
            queryset = sort_queryset(queryset, self.request,
                                     ['name',], '-date_created')
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

class EngineCreateUpdateView(generic.UpdateView):
    """
    Dashboard view that bundles both creating and updating single products.
    Supports the permission-based dashboard.
    """

    template_name = 'dashboard/podcatalogue/engine_update.html'
    model = Engine
    context_object_name = 'engine'

    form_class = EngineForm

    def get_context_data(self, **kwargs):
        ctx = super(EngineCreateUpdateView, self).get_context_data(**kwargs)

        if self.object is None:
            ctx['title'] = _('Create new engine')
        else:
            ctx['title'] = ctx['engine'].name
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
            model = super(EngineCreateUpdateView, self).get_object(queryset)
            return model

    def get_success_url(self):
        msg = render_to_string(
            'dashboard/podcatalogue/messages/engine_saved.html',
            {
                'engine': self.object,
                'creating': self.creating,
            })
        messages.success(self.request, msg)
        url = reverse('dashboard:catalogue-engine-list')
        if self.request.POST.get('action') == 'continue':
            url = reverse('dashboard:catalogue-engine',
                          kwargs={"pk": self.object.id})
        return self.get_url_with_querystring(url)


class EngineCreateView(EngineListMixin, generic.CreateView):
    template_name = 'dashboard/podcatalogue/engine_form.html'
    model = Engine
    form_class = EngineForm

    def get_context_data(self, **kwargs):
        ctx = super(EngineCreateView, self).get_context_data(**kwargs)
        ctx['title'] = _("Add a new engine")
        return ctx

    def get_success_url(self):
        messages.info(self.request, _("Engine created successfully"))
        return super(EngineCreateView, self).get_success_url()

    def get_initial(self):
        # set child category if set in the URL kwargs
        initial = super(EngineCreateView, self).get_initial()
        return initial


class EngineUpdateView(EngineListMixin, generic.UpdateView):
    template_name = 'dashboard/podcatalogue/engine_form.html'
    model = Engine
    form_class = EngineForm

    def get_context_data(self, **kwargs):
        ctx = super(EngineUpdateView, self).get_context_data(**kwargs)
        return ctx

    def get_success_url(self):
        messages.info(self.request, _("Engine updated successfully"))
        return super(EngineUpdateView, self).get_success_url()


class EngineDeleteView(EngineListMixin, generic.DeleteView):
    template_name = 'dashboard/podcatalogue/engine_delete.html'
    model = Engine

    def get_context_data(self, *args, **kwargs):
        ctx = super(EngineDeleteView, self).get_context_data(*args, **kwargs)
        return ctx

    def get_success_url(self):
        messages.info(self.request, _("Engine deleted successfully"))
        return super(EngineDeleteView, self).get_success_url()


class ProductCreateUpdateView(CoreProductCreateUpdateView):
    """
    Dashboard view that bundles both creating and updating single products.
    Supports the permission-based dashboard.
    """

    template_name = 'dashboard/catalogue/product_update.html'
    model = Product
    context_object_name = 'product'

    form_class = ProductForm
    category_formset = ProductCategoryFormSet
    questions_formset = ProductQuestionsFormSet

    def __init__(self, *args, **kwargs):
        super(ProductCreateUpdateView, self).__init__(*args, **kwargs)
        self.formsets = {'category_formset': self.category_formset, 'questions_formset': self.questions_formset}

    def get_object(self, queryset=None):
        """
        This parts allows generic.UpdateView to handle creating products as
        well. The only distinction between an UpdateView and a CreateView
        is that self.object is None. We emulate this behavior.
        Additionally, self.product_class is set.
        """
        self.creating = not 'pk' in self.kwargs
        if self.creating:
            try:
                product_class_id = 1
                self.product_class = ProductClass.objects.get(
                    id=product_class_id)
            except ObjectDoesNotExist:
                raise Http404
            else:
                return None  # success
        else:
            product = super(ProductCreateUpdateView, self).get_object(queryset)
            self.product_class = product.product_class
            product.questions = ProductQuestion.objects.filter(product=product)
            return product

    def get_context_data(self, **kwargs):
        ctx = super(ProductCreateUpdateView, self).get_context_data(**kwargs)
        ctx['product_class'] = self.product_class
        if 'category_formset' not in ctx:
            ctx['category_formset'] \
                = self.category_formset(instance=self.object)
        if 'questions_formset' not in ctx:
            ctx['questions_formset'] = self.questions_formset(instance=self.object)
        if self.object is None:
            ctx['title'] = _('Create new %s product') % self.product_class.name
        else:
            ctx['title'] = ctx['product'].get_title()
        return ctx

    def forms_valid(self, form, category_formset, questions_formset):
        """
        Save all changes and display a success url.
        """
        if not self.creating:
            # a just created product was already saved in process_all_forms()
            self.object = form.save()
        # Save formsets
        category_formset.save()
        questions_formset.save()
        return HttpResponseRedirect(self.get_success_url())

    def forms_invalid(self, form, category_formset, questions_formset):
        messages.error(self.request,
                       _("Your submitted data was not valid - please "
                         "correct the below errors"))
        ctx = self.get_context_data(form=form,
                                    category_formset=category_formset,
                                    questions_formset=questions_formset)
        return self.render_to_response(ctx)

    def process_all_forms(self, form):
        """
        Short-circuits the regular logic to have one place to have our
        logic to check all forms
        """
        # Need to create the product here because the inline forms need it
        # can't use commit=False because ProductForm does not support it
        if self.creating and form.is_valid():
            self.object = form.save()

        category_formset = self.category_formset(
            self.request.POST, instance=self.object)
        questions_formset = self.questions_formset(
            self.request.POST, instance=self.object)

        is_valid = all([
            form.is_valid(),
            category_formset.is_valid(), questions_formset.is_valid()
        ])

        if is_valid:
            return self.forms_valid(
                form, category_formset, questions_formset)
        else:
            # delete the temporary product again
            if self.creating and form.is_valid():
                self.object.delete()
                self.object = None

            return self.forms_invalid(
                form, category_formset, questions_formset)

