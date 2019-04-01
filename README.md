# Scrapy-ElasticStats
Send Scrapy stats to ElasticSearch

A scrapy middleware for sending stats to ElasticSearch

Add the custom middleware to your middlewares.py
Don't forget the import statements

Add the following lines to settings.py:

EXTENSIONS = {

    'PROJECT_NAME.middlewares.ElasticStatsSender': 910,
    
}

#Replace values as appropriate

ELASTICSTATS_ENABLED = 'True/False'

ELASTICSEARCH_AUTH = ("USERNAME", "PASSWORD")

ELASTICSEARCH_SERVERS = 'SERVER IP'     eg. "https://192.65.23.10"

ELASTICSEARCH_PORT = 'PORT'             eg. "5601"

ELASTICSEARCH_USE_SSL = 'True/False'

ELASTICSTATS_INDEX = 'INDEX NAME'       eg. "ElasticStats"

ELASTICSTATS_TYPE = '_doc'
