import re
import opengraph


class OpenGraph2(opengraph.OpenGraph):

    required_attrs = ['title', 'type', 'image', 'url', 'description', 'icon']
    scrape = True
    

    def scrape_description(self, doc):
        tags = doc.findAll('meta', attrs={'name': 'og:description'})
        for tag in tags:
            return tag['content']

    def scrape_icon(self, doc):
        tags = doc.findAll('link', attrs={'rel': re.compile(r'^apple-touch-icon')})
        if len(tags) == 0:
            tags = doc.findAll('link', attrs={'rel': re.compile(r'^icon')})
        for tag in tags:
            return tag['href']
