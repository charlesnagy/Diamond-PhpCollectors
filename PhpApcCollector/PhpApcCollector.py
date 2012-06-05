import json
import urllib

import diamond.collector
import socket

class PhpApcCollector(diamond.collector.Collector):
    """
    Collect PHP-APC stats
    """

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        return {
            'path':     'php.apc',
            
            # Which rows of 'status' you would like to publish.
            # 'telnet host port' and type stats and hit enter to see the list of
            # possibilities.
            # Leave unset to publish all
            #'publish': ''

	    'status_uri': 	'/stats_apc.php',
       }

    def get_stats(self, config):
        # stuff that's always ignored, aren't 'stats'
        ignored = ('libevent', 'pid', 'pointer_size', 'time', 'version')
        
        stats = {}
        # get php-apc stats
        try:
            stdout = urllib.urlopen('http://localhost/{uri}'.format(uri=config['status_uri'])).read()
        except IOError, e:
            self.log.exception('Failed to get stats from %s', config['status_uri'])
        else:
            # parse stats
	    data = json.loads(stdout) 
	    for set, metrics in data.iteritems():
		for metric, value in metrics.iteritems():
                    if isinstance(value, int):
			stats['{set}_{metric}'.format(set=set, metric=metric)] = value
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

