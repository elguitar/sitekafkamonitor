#!/usr/bin/env python3
import re
import requests


class SiteFetcher:
    def __init__(self, site):
        self.regex_found = None
        self.latency = None
        self.site = site
        self.status_code = None

    def __str__(self):
        return f"<SiteFetcher site={self.site}>"

    def get_site(self):
        r = requests.get(self.site['url'])
        self.status_code = r.status_code
        self.latency = r.elapsed.total_seconds()
        self.regex_found = self.regex_is_found(r, self.site['regex'])
        return self.status_code

    def regex_is_found(self, response, regex_str):
        if not regex_str:
            return None
        return bool(re.search(regex_str, response.text))

    def stats_str(self):
        return (f"Site: {self.site['url']} "
                f"Status: {self.status_code} "
                f"Latency: {self.latency} "
                f"Regex found: {self.regex_found}")
