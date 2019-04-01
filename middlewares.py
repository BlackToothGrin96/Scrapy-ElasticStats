from scrapy import signals
from scrapy.exceptions import NotConfigured
import requests
import hashlib
import json
from datetime import datetime


class ElasticStatsSender(object):

    def __init__(self, stats, settings):
        self.stats = stats
        self.settings = settings

    @classmethod
    def from_crawler(cls, crawler):
        enabled = crawler.settings.getbool("ELASTICSTATS_ENABLED")
        if not enabled:
            raise NotConfigured

        o = cls(crawler.stats, crawler.settings)
        crawler.signals.connect(o.spider_closed, signal=signals.spider_closed)
        return o

    def spider_closed(self, spider):
        data = {}
        settings = self.settings
        host = settings.get("ELASTICSEARCH_SERVERS")
        port = settings.get("ELASTICSEARCH_PORT")
        auth = settings.get("ELASTICSEARCH_AUTH")

        index = self.settings.get('ELASTICSTATS_INDEX')
        doc_type = self.settings.get('ELASTICSTATS_TYPE')

        data['spider'] = spider.name
        data['created_at'] = datetime.now().isoformat()

        stats = self.stats.get_stats()

        # convert datetime objects into str
        for key, value in stats.items():
            if isinstance(value, datetime):
                stats[key] = str(value)

            # replace / with _ in keys in default stats
            # for better dictionary keys
            if '/' in key:
                del stats[key]
                key = key.replace('/', '_')
                stats[key] = value

        data['stats'] = stats

        doc_id = hashlib.sha256(data['created_at'].encode()).hexdigest()

        url = host + ":" + port + "/" + index + "/" + doc_type + "/" + doc_id + "/_create"
        headers = {'Content-Type': 'application/json; charset=utf-8'}

        return requests.post(url=url, verify=False, auth=auth,
                             data=json.dumps(data, indent=4, sort_keys=True, default=str),
                             headers=headers)
