
Jerv Crawler
############
The Jerv Crawler is a work in progress, it's purpose is to evaluate the SSL/TLS setup of websites. The primary 
demographic is websites targeted towards Norwegians. This is determined by looking up the language attribute in the HTML
returned, or if any of the Norwegian TDL's are used. The crawler does not yet respect the robots.txt file, but it it 
will crawl a maximum of two pages per minute now, 1 normal GET request, and 1 HEAD request. The data that is saved from 
the GET request will be the language attribute, size of page, response time, and any links to other pages. The HEAD 
request is used to check the HTTPS status of the site.

The user agent supplied by the crawler will look like this, if you wish to block the crawler.: 
`Mozilla/5.0 (compatible; Jerv.http.client/0.1; +http://puse.cat/jerv.html)`
