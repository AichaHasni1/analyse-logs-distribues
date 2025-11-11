 

---

# 🔍 Système Distribué d’Analyse de Logs avec ELK + Interface Django

Un système léger mais puissant d’analyse de logs basé sur la **stack ELK (Elasticsearch, Logstash, Kibana)** combinée avec **Filebeat** pour l’envoi des logs, ainsi qu’une **interface web développée en Django** permettant la visualisation, l’interaction et le téléchargement des données.

---

## 📝 Aperçu

Ce projet propose un environnement complet et conteneurisé permettant de :

* Collecter les logs avec **Filebeat**
* Les analyser et les transformer via **Logstash**
* Les stocker et les interroger dans **Elasticsearch**
* Visualiser les dashboards dans **Kibana**
* Interagir avec les logs grâce à une **application Django** permettant :

  * Le téléchargement des fichiers de logs
  * Le téléchargement des dashboards
  * L’affichage des rapports d’analyse
  * Le filtrage des logs

---

## 🧰 Technologies Utilisées

| Composant          | Rôle                                          |
| ------------------ | --------------------------------------------- |
| **Docker Compose** | Orchestration des services                    |
| **Filebeat**       | Collecte et envoi des logs                    |
| **Logstash**       | Parsing et traitement centralisé              |
| **Elasticsearch**  | Stockage et moteur de recherche plein texte   |
| **Kibana**         | Visualisation et création de tableaux de bord |
| **Django**         | Interface web utilisateur                     |
| **Python**         | Logique backend et gestion des exports        |

---

## 🏗️ Architecture

```
   [Utilisateur]
         │
   [Filebeat]
         ↓
   [Logstash]
         ↓
 [Elasticsearch]
         ↓
     [Kibana]
```

---

## ✨ Fonctionnalités

### 📥 Collecte & Traitement des Logs

* Collecte automatique des logs système ou applicatifs
* Parsing avec **GROK** (patterns personnalisables)
* Ajout de métadonnées (timestamp, source, etc.)

### 📊 Visualisation & Analyse

* Dashboards interactifs dans **Kibana**
* Export des logs filtrés au format **CSV / JSON**

### 🌐 Interface Django

* Visualisation de métriques
* Téléchargement de logs et dashboards
* Accès direct aux pages Kibana

---

## 📊 Accès à Kibana

➡️ [http://localhost:5601](http://localhost:5601)

* Visualisation des données
* Création et gestion de dashboards
* Export et import de visualisations

---

## 🛠️ Améliorations Possibles

* Détection d’anomalies (Machine Learning)
* Gestion des rôles et permissions (Admin / User)
* Alertes sur conditions critiques

---

 

 

