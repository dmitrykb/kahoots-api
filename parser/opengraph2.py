import opengraph


class OpenGraph2(OpenGraph):

    scrape = True
    required_attrs = ['title', 'type', 'image', 'url', 'description']

     def scrap_description(self, doc):
        tags = doc.findAll('meta', attrs={'name': 'og:description'})
        for tag in tags:
            return tag['content']