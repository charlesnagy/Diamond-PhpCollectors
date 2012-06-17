import json
import urllib

import diamond.collector
import socket

class PhpFpmCollector(diamond.collector.Collector):
    """
    Collect PHP-FPM stats
    """

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        return {
            'path':     'php.fpm',
            
            # Which rows of 'status' you would like to publish.
            # 'telnet host port' and type stats and hit enter to see the list of
            # possibilities.
            # Leave unset to publish all
            #'publish': ''

	    'status_uri': 	'/fpm-status',
       }

    def get_stats(self, config):
        # Always ignoe this metrics:
        ignore = ['pool', 'process manager', 'start time']
	
        stats = {}
        # get php-fpm stats
        try:
            stdout = urllib.urlopen('http://localhost/{uri}?json'.format(uri=config['status_uri'])).read()
        except IOError, e:
            self.log.exception('Failed to get stats from %s', config['status_uri'])
        else:
            # parse stats
	    data = json.loads(stdout) 
        for metric, value in data.iteritems():
            if isinstance(value, int) and not metric in ignore:
				stats['{metric}'.format(metric=metric.replace(' ', '_'))] = value
        return stats

    def collect(self):
        stats = self.get_stats(self.config)
        # figure out what we're configured to get, defaulting to everything
        desired = self.config.get('publish', stats.keys())
        # for everything we want
        for stat in desired:
            if stat in stats:
                # we have it
                self.publish(stat, stats[stat])
            else:
                # we don't, must be somehting configured in publish so we
                # should log an error about it
                self.log.error("No such key '%s' available, issue 'stats' for "
                               "a full list", stat)

