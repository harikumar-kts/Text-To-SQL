from elasticsearch import Elasticsearch
from src.entity.entity_config import ElasticSearchConfig


class ElasticSearch:

    @staticmethod
    def client_initialization(elastic_config: ElasticSearchConfig):
        return Elasticsearch(
            hosts=elastic_config.hosts,
            basic_auth=(elastic_config.user_id, elastic_config.password)
        )
