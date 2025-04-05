import os

# Dossiers à créer
folders = ["logs", "src", "tests"]

# Fichiers à créer
files = [
    "src/main.py",
    "src/log_parser.py",
    "src/elasticsearch_config.py",
    "src/log_generator.py",
    "tests/test_log_parser.py",
    "tests/test_elasticsearch.py",
    "logstash.conf",
    "docker-compose.yml",
    "README.md",
    "CONTRIBUTING.md"
]

# Créer les dossiers
for folder in folders:
    os.makedirs(folder, exist_ok=True)

# Créer les fichiers vides
for file in files:
    with open(file, 'w') as f:
        f.write("")  # fichier vide

print("✅ Structure du projet créée avec succès!!!")
