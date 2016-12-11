from elasticsearch import Elasticsearch
import hashlib
import logging

LOGGER = logging.getLogger('Elastic_URL_tester')
logging.getLogger('elasticsearch').setLevel('WARNING')


class ElasticHelpers:
    def __init__(self, spider):
        self.spider = spider
        self.es = None

    def get_connection(self):
        if isinstance(self.es, Elasticsearch):
            return self.es
        else:
            self.es = Elasticsearch(hosts=self.spider.settings.attributes['ELASTICSEARCH_SERVERS'].value,
                                    retry_on_timeout=True)
            return self.es

    def exist(self, url):
        es = self.get_connection()
        doc_id = hashlib.sha1(url.encode('utf-8')).hexdigest()
        res = es.exists(index=self.spider.settings.attributes['ELASTICSEARCH_INDEX'].value,
                        doc_type=self.spider.settings.attributes['ELASTICSEARCH_TYPE'].value,
                        id=doc_id)
        return res

    def process_url(self, urls):
        filtered_urls = []
        for url in urls:
            if not self.exist(url.url):
                filtered_urls.append(url)
            else:
                LOGGER.debug('%s already scrapped. Skipping.', url.url)
        return filtered_urls
