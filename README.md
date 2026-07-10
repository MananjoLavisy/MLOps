# Projet MLOps CI/CD

Initialisation d'un projet MLOps conforme au cahier du `Project.pdf` :

- code Machine Learning avec `scikit-learn`
- API `FastAPI` pour servir le modele
- conteneurisation Docker
- pipeline GitLab CI/CD
- deploiement via Docker Compose
- base de monitoring Prometheus

## Structure

```text
.
├── .gitlab-ci.yml
├── .env.example
├── docker-compose.yml
├── docker/
│   └── Dockerfile
├── docs/
├── monitoring/
├── requirements.txt
├── src/
└── tests/
```

## Demarrage rapide

1. Creer un environnement Python.
2. Installer les dependances : `pip install -r requirements.txt`
3. Entrainer le modele : `python -m src.train`
4. Lancer l'API : `uvicorn src.app:app --host 0.0.0.0 --port 8000`

## Tests et qualite

- Tests : `pytest`
- Lint : `flake8 src tests`
- Format check : `black --check src tests`

## Docker

- Build : `docker build -f docker/Dockerfile -t mlops-fastapi .`
- Run : `docker compose up --build`

## Variables CI/CD attendues

- `HARBOR_REGISTRY`
- `HARBOR_PROJECT`
- `HARBOR_USERNAME`
- `HARBOR_PASSWORD`
- `SSH_PRIVATE_KEY`
- `DEPLOY_HOST`
- `DEPLOY_USER`
- `DEPLOY_PATH`

## Cas d'usage retenu

Recommandation de culture agricole a partir du dataset Kaggle `Crop_recommendation`.

## Dataset

- emplacement : `data/Crop_recommendation.csv`
- variables d'entree : `N`, `P`, `K`, `temperature`, `humidity`, `ph`, `rainfall`
- cible : `label`

## Exemple d'appel API

```json
{
  "N": 90,
  "P": 42,
  "K": 43,
  "temperature": 20.87974371,
  "humidity": 82.00274423,
  "ph": 6.502985292000001,
  "rainfall": 202.9355362
}
```
