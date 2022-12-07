# Guacamole

## Requêtes Curl
### Base
curl -X GET "https://guacamole.univ-avignon.fr:9200/dblp1/_search.q=sanjuan"
### Sized
curl -X GET "https://guacamole.univ-avignon.fr:9200/dblp1/_search.q=sanjuan&size=1000"
### On specific field
##### lorsqu'on chrche cette article spécifiquement
curl -X GET "https://guacamole.univ-avignon.fr:9200/dblp1/_search.q=_id:1564531496"


à faire : représentation des documents avec WordEmbedding ou LDA (Latent Diricllet Allocation)


fichier à docs2eval.txt à la racine du dossier
Ajouter un identifiant par ligne pour les articles qu'il faut évaluer (pour la colonne title du fichier SP1eval2022.csv)

