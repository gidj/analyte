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
        APIConnectionClass = socialapi.get_api_class(self.api_code)
        return APIConnectionClass()


class SocialSearch(models.Model):
    user = models.ForeignKey(User, blank=False)
    social_networks = models.ManyToManyField(SocialMediaNetwork, blank=False)
    # If self.frequency is None, never repeat.
    frequency = models.DurationField(u"Time between executions", blank=True, default=None)
    query = models.CharField(u"Keyword Term", blank=False)

    # Let's assume celery is setup properly
    from celery.task import app
    @app.task()
    def execute_social_search(self):
        execution = SocialSearchExecution.objects.create(
            social_search=self,
            searched_query=self.query,
            date=datetime.now()
        )
        execution.save()

        # Search all of the selected social networks
        for network in self.social_networks.all():
            connection = network.api_connection()
            connection.keyword_search(self.query)
            results = connection.search_results_list

            # Create search result objects for each returned result
            for result in results:
                r = SocialSearchResult.objects.create(
                    search_execution=execution,
                    title=result["title"],
                    content_link=result["content_link"],
                    source=network)
                r.save()

    def schedule_search_task(self):
        # Assuming we are using Celery
        if self.frequency:
            self.execute_social_search.schedule(run_every=self.frequency)
        else:
            pass


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

        # Returns csv file objec
        return write_to_csv_file(self._csv_filename, rows)

    def send_in_email(self, email_addresses=[], attachments=[]):
        # TODO: Fill in this using a library, or some custom implementation
        return None


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


