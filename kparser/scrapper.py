import StringIO
import gzip
import urllib2
import cgi
from bs4 import BeautifulSoup
from urlparse import urlparse

import kparser.opengraph2


class Scraper():
    def __init__(self, url):
        self.url = url
        self.data = {}

    def parse(self):
        raw_html = self.request_url(self.url)
        parsed = self.scrap_html(raw_html)
        self.build(parsed)


    def request_url(self, url):
        response = urllib2.urlopen(url)
        _, params = cgi.parse_header(response.headers.get('Content-Type', ''))
        self.data['charset'] = params.get('charset', 'utf-8')
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
        parsed = kparser.opengraph2.OpenGraph2(html=soup, scrape = True)
        return parsed

    def build(self, parsed):

        parsed_url = urlparse(self.url)
        netloc = parsed_url.netloc.replace('www.', '')
        self.data['host'] = netloc
        self.data['url'] = self.url


        if 'site_name' in parsed:
            self.data['site_name'] = parsed['site_name']

        if 'title' in parsed:
            self.data['title'] = parsed['title']

        if 'description' in parsed:
            self.data['description'] = parsed['description']

        if 'image' in parsed:
            self.data['image'] = parsed['image']

        if 'type' in parsed:
            self.data['type'] = parsed['type']

        if 'icon' in parsed:
            self.data['site_icon'] = parsed['icon']

        # set defaults, if not found in meta
        if 'title' not in self.data:
            self.data['title'] = netloc

        if 'site_name' not in self.data:
            self.data['site_name'] = netloc
