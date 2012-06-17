PhpFpmCollector
---------------

This collector is for collecting PHP-FPM (FastCGI Process Manager for PHP) statistics for Graphite.

### Configuration

First of all you will need to enable status page in php-fpm.conf. 

__PHP-FPM__

The following line should be in the config file.

   pm.status_path = /fpm_status
   
Reload php-fpm service.

__Nginx__

In the Nginx config most likely you have to create an explicit location for this. It's good practice to allow connection from only localhost.

   location = /fpm_status {
      access_log off;
      allow 127.0.0.1;
      deny all;
	  
      include /etc/nginx/fastcgi_params;	
      fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
      fastcgi_param SCRIPT_NAME $fastcgi_script_name;
      fastcgi_param PATH_INFO $fastcgi_path_info;
      fastcgi_param PATH_TRANSLATED $document_root$fastcgi_path_info;
      fastcgi_pass 127.0.0.1:9000;
   }

After reload nginx you can test the setup from commandline.

   curl http://localhost/fpm_status
   
If this returned the list of metrics that means it's working. 

__Diamond__

In /etc/diamond/collectors/PhpFpmCollector.conf insert the followings

   enabled = True
   status_uri = /fpm_status
   
Restart Diamond and you're all set.