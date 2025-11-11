# Ce script teste la connexion à un serveur Elasticsearch local.
# Il vérifie si le serveur Elasticsearch est accessible via l'URL http://localhost:9200.
# Le test passe si la méthode `ping()` retourne True.

import unittest
from elasticsearch import Elasticsearch

class TestElasticsearchConnection(unittest.TestCase):
    def test_connection(self):
        es = Elasticsearch("http://localhost:9200")
        self.assertTrue(es.ping())

if __name__ == '__main__':
    unittest.main()
