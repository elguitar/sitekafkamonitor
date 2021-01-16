#!/usr/bin/env python3
import argparse
import datetime
import pathlib
import time
import yaml

import options
import siteinfofetcher


class SiteMonitor():
    """Monitors sites periodically"""

    def __init__(self, config):
        """Initialize the object

        Read config and initialize sites"""
        self._config = self.read_config(config)
        self.sites = self._init_sites()

    @staticmethod
    def _init_last_check(site):
        """Adds 'last_check' key to site and initializes it with current time
        """
        return site | {'last_check': datetime.datetime.now()}

    @staticmethod
    def _site_needs_checking(site):
        """Returns a bool about whether it is time to check the site"""
        now = datetime.datetime.now()
        interval = datetime.timedelta(seconds=site['interval'])
        return now - site['last_check'] > interval

    def _init_sites(self):
        """Initializes site objects with a initial datetime (now)"""
        return [self._init_last_check(site) for site in self._config['sites']]

    def check_urls(self):
        """Checks whether sites need to be fetched,
           fetches them and pushes them to Kafka"""
        for site in self.sites:
            if self._site_needs_checking(site):
                print(f"Fetch {site['url']}")
                sif = siteinfofetcher.SiteFetcher(site)
                if sif.get_site():
                    print(sif.stats_str())
                site['last_check'] = datetime.datetime.now()
        return True

    @staticmethod
    def read_config(config):
        """Reads the config from file"""
        conf_file = pathlib.Path(config)
        contents = conf_file.read_text(encoding='utf-8')
        return yaml.safe_load(contents)

    def run_loop(self):
        """Runs the loop"""
        while True:
            self.check_urls()
            time.sleep(options.sleeptime)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                 description="Monitor sites and produce Kafka topic")
    parser.add_argument('-c', '--config',
                        help="Path of the configuration file",
                        default=(options.root_path / "config.yml"))

    args = parser.parse_args()
    sm = SiteMonitor(config=args.config)
    sm.run_loop()
