"""socialsearch URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from search import views as search_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
]

urlpatterns += [
    url(r'^searches/$', search_views.Searches.as_view(), name="searches"),
    url(r'^searches/(?P<search_id>[0-9]+)$', search_views.SearchDetail.as_view(), name="search_detail"),
    url(r'^searches/(?P<search_id>[0-9]+)$/new', search_views.SearchDetailCreate.as_view(), name="search_ create"),
    url(r'^searches/(?P<search_id>[0-9]+)$/edit', search_views.SearchDetailEdit, name="search_edit"),
    url(r'^searches/(?P<search_id>[0-9]+)/runs/$', search_views.ExecutedSearches.as_view(), name="executed_searches"),
]
