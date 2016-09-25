""" Since we will conducting the same actions with each social media site, it
    makes sense to have an abstract base class to define common methods, and then
    implement them specifically for each site in their own subclass. """

class SocialAPIBase(object):
    key = NotImplemented

    class Meta:
        abstract = True

    def open_connection(self):
        raise NotImplementedError

    def keyword_search(self, keyword):
        raise NotImplementedError

    def search_results_list(self):
        raise NotImplementedError


class RedditAPI(SocialAPIBase):
    """ Interfaces with Reddit's API to search for keywords. """
    key = u"reddit"

class TwitterAPI(SocialAPIBase):
    """ Interface with Twitter's API to search for keywords. """
    key = u"twitter"

    # Twitter's API is OAuth2 based, so we ne
    pass

