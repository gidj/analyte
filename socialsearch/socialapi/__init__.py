""" Since we will conducting the same actions with each social media site, it
    makes sense to have an abstract base class to define common methods, and then
    implement them specifically for each site in their own subclass. """


_SOCIAL_API_MAP = {}
_SOCIAL_API_CHOICES = []

def register_social_api(api_class):
    # This decorator registers a class as SocialAPI
    _SOCIAL_API_MAP[api_class.api_code] = api_class
    _SOCIAL_API_CHOICES.append([api_class.api_code, api_class.api_name])
    return api_class

def get_api_class(api_code):
    return _SOCIAL_API_MAP[api_code]

def api_code_choices():
    return _SOCIAL_API_CHOICES


class SocialAPIBase(object):
    """ Abstract Base Class for building searching objects for social media
        sites. 'api_code' and 'api_name' are used for registering each search
        API class, and in turn limiting which API classes are available for
        performing searches. """

    api_code = NotImplemented
    api_name = NotImplemented

    search_endpoint = NotImplemented

    class Meta:
        abstract = True

    def keyword_search(self, keyword):
        raise NotImplementedError

    @property
    def search_results_list(self):
        raise NotImplementedError


@register_social_api
class RedditAPI(SocialAPIBase):
    """ Interfaces with Reddit's API to search for keywords.
        This is mostly pseudocode, there are several options to build this out--
        use a third party library, use the requests package, etc. """
    api_code = u"REDDIT"
    api_name = u"Reddit Search API"

    search_endpoint = "https/www.reddit.com/search"

    def _build_query(keyword):
        return ".json?q={}&sort=new".format(keyword)

    def _process_data(self, response):
        data = []
        for record in response["payload"]:
            row = {"title": record["title"],
                   "content_link": record["url"]}
            data.append(row)
        return data

    def keyword_search(self, keyword):
        self._response = get_response(self.search_endpoint + self._build_query)
        self._clean_data = self._process_data(self._respons)

    @property
    def search_results_list(self):
        return self._clean_data


class TwitterAPI(SocialAPIBase):
    """ Interface with Twitter's API to search for keywords.
        I would build out this class in a similar way to RedditAPI, but
        obviously making the methods specific to Twitter instead of Reddit. """
    api_code = u"TWITTER"
    api_name = u"Twitter Search API"


@register_social_api
class CrawlerAPI(SocialAPIBase):
    """ Some sites may not have an API exposed. I'm not going to do it now,
        but we could write our own crawler for any arbitrary site. As long as
        it conforms to the interfaces of the base class, and we decorate it
        with @register_social_api, it would be available for search.models.SocialMediaNetwork
        to use to perform a search. """
    api_code = u"BUSINESSINSIDER"
    api_name = u"Business Insider Crawler"

