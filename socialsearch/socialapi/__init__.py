""" Since we will conducting the same actions with each social media site, it
    makes sense to have an abstract base class to define common methods, and then
    implement them specifically for each site in their own subclass. """


_SOCIAL_API_MAP = {}
_SOCIAL_API_CHOICES = []

def register_social_api(api_class):
    # This decorator registers a class as SocialAPI
    _SOCIAL_API_MAP[api_class.key] = api_class
    _SOCIAL_API_CHOICES.append([api_class.key, api_class.name])
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

    class Meta:
        abstract = True

    def open_connection(self):
        raise NotImplementedError

    def keyword_search(self, keyword):
        raise NotImplementedError

    def search_results_list(self):
        raise NotImplementedError


@register_social_api
class RedditAPI(SocialAPIBase):
    """ Interfaces with Reddit's API to search for keywords. """
    api_code = u"REDDIT"
    api_name = u"Reddit Search API"


@register_social_api
class TwitterAPI(SocialAPIBase):
    """ Interface with Twitter's API to search for keywords. """
    api_code = u"TWITTER"
    api_name = u"Twitter Search API"

    # Twitter's API is OAuth2 based, so we ne
    pass

