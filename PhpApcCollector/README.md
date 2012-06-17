PhpApcCollector
---------------

This collector is for collecting APC (Alternative PHP Cache) statistics for Graphite.

### Configuration

To be able to use the plugin first of all you will need to put the included stats_apc.php to the www directory where Apache or Nginx (or whatever webserver you like) will be able to serve from. The following configurations assume nginx setup but can be easily applied to any webserver.

__Nginx__

Put the stats_apc.php file in the webserver root for http://localhost/. This way you will be able to crawl the statistics from the url http://localhost/stats_apc.php. You can test your setup from console:

	curl http://localhost/stats_apc.php
   
If this returned a JSON object that means it's working. 

__Diamond__

In /etc/diamond/collectors/PhpApcCollector.conf insert the followings

	enabled = True
	status_uri = /stats_apc.php
   
Restart Diamond and you're all set.