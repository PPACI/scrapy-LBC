# LBC spider

Cette araignée, basé sur le framework [Scrapy](https://scrapy.org/)
parcours Leboncoin, analyse les pages et insère les résultats dans une base ElasticSearch.

Combiné avec la solution d'ElasticSearch : Kibana, vous obtenez une solution complète permettant de suivre l'évolution des prix sur LeBonCoin.

## Pré-requis:
* Une base ElasticSearch (disponible via [Docker](https://hub.docker.com/_/elasticsearch/))
* (Optionnel) Kibana pour la visualisation (disponbile via [Docker](https://hub.docker.com/_/kibana/))
* Python 2 ou 3

## Installation
1) Installer les dépendances via `pip install -r requirements.txt`
2) Parametrer votre base ElasticSearch dans `scrapy_LBC/scrapy_LBC/settings.py`
```python
# scrapyelasticsearch configuration
ELASTICSEARCH_SERVERS = ['localhost']
ELASTICSEARCH_INDEX = 'scrapy-lbc'
ELASTICSEARCH_TYPE = 'items'
ELASTICSEARCH_UNIQ_KEY = 'url'
ELASTICSEARCH_BUFFER_LENGTH = 10
```
L'araignée se connectera par défaut sur une base localhost:9200 (paramètre par défaut).
Pour plus d'information sur les paramètres disponible : [scrapy-elasticsearch](https://github.com/knockrentals/scrapy-elasticsearch)

3) Definir vos url de recherche dans le `url.json`
```json
{
  "urls":[
    "https://www.leboncoin.fr/telephonie/offres/lorraine/occasions/?th=1&q=iphone&it=1&parrot=0&ps=7",
    "https://www.leboncoin.fr/ventes_immobilieres/offres/lorraine/occasions/?th=1&parrot=0"
  ]
}
```
4) se placer dans le dossier `./scrapy_LBC`

5) **Lancer l'araignée `scrapy crawl leboncoin`**

Actuellement, l'araignée récupère :
* url
* titre
* date de mise en ligne
* prix
* description
* tous les tags (Ville, Surface d'une maison, Km d'une voiture, etc)

**Par défaut l'araginée ne parcours d'une page par seconde, n'essayez pas de parcours TOUT LeBonCoin à moins d'etre très patient.**

Il est possible d'augmenter la vitesse de l'araignée via les paramètres.
```
# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 1

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 1
```

*L'araignée ne traite maintenant plus deux fois la même annonce (identifié par l'url)'.*

**Mise en garde** : un delai trop faible (0 par exemple) combiné à de nombreuses requetes concurrentes peuvent vous faire bannir temporairement de LeBonCoin. 