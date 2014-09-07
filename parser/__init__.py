import re
import StringIO
import gzip
import urllib2
import cgi
from bs4 import BeautifulSoup
from urlparse import urlparse

import opengraph


class Scraper():
    def __init__(self, url):
        self.url = url

        self.site_name = None
        self.title = None
        self.description = None
        self.image = None
        self.host = None
        self.site_icon = None
        self.type = None
        self.charset = None

    def parse(self):
        raw_html = self.request_url(self.url)
        parsed = self.scrap_html(raw_html)
        self.build(parsed)


    def request_url(self, url):
        response = urllib2.urlopen(url)
        _, params = cgi.parse_header(response.headers.get('Content-Type', ''))
        self.charset = params.get('charset', 'utf-8')
        encoding = response.info().get('Content-Encoding')
        if encoding and encoding == 'gzip':
            buf = StringIO.StringIO( response.read())
            f = gzip.GzipFile(fileobj=buf)
            data = f.read()
        else:
            data = response.read()
        return data


    def scrap_html(self, raw_html):
        soup = BeautifulSoup(raw_html)
        opengraph.OpenGraph.scrape = True
        parsed = opengraph.OpenGraph(html=soup, scrape = True)

        if 'description' not in parsed:
            parsed['description'] = self.scrap_description(soup)

        parsed['site_icon'] = self.scrap_icon(soup)


        return parsed

    def scrap_description(self, doc):
        tags = doc.findAll('meta', attrs={'name': 'og:description'})
        if len(tags) == 0:
            tags = doc.findAll('meta', attrs={'name': 'description'})
        for tag in tags:
            return tag['content']

    def scrap_icon(self, doc):
        tags = doc.findAll('link', attrs={'rel': re.compile(r'^apple-touch-icon')})
        if len(tags) == 0:
            tags = doc.findAll('link', attrs={'rel': re.compile(r'^icon')})
        for tag in tags:
            return tag['href']



    def build(self, parsed):

        parsed_url = urlparse(self.url)
        netloc = parsed_url.netloc.replace('www.', '')

        self.host = netloc

        if 'site_name' in parsed:
            self.site_name = parsed['site_name']

        if 'title' in parsed:
            self.title = parsed['title']

        if 'description' in parsed:
            self.description = parsed['description']

        if 'image' in parsed:
            self.image = parsed['image']

        if 'type' in parsed:
            self.type = parsed['type']

        if 'site_icon' in parsed:
            self.site_icon = parsed['site_icon']

        # set defaults, if not found in meta
        if not self.title:
            self.title = netloc

        if not self.site_name:
            self.site_name = netloc

    def as_dict(self):
        ret = {}
        return {
            u'title': self.title, 
            u'description': self.description, 
            u'site_name':self.site_name, 
            u'host': self.host,
            u'image': self.image,
            u'type': self.type,
            u'url': self.url,
            u'charset': self.charset,
            u'site_icon': self.site_icon}





