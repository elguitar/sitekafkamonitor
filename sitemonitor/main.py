#!/usr/bin/env python3
import argparse
import datetime
import pathlib
import time
import yaml

import options
from producer import producer, default_topic
from siteinfofetcher import SiteFetcher


class SiteMonitor():
    """Monitors sites periodically

    :param config: A path to an YAML-file containing
        the site information
    :type config: pathlib.Path
    """

    def __init__(self, config):
        """Initialize the object

        Read config and initialize sites"""
        print("Initializing SiteMonitor")
        self._config = self.read_config(config)
        self.sites = self._init_sites()

    @staticmethod
    def _init_last_check(site):
        """Adds 'last_check' key to site and initializes it with current time

        :param site: A site dict
        :type site: dict
        :return: The same site dict, but with added 'last_check' key
        :rtype: dict
        """
        return site | {'last_check': datetime.datetime.now()}

    @staticmethod
    def _site_needs_checking(site):
        """Returns a bool about whether it is time to check the site

        :param site: A site dict
        :type site: dict
        :return: A boolean whether the site needs checking
        :rtype: bool
        """
        now = datetime.datetime.now()
        interval = datetime.timedelta(seconds=site['interval'])
        return now - site['last_check'] > interval

    def _init_sites(self):
        """Initializes site objects with a initial datetime (now)

        :return: A list of fully initialized sites
        :rtype: list
        """
        return [self._init_last_check(site) for site in self._config['sites']]

    def check_urls(self):
        """Checks whether sites need to be fetched,
        fetches them and pushes them to Kafka

        :return: True on success
        :rtype: bool
        """
        for site in self.sites:
            if self._site_needs_checking(site):
                sif = SiteFetcher(site)
                if sif.get_site():
                    print(sif.stats_str())
                    producer.send(default_topic, value=sif.to_dict())
                site['last_check'] = datetime.datetime.now()
        return True

    @staticmethod
    def read_config(config):
        """Reads the config from file

        :param config: A path to the config file
        :type config: pathlib.Path
        :return: A dict, containing the site information
        :rtype: dict
        """
        conf_file = pathlib.Path(config)
        contents = conf_file.read_text(encoding='utf-8')
        print("Config read successfully!")
        return yaml.safe_load(contents)

    def run_loop(self):
        """Runs the loop

        This is the heart of the program,
        it runs the loop where it checks whether
        the urls need fetching and then acts accordingly
        """
        while True:
            self.check_urls()
            time.sleep(options.sleeptime)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                 description="Monitor sites and produce Kafka topic")
    parser.add_argument('-c', '--config',
                        help="Path of the configuration file",
                        default=(options.root_path / "sites.yml"))

    args = parser.parse_args()
    sm = SiteMonitor(config=args.config)
    print("Initialized successfully!")
    sm.run_loop()
