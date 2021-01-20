#!/usr/bin/env python3
import re
import requests


class SiteFetcher:
    """Fetches a single site and stores information about
    the latency, status_code and other stuff

    :param site: A site dict
    :type site: dict
    """
    def __init__(self, site):
        """Constructor method"""
        self.regex_found = None
        self.latency = None
        self.site = site
        self.status_code = None

    def __str__(self):
        return f"<SiteFetcher site={self.site}>"

    def to_dict(self):
        """Return a dict representation of the fetcher

        :return: A dict representation of the fetcher
        :rtype: dict
        """
        return {'site': self.site['url'],
                'status': self.status_code,
                'latency': self.latency,
                'regex_found': self.regex_found}

    def get_site(self):
        """Fetches a single site and stores the information

        :return: The status code of the request
        :rtype: int
        """
        try:
            r = requests.get(self.site['url'])
        except requests.exceptions.ConnectionError:
            self.status_code = None
            self.latency = None
            self.regex_found = None
            return None
        self.status_code = r.status_code
        self.latency = r.elapsed.total_seconds()
        self.regex_found = self.regex_is_found(r, self.site.get('regex', None))
        return self.status_code

    @staticmethod
    def regex_is_found(response, regex_str):
        """Whether the regex is found in the response text

        :param response: A response object
        :type response: requests.Response
        :param regex_str: A string representation of a regular expression
        :type regex_str: str

        :return: A boolean whether the regex is matched in the text
        :rtype: bool
        """
        if not regex_str:
            return None
        return bool(re.search(regex_str, response.text))

    def stats_str(self):
        """Returns the site stats. Cool for debugging

        :return: String of a site dict
        :rtype: str
        """
        return (f"Site: {self.site['url']} "
                f"Status: {self.status_code} "
                f"Latency: {self.latency} "
                f"Regex found: {self.regex_found}")
