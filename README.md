# 🔍 Distributed Log Analysis System with ELK + Django Interface

A lightweight yet powerful log analysis platform using the **ELK Stack (Elasticsearch, Logstash, Kibana)** combined with **Filebeat** for log shipping and a custom **Django web interface** for visualization, interaction, and download.

---

##  Overview

This project provides a complete, containerized environment to:
- Collect logs using **Filebeat**
- Parse and index logs via **Logstash**
- Store and query logs in **Elasticsearch**
- Visualize data through **Kibana**
- Interact with logs via a **Django application** that allows:
  - downloading the logs file
  - downloading the dashboards file
  - Viewing analysis reports
  - Filtering logs

---

##  Technologies Used

| Component        | Description                                  |
|------------------|----------------------------------------------|
| **Docker Compose** | Orchestrates all services                   |
| **Filebeat**       | Lightweight shipper to collect logs         |
| **Logstash**       | Central log parser and processor            |
| **Elasticsearch**  | Full-text search and storage engine         |
| **Kibana**         | Log visualization and dashboarding          |
| **Django**         | Web UI to interact with log data            |
| **Python**         | Backend logic, log formatting, downloads    |

## Architecture

 [User]
   │
[Filebeat] --> [Logstash] --> [Elasticsearch] --> [Kibana]



##  Features

###  Log Collection & Parsing
- Collect logs from local sources (or simulated logs via Django)
- Grok parsing of logs with custom patterns
- Automatic timestamp recognition and enrichment

###  Dashboards & Analysis
- Use Kibana to explore logs and build interactive dashboards
- Django app embeds Kibana dashboards via iframe
- Option to download filtered logs as CSV or JSON

###  Django Web Interface
- Submit logs via form or file
- Visualize key metrics
- Download logs or anomaly reports (if added later)

## 📊 Kibana Dashboards

- Accessible at [http://localhost:5601](http://localhost:5601)
- Support for saved dashboards and visualizations
- You can export and re-import dashboards if needed.

---

## 📦 Django Interface

Provides:
- Logging interface
- Download dashboard as .ndJSON
- Accessing Kibana

---

## 🛠 Optional Enhancements

- Anomaly Detection (ML) module using Python
- Role-based user access in Django
- Log tagging and alerts


## 👤 Author

**Hind Elqorachi**  
Master’s Student – Data Analytics & AI  
Project GitHub: [github.com/Hindeq/analyse-logs-distribues](https://github.com/Hindeq/analyse-logs-distribues)



