from django.contrib import messages
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _
from django.views.generic import CreateView, FormView
from django.core.urlresolvers import reverse
from oscar.core.loading import get_model
import json
import forms


class HomeView(FormView):
    form_class = forms.SearchCreationForm
    template_name = 'search/home.html'

    def get_form_kwargs(self):
        current_session = self.request.session.get('search_data', None)
        if current_session:
            current_data = json.loads(current_session)
            kwargs = {'data':current_data}
            kwargs.update(super(HomeView, self).get_form_kwargs())
        else:
            kwargs = super(HomeView, self).get_form_kwargs()
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = forms.SearchCreationFormSet(self.request.POST)
        else:
            current_session = self.request.session.get('search_data', None)
            initial = []
            if current_session:
                current_data = json.loads(current_session)
                for item in current_data['pieces']:
                    initial_item = {}
                    initial_item['category'] = item['category']
                    initial_item['piece'] = item['piece']
                    initial_item['comments'] = item['comments']
                    initial_item['quantity'] = item['quantity']
                    initial.append(initial_item)

            context['formset'] = forms.SearchCreationFormSet(initial=initial)
        return context
    
    def form_valid(self, form):
        response = super(HomeView, self).form_valid(form)
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            final_data = {}
            final_data["engine"] = form.cleaned_data["engine"].id
            final_data["frameref"] = form.cleaned_data["frameref"]
            final_data["brand"] = form.cleaned_data["brand"].id
            final_data["version"] = form.cleaned_data["version"].id
            final_data["model"] = form.cleaned_data["model"].id
            final_data["bodywork"] = form.cleaned_data["bodywork"].id

            # formset
            final_data["pieces"] = []
            current_formset_data = formset.cleaned_data
            for current_item in current_formset_data:
                final_item = {}
                if "category" in current_item:
                    final_item["category"] = current_item["category"].id
                if "quantity" in current_item:
                    final_item["quantity"] = current_item["quantity"]
                if "piece" in current_item:
                    final_item["piece"] = current_item["piece"].id
                if "comments" in current_item:
                    final_item["comments"] = current_item["comments"]
                final_data["pieces"].append(final_item)   

            self.request.session['search_data'] = json.dumps(final_data)
            return True
        else:
            return False

    def get_success_url(self):
        return reverse('search:home')

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            result = self.form_valid(form)
            return HttpResponse(json.dumps({"result":result}), mimetype='application/json')
        else:
            self.form_invalid(form)
            return HttpResponse(json.dumps({"result":False}), mimetype='application/json')


class ConfirmView(FormView):
    form_class = forms.SearchConfirmForm
    template_name = 'search/confirm.html'
