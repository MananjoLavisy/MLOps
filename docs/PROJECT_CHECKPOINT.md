# Project Checkpoint

## Purpose

This file is the main restart point for the project.

Use it to answer three questions quickly:

1. What is already done?
2. What is still missing?
3. What is the next exact step to execute?

## Current Project Goal

Build an open source MLOps project with:

- `GitLab CE`
- `Harbor`
- `Ansible`
- `Docker Compose`
- `FastAPI + scikit-learn`
- optional `Jenkins` demo pipeline

Current ML use case:

- agricultural crop recommendation
- dataset file: `data/Crop_recommendation.csv`
- target column: `label`
- features: `N`, `P`, `K`, `temperature`, `humidity`, `ph`, `rainfall`

## Current Repo Status

## Already created

- base Python app structure in `src/`
- tests in `tests/`
- `docker/Dockerfile`
- `docker-compose.yml`
- `.gitlab-ci.yml`
- `Jenkinsfile`
- `docker-compose.jenkins.yml`
- `docs/JENKINS_SETUP.md`
- full `ansible/` scaffold
- project docs in `docs/`
- Word documentation generated from Markdown

## Key files already present

- `README.md`
- `requirements.txt`
- `pyproject.toml`
- `.flake8`
- `.env.example`
- `docker-compose.yml`
- `.gitlab-ci.yml`
- `Jenkinsfile`
- `docs/Documentation_Projet_MLOps_OpenSource.md`
- `docs/Documentation_Projet_MLOps_OpenSource.docx`
- `docs/plan_architecture_final.md`
- `ansible/playbooks/provision.yml`
- `ansible/playbooks/deploy.yml`
- `ansible/playbooks/rollback.yml`

## Technical State

## App

- training script exists
- prediction script exists
- FastAPI app exists
- project is now wired to the Kaggle `Crop_recommendation` dataset
- model artifacts are now centralized in `src/model_artifacts.py`
- training now writes reusable metadata alongside the model
- API exposes `/`, `/health`, `/model-info` and `/predict`
- prediction now returns `recommended_crop` and `confidence`
- prediction validation is now based on stored model metadata
- local tests pass for train, health, model-info, valid prediction, invalid payload and missing model

## Deploy model

- Docker image can be built locally
- Compose file supports `IMAGE_NAME`
- Jenkins pipeline is the primary CI/CD target
- GitLab CI remains secondary/reference only
- local Jenkins compose file exists for easy startup
- Jenkins logic now follows `dev -> dev`, `main -> preprod`, `tag -> prod`

## Infra automation

- inventories exist for `dev`, `preprod` and `production`
- basic roles exist for `common`, `docker`, `app_deploy`, `monitoring`
- Harbor login and compose deploy are modeled in Ansible

## What is still placeholder and must be customized

These values are examples and must be replaced before real deployment:

- `harbor.local`
- staging IP `192.168.56.20`
- production IP `192.168.56.21`
- SSH user/key setup
- Jenkins credentials IDs
- real GitLab CE URL
- real Harbor project and robot account

## Next Recommended Milestone

The next practical milestone is:

**make local training and local container run reproducibly with the real crop dataset**

That means validating in this order:

1. Python environment
2. local training
3. local API run
4. local tests
5. local Docker build
6. local Docker Compose run

## Recommended Execution Order From Here

## Phase 1. Validate local app

Run:

```bash
source .venv/bin/activate
pytest
python -m src.train
uvicorn src.app:app --host 0.0.0.0 --port 8000
```

Check:

```bash
curl http://127.0.0.1:8000/health
```

## Phase 2. Validate Docker locally

Run:

```bash
cp .env.example .env
docker build -f docker/Dockerfile -t mlops-fastapi:local .
docker compose up --build -d
docker compose ps
curl http://127.0.0.1:8000/health
```

## Phase 3. Prepare real infra values

Update these files with real values:

- `ansible/inventories/staging/hosts.ini`
- `ansible/inventories/staging/group_vars/all.yml`
- `ansible/inventories/production/hosts.ini`
- `ansible/inventories/production/group_vars/all.yml`
- `Jenkinsfile`
- `.gitlab-ci.yml`

## Phase 4. Validate Ansible connectivity

Run:

```bash
ansible-galaxy collection install -r ansible/requirements.yml
ansible -i ansible/inventories/staging/hosts.ini staging -m ping
ansible-playbook -i ansible/inventories/staging/hosts.ini ansible/playbooks/provision.yml
```

## Phase 5. Validate remote deploy

Run:

```bash
ansible-playbook -i ansible/inventories/staging/hosts.ini ansible/playbooks/deploy.yml \
  -e image_name="harbor.local/mlops/mlops-fastapi:latest" \
  -e harbor_registry="harbor.local" \
  -e harbor_username="robot$mlops" \
  -e harbor_password="CHANGE_ME"
```

## Checklist

Use this section as a manual progress tracker.

## Done

- [x] Project structure created
- [x] Base docs created
- [x] Main app files created
- [x] Main tests created
- [x] Model artifact helper added
- [x] Model metadata persistence added
- [x] API informational endpoints added
- [x] Prediction validation hardened
- [x] Dockerfile created
- [x] Compose file created
- [x] GitLab CI file created
- [x] Jenkinsfile created
- [x] Ansible scaffold created
- [x] Architecture documentation created
- [x] WSL command documentation created

## To do next

- [ ] Confirm real hostnames, IPs and domains
- [ ] Decide where GitLab CE will run
- [ ] Install Harbor with real config
- [ ] Create real `.env` with `DATASET_PATH=data/Crop_recommendation.csv`
- [x] Re-run local tests in current environment
- [ ] Validate local Docker run
- [ ] Validate local Compose run
- [ ] Validate SSH access to staging
- [ ] Run `provision.yml` on staging
- [ ] Push first image to Harbor
- [ ] Run `deploy.yml` on staging
- [ ] Add monitoring stack runtime if needed
- [ ] Add advanced security tools if needed

## If Work Stops Here

When resuming later, start with this exact sequence:

1. Read `docs/PROJECT_CHECKPOINT.md`
2. Read `docs/Documentation_Projet_MLOps_OpenSource.md`
3. Verify local tools:
   `docker version`, `docker compose version`, `python3 --version`
4. Re-check repo files:
   `README.md`, `.gitlab-ci.yml`, `Jenkinsfile`, `ansible/`
5. Continue with the first unchecked item in `To do next`

## Suggested Update Rule

Each time a meaningful step is completed, update this file:

- move items from `To do next` to done
- note any real IP/domain/credential identifiers used
- add blockers
- add the next exact command to run

## Current Best Next Command

If you want the most useful next command right now:

```bash
source .venv/bin/activate && python -m src.train
```
