import StringIO
import gzip
import urllib2
import urllib
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

        hdr = {'User-Agent': 'Mozilla/5.0'}
        req = urllib2.Request(url, headers=hdr)
        response = urllib2.urlopen(req)


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

    def get(self, param, default = ''):
        return self.data.get(param, default)



    def scrap_html(self, raw_html):
        soup = BeautifulSoup(raw_html)
        parsed = kparser.opengraph2.OpenGraph2(html=soup, scrape = True)
        return parsed

    def build(self, parsed):

        parsed_url = urlparse(self.url)
        netloc = parsed_url.netloc.replace('www.', '')
        self.data['host'] = netloc
        self.data['url'] = self.url


        self.data['site_name'] = parsed.get('site_name')

        self.data['title'] = parsed.get('title')

        self.data['description'] = parsed.get('description')

        self.data['image'] = parsed.get('image')

        self.data['type'] = parsed.get('type')

        self.data['site_icon'] = parsed.get('icon')

        # set defaults, if not found in meta
        if not self.data.get('title'):
            self.data['title'] = netloc

        if not self.data.get('site_name'):
            self.data['site_name'] = netloc

        if  not self.data.get('description'):
            self.data['description'] = self.data['title']