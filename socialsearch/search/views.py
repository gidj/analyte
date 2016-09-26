from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView

from search.models import SocialSearch, SocialSearchExecution, SocialSearchResult
from search.forms import SocialSearchModelForm, CSVExportForm

@method_decorator(login_required, name="dispatch")
class Searches(ListView):
    template_name = u"search/searches.html"

    def get_queryset(self):
        return SocialSearch.objects.filter(user=self.request.user)


@method_decorator(login_required, name="dispatch")
class SearchDetail(DetailView):
    model = SocialSearch
    template_name = u"search/search_detail.html"


class SearchDetailCreate(View):
    context = {}
    template_name = u"search/search_create.html"

    form_class = SocialSearchModelForm

    @login_required
    def get(self, request):
        self.context["form"] = self.form_class()
        return render(request, self.template_name, self.context)

    @login_required
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            # We set the user here, since it is not part of the form
            search = form.save(commit=False)
            search.user = request.user
            search.save()
            return HttpResponseRedirect(reverse("search_detail", args=[search.id]))

        self.context["form"] = form
        return render(request, self.template_name, self.context)


@method_decorator(login_required, name="dispatch")
class SearchDetailEdit(UpdateView):
    model = SocialSearch
    fields = ["social_networks", "frequency", "query"]


@method_decorator(login_required, name="dispatch")
class ExecutedSearches(ListView):
    template_name = u"search/executed_searches.html"

    def get_queryset(self):
        return SocialSearchExecution.objects.filter(user=self.request.user)


class ExecutedSearchDetail(View):
    context = {}
    template_name = u"search/executed_detail.html"

    email_form = CSVExportForm

    @login_required
    def get(self, request, *args, **kwargs):
        self.context["form"] = self.email_form()
        return render(request, self.template_name, self.context)

    @login_required
    def post(self, request, *args, **kwargs):
        form = self.email_form(request.POST)

        if form.is_valid():
            execution_id = kwargs.pop("execution_id")
            execution = SocialSearchExecution.objects.get(id=execution_id)

            email_address = form.cleaned_data["email_address"]

            execution.send_in_email(
                email_addresses=[email_address],
                attachments=[execution.as_csv_file()]
            )

            # Should add a success message here if we are using a messages framework

        return render(request, self.template_name, self.context)

