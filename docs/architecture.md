# Architecture

## Composants

- `src/train.py` : entraine et exporte le modele
- `src/app.py` : expose l'API REST FastAPI
- `docker/Dockerfile` : construit l'image applicative
- `.gitlab-ci.yml` : lint, tests, build, scan, push et deploiement
- `docker-compose.yml` : execution du service sur l'hote cible
- `monitoring/prometheus.yml` : configuration de collecte des metriques

## Flux cible

1. Push du code sur GitLab.
2. Execution du pipeline CI/CD.
3. Build puis scan de l'image Docker.
4. Push vers Harbor.
5. Deploiement distant via `docker compose`.
