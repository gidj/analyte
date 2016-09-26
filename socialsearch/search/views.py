from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import Http404
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView

from search.models import SocialSearch, SocialSearchExecution, SocialSearchResult

@method_decorator(login_required, name="dispatch")
class Searches(ListView):
    template_name = u"search/searches.html"

    def get_queryset(self):
        return SocialSearch.objects.filter(user=self.request.user)


@method_decorator(login_required, name="dispatch")
class SearchDetail(DetailView):
    model = SocialSearch
    template_name = u"search/search_detail.html"


@method_decorator(login_required, name="dispatch")
class SearchDetailCreate(View):
    model = SocialSearch
    template_name = u"search/search_create.html"


@method_decorator(login_required, name="dispatch")
class ExecutedSearches(ListView):
    template_name = u"search/executed_searches.html"

    def get_queryset(self):
        return SocialSearchExecution.objects.filter(user=self.request.user)






@login_required
def executions(request):
    context = {}
    return render(request, "search/searches.html", context)

@login_required
def results(request, run_id):
    context = {}
    return render(request, "search/searches.html", context)

