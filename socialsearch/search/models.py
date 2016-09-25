from __future__ import unicode_literals

from datetime import datetime

from django.db import models
from django.contrib.auth.models import User

import socialapi


class SocialMediaNetwork(models.Model):
    name = models.CharField(u"Name", required=True)
    api_code = models.CharField(u"Search API Code",
        choices=socialapi.api_code_choices(),
        blank=False)

    def __unicode__(self):
        return self.name

    def api_connection(self):
        return socialapi.get_api_class(self.api_code)


class SocialSearch(models.Model):
    user = models.ForeignKey(User, blank=False)
    social_networks = models.ManyToManyField(SocialMediaNetwork, blank=False)
    # If self.frequency is None, never repeat.
    frequency = models.DurationField(u"Time between executions", blank=True, default=None)
    query = models.CharField(u"Keyword Term", blank=False)


class SocialSearchExecution(models.Model):
    social_search = models.ForeignKey(SocialSearch, related_name="search")
    # Since the original SocialSearch.query related to this may change with
    # time, we duplicate it here at the time of search execution.
    searched_query = models.CharField(u"Keyword that was Searched", blank=False)
    date = models.DateTimeField(u"Time and Date when this search was run",
            blank=False,
            default=datetime.now())

    def as_csv_file(self):
        rows = []
        rows.append([u"Title", u"Content Link", "Social Media Source"])
        for result in self.results.all():
            rows.append(result.data_to_row)

        # Returns csv file object
        return write_to_csv_file(self._csv_filename, rows)

    @property
    def _csv_filename(self):
        return "{date}_{keyword}_{sources}.csv".format(
            date=self.date.strftime(u"%Y%m%d"),
            keyword=self.searched_query,
            sources=u"_".join(self.social_search.social_networks.all()))


class SocialSearchResult(models.Model):
    search_execution = models.ForignKey(u"Social Search Execution",
            blank=False,
            related_name=u"results")
    title = models.CharField(u"Title", blank=False)
    content_link = models.CharField(u"URI", blank=False)
    source = models.ForeignKey(SocialMediaNetwork, required=True)

    def data_to_row(self):
        return [self.title, self.content_link, self.source.name]


