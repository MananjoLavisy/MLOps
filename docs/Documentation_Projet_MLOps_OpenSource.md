# Documentation complete du projet MLOps open source

## 1. Objectif du projet

Realiser un projet MLOps CI/CD open source autour d'une application Machine Learning exposee avec FastAPI.

Cas d'usage actuellement retenu dans ce repo :

- recommandation de culture agricole
- dataset Kaggle : `Crop_recommendation`
- fichier local : `data/Crop_recommendation.csv`
- cible : `label`

Le cycle cible est le suivant :

1. Ecrire le code ML et API.
2. Linter et tester.
3. Construire l'image Docker.
4. Scanner le code et l'image.
5. Pousser l'image vers un registre prive open source.
6. Deployer automatiquement sur un serveur Linux.
7. Superviser l'application.

## 2. Peut-on faire tout le projet dans un seul Docker ?

### Reponse courte

Oui pour une demonstration tres limitee, mais ce n'est pas la bonne approche pour un vrai projet MLOps CI/CD.

### Ce que veut dire "un seul Docker"

Il y a trois interpretations possibles :

1. Un seul conteneur pour l'application ML seulement.
2. Un seul hote Docker qui execute plusieurs conteneurs.
3. Un seul conteneur geant qui contient GitLab, Harbor, Jenkins, l'app ML et la supervision.

### Evaluation de chaque cas

#### Cas 1. Un seul conteneur pour l'application ML

C'est normal et recommande pour l'application FastAPI elle-meme.

Exemple :

- 1 conteneur `ml-api`
- le modele est charge depuis un volume ou inclus dans l'image

#### Cas 2. Un seul serveur Linux ou WSL avec plusieurs conteneurs

C'est la meilleure approche pour un projet etudiant ou un POC.

Exemple :

- conteneur `gitlab-ce`
- conteneur `harbor` ou autre registre
- conteneur `jenkins` si necessaire
- conteneur `ml-api`
- conteneur `prometheus`
- conteneur `grafana`

C'est simple, open source, peu couteux, et assez realiste.

#### Cas 3. Tout mettre dans un seul mega conteneur

Techniquement possible mais fortement deconseille.

Problemes :

- contraire a la philosophie conteneur
- difficile a maintenir
- difficile a redemarrer proprement
- difficile a securiser
- difficile a expliquer dans un rapport technique

### Conclusion

La bonne approche n'est pas `un seul conteneur`, mais `un seul hote avec plusieurs conteneurs`.

## 3. Toutes les approches open source possibles

## Approche A. Recommandee

`GitLab CE + Harbor + Ansible + Docker Compose + FastAPI + scikit-learn + Prometheus + Grafana`

### Avantages

- tres proche de l'enonce du PDF
- entierement open source en version self-hosted
- Ansible s'integre tres bien
- facile a expliquer dans le rapport
- bonne separation entre CI/CD, registre, deploiement et application

### Inconvenients

- plus lourd a installer qu'un simple projet Docker
- GitLab CE consomme pas mal de RAM

### Quand choisir cette approche

- si tu veux coller au sujet initial
- si tu veux garder `GitLab CE`
- si tu veux ajouter Ansible proprement

## Approche B

`Jenkins + Harbor + Ansible + Docker Compose`

### Avantages

- completement open source
- Jenkins est tres connu pour les pipelines
- plus flexible pour demontrer CI/CD classique

### Inconvenients

- un peu moins aligne avec l'enonce qui mentionne GitLab
- demande souvent plus de configuration manuelle

## Approche C

`GitLab CE + Registry integre GitLab + Ansible + Docker Compose`

### Avantages

- architecture plus simple
- moins de composants a administrer

### Inconvenients

- tu perds la demonstration specifique Harbor
- moins riche sur la partie registry securisee

## Approche D

`Gitea ou Forgejo + Drone CI ou Woodpecker + Harbor + Ansible`

### Avantages

- stack tres open source et legere
- moderne et plus facile a auto-heberger sur petite machine

### Inconvenients

- moins proche du sujet demande
- peut etre moins defendable face a un enonce centre sur GitLab

## Approche E

`GitLab CE + Harbor + Ansible + Kubernetes`

### Avantages

- tres professionnelle
- excellente demonstration DevOps/MLOps

### Inconvenients

- trop lourde pour un premier projet si Compose suffit
- complexite largement superieure

## 4. Approche retenue

Je recommande **Approche A** :

1. GitLab CE pour le code source et le CI/CD.
2. Harbor pour le registre d'images prive.
3. Ansible pour le provisionnement et le deploiement.
4. Docker Compose pour l'execution de l'application sur le serveur cible.
5. Prometheus et Grafana pour le monitoring.

## 5. Pourquoi Ansible est utile ici

Ansible ne remplace pas GitLab CE.

Ansible ajoute la couche **automatisation d'infrastructure et de deploiement**.

Il sert a :

1. Installer Docker sur le serveur cible.
2. Installer le plugin Docker Compose.
3. Creer les dossiers de deploiement.
4. Copier ou generer le fichier `.env`.
5. Copier ou templatiser `docker-compose.yml`.
6. Faire le login au registre.
7. Pull la bonne image Docker.
8. Lancer `docker compose up -d`.
9. Verifier `http://host:port/health`.

## 6. Architecture finale recommandee

```text
Developpeur
   |
   v
GitLab CE
   |
   | pipeline CI/CD
   v
Lint -> Tests -> Build -> Scan -> Push Harbor -> Deploy Ansible
                                              |
                                              v
                                           Harbor
                                              |
                                              v
                                   Serveur cible Linux/WSL
                                     - Docker Engine
                                     - Docker Compose
                                     - Application FastAPI ML
                                     - Prometheus
                                     - Grafana
```

## 7. Architecture logicielle dans le repo

```text
.
├── .gitlab-ci.yml
├── .env.example
├── docker-compose.yml
├── docker/
│   └── Dockerfile
├── src/
│   ├── train.py
│   ├── predict.py
│   └── app.py
├── tests/
│   ├── test_train.py
│   └── test_api.py
├── ansible/
│   ├── ansible.cfg
│   ├── inventories/
│   │   ├── staging/
│   │   └── production/
│   ├── playbooks/
│   │   ├── provision.yml
│   │   ├── deploy.yml
│   │   └── rollback.yml
│   └── roles/
│       ├── common/
│       ├── docker/
│       ├── app_deploy/
│       └── monitoring/
├── monitoring/
│   ├── prometheus.yml
│   └── grafana/
└── docs/
```

## 8. Regles de conception du projet

## Regles techniques

1. Un composant, une responsabilite principale.
2. Les secrets ne doivent jamais etre commits dans Git.
3. L'image Docker doit etre reproductible.
4. Les tests doivent tourner avant tout build de production.
5. Le scan securite doit bloquer les niveaux critiques.
6. Les deploiements doivent etre idempotents.
7. Les environnements `staging` et `production` doivent etre separes.
8. Les tags d'image doivent etre explicites : SHA, version ou date.

## Regles de code

1. Utiliser `black` pour le formatage.
2. Utiliser `flake8` pour le lint.
3. Utiliser `pytest` pour les tests.
4. Ajouter des tests API et modele.
5. Garder les fichiers `src/` petits et lisibles.

## Regles de securite

1. Scanner le code source avec `bandit` ou `semgrep`.
2. Scanner les secrets avec `gitleaks`.
3. Scanner les dependances avec `pip-audit` ou `OWASP Dependency Check`.
4. Scanner l'image avec `trivy`.
5. Signer l'image avec `cosign`.

## 9. Skills a maitriser

## Niveau application

- Python 3.11
- FastAPI
- scikit-learn
- gestion de modele avec `joblib`
- ecriture de tests `pytest`

## Niveau conteneurs

- Dockerfile
- build d'image
- volumes
- variables d'environnement
- Docker Compose

## Niveau CI/CD

- Git et GitLab CE
- `.gitlab-ci.yml`
- runners GitLab
- artefacts et variables CI/CD

## Niveau automatisation

- Ansible inventory
- playbooks
- roles
- templates Jinja2
- idempotence
- connexion SSH

## Niveau securite

- scan de dependances
- scan de secrets
- scan d'images
- signature d'images

## Niveau systeme

- Linux
- systemd basique
- droits utilisateurs
- reseau Docker
- WSL2

## 10. Materiel et prerequis minimaux

## Machine locale

- Windows 10/11 avec WSL2
- Ubuntu dans WSL2
- Docker Desktop avec integration WSL ou Docker Engine dans WSL
- Git
- Python 3.11

## Serveur cible

- Ubuntu Server 22.04 ou 24.04
- acces SSH
- Docker Engine
- Docker Compose plugin

## Ressources minimales conseillees

- 8 Go RAM minimum
- 16 Go preferable si GitLab CE tourne sur la meme machine
- 40 Go de disque minimum

## 11. Demarrage from scratch

Cette section suppose que tu commences de zero, avec seulement une machine Windows + WSL2 ou une machine Linux.

## Ordre recommande avant d'ecrire le code applicatif

1. verifier WSL2 et Docker
2. preparer la structure du repo
3. pull les images Docker d'infrastructure utiles
4. preparer les fichiers de configuration du projet
5. seulement apres, ecrire le code Python dans `src/`

## Ce qu'il faut preparer avant de coder

Avant d'ecrire `train.py`, `predict.py` ou `app.py`, prepare d'abord les fichiers qui definissent le cadre du projet.

## Fichiers a preparer en premier

### Fichiers racine

- `README.md`
- `.gitignore`
- `requirements.txt`
- `pyproject.toml`
- `.flake8`
- `.env.example`
- `.gitlab-ci.yml`
- `Jenkinsfile` si tu veux aussi la variante Jenkins

### Fichiers Docker

- `docker/Dockerfile`
- `.dockerignore`
- `docker-compose.yml`

### Fichiers application vides ou squelette

- `src/__init__.py`
- `src/train.py`
- `src/predict.py`
- `src/app.py`

### Fichiers de test

- `tests/test_train.py`
- `tests/test_api.py`

### Fichiers Ansible

- `ansible/ansible.cfg`
- `ansible/requirements.yml`
- `ansible/inventories/staging/hosts.ini`
- `ansible/inventories/staging/group_vars/all.yml`
- `ansible/inventories/production/hosts.ini`
- `ansible/inventories/production/group_vars/all.yml`
- `ansible/playbooks/provision.yml`
- `ansible/playbooks/deploy.yml`
- `ansible/playbooks/rollback.yml`

### Templates et roles Ansible

- `ansible/roles/common/tasks/main.yml`
- `ansible/roles/docker/tasks/main.yml`
- `ansible/roles/app_deploy/tasks/main.yml`
- `ansible/roles/app_deploy/templates/env.j2`
- `ansible/roles/app_deploy/templates/docker-compose.yml.j2`

### Fichiers documentation

- `docs/cahier_des_charges.md`
- `docs/architecture.md`
- `docs/rapport_final.md`
- `docs/plan_architecture_final.md`

### Fichiers monitoring

- `monitoring/prometheus.yml`
- `monitoring/grafana/`

## Ordre de creation conseille des fichiers

1. `README.md`
2. `.gitignore`
3. `requirements.txt`
4. `pyproject.toml`
5. `.env.example`
6. `docker/Dockerfile`
7. `docker-compose.yml`
8. `.gitlab-ci.yml`
9. structure `ansible/`
10. ensuite seulement `src/*.py`
11. puis `tests/*.py`

## 12. Images Docker a pull au debut du projet

Il ne faut pas pull toutes les images possibles avant de coder. Il faut surtout preparer celles qui servent au socle du projet et a l'infrastructure de demo.

## Images minimales recommandees

### 1. Image de base applicative

```bash
docker pull python:3.11-slim
```

Utilisation : base de ton `docker/Dockerfile`.

### 2. GitLab CE

```bash
docker pull gitlab/gitlab-ce:latest
```

Utilisation : depot Git self-hosted et pipeline CI/CD si tu installes GitLab CE toi-meme.

### 3. Trivy

```bash
docker pull aquasec/trivy:0.53.0
```

Utilisation : scan de l'image Docker construite.

### 4. Prometheus

```bash
docker pull prom/prometheus:latest
```

Utilisation : collecte des metriques.

### 5. Grafana

```bash
docker pull grafana/grafana:latest
```

Utilisation : visualisation et dashboards.

## Images optionnelles selon les choix de projet

### Jenkins

```bash
docker pull jenkins/jenkins:lts
```

Utilisation : pipeline CI/CD alternatif ou demonstration Jenkins.

### PostgreSQL pour MLflow

```bash
docker pull postgres:16
```

Utilisation : base backend pour MLflow.

### MLflow

```bash
docker pull ghcr.io/mlflow/mlflow:latest
```

Utilisation : tracking d'experiences ML.

### Gitleaks

```bash
docker pull zricethezav/gitleaks:latest
```

Utilisation : detection de secrets.

### Semgrep

```bash
docker pull returntocorp/semgrep:latest
```

Utilisation : scan SAST du code source.

## Cas particulier de Harbor

Harbor n'est pas un simple composant qu'on prepare avec un seul `docker pull` avant le projet.

En pratique :

1. tu telecharges le package d'installation officiel Harbor
2. tu configures `harbor.yml`
3. le script d'installation Harbor recupere ensuite les images necessaires

Donc pour Harbor, la bonne logique est :

- preparer son installation
- pas juste faire un pull manuel d'une image unique

## Checklist de pull conseillee au tout debut

Si tu veux preparer ton labo des le premier jour, execute au moins :

```bash
docker pull python:3.11-slim
docker pull gitlab/gitlab-ce:latest
docker pull aquasec/trivy:0.53.0
docker pull prom/prometheus:latest
docker pull grafana/grafana:latest
```

Si tu veux aussi la variante Jenkins :

```bash
docker pull jenkins/jenkins:lts
```

## 13. Sequence de travail from scratch

## Etape 0. Verifier l'environnement local

Commandes utiles :

```bash
docker version
docker compose version
python3 --version
git --version
```

## Etape 1. Creer le repo et l'arborescence

Creer au minimum :

```text
.
├── README.md
├── .gitignore
├── requirements.txt
├── pyproject.toml
├── .env.example
├── docker-compose.yml
├── docker/
│   └── Dockerfile
├── src/
├── tests/
├── docs/
├── monitoring/
└── ansible/
```

## Etape 2. Ecrire les fichiers de cadre avant le code metier

Commencer par :

1. `README.md`
2. `.gitignore`
3. `requirements.txt`
4. `.env.example`
5. `docker/Dockerfile`
6. `docker-compose.yml`
7. `.gitlab-ci.yml`
8. `ansible/ansible.cfg`

## Etape 3. Ecrire ensuite le code applicatif

Ordre conseille :

1. `src/train.py`
2. `src/predict.py`
3. `src/app.py`
4. `tests/test_train.py`
5. `tests/test_api.py`

## Etape 4. Tester localement avant CI/CD

1. lancer le train localement
2. lancer l'API localement
3. lancer les tests
4. build l'image Docker
5. lancer `docker compose up`

## Etape 5. Installer ensuite l'infrastructure

1. GitLab CE
2. Harbor
3. Runner GitLab ou Jenkins
4. Prometheus et Grafana
5. serveur cible de staging

## Etape 6. Ajouter le deploiement Ansible

1. remplir les inventories
2. tester `provision.yml`
3. tester `deploy.yml`
4. brancher Ansible dans le pipeline

## 14. Commandes exactes a lancer dans WSL

Cette section donne une sequence de commandes concretement executable si tu commences depuis zero dans Ubuntu WSL2.

## 14.1. Verifier les outils de base

```bash
uname -a
pwd
python3 --version
git --version
docker version
docker compose version
```

Si `docker version` echoue, verifier Docker Desktop et l'integration WSL.

## 14.2. Creer un dossier de travail Linux recommande

```bash
mkdir -p ~/projects
cd ~/projects
mkdir -p mlops
cd mlops
pwd
```

Si tu veux absolument travailler dans un disque Windows monte dans WSL :

```bash
mkdir -p "/mnt/d/ws/MLOps"
cd "/mnt/d/ws/MLOps"
pwd
```

## 14.3. Initialiser Git si le projet est local

```bash
git init
git branch -M main
```

## 14.4. Pull les images Docker minimales

```bash
docker pull python:3.11-slim
docker pull gitlab/gitlab-ce:latest
docker pull aquasec/trivy:0.53.0
docker pull prom/prometheus:latest
docker pull grafana/grafana:latest
```

Si tu veux aussi Jenkins :

```bash
docker pull jenkins/jenkins:lts
```

Si tu veux MLflow plus tard :

```bash
docker pull postgres:16
docker pull ghcr.io/mlflow/mlflow:latest
```

## 14.5. Creer l'arborescence du projet

```bash
mkdir -p src tests docker docs monitoring/grafana models
mkdir -p ansible/inventories/staging/group_vars
mkdir -p ansible/inventories/production/group_vars
mkdir -p ansible/playbooks
mkdir -p ansible/roles/common/tasks
mkdir -p ansible/roles/docker/tasks
mkdir -p ansible/roles/app_deploy/tasks
mkdir -p ansible/roles/app_deploy/templates
mkdir -p ansible/roles/monitoring/tasks
```

## 14.6. Creer les fichiers de base a preparer avant le code

```bash
touch README.md .gitignore requirements.txt pyproject.toml .flake8 .env.example .gitlab-ci.yml Jenkinsfile docker-compose.yml
touch docker/Dockerfile .dockerignore
touch src/__init__.py src/train.py src/predict.py src/app.py
touch tests/test_train.py tests/test_api.py
touch docs/cahier_des_charges.md docs/architecture.md docs/rapport_final.md docs/plan_architecture_final.md
touch monitoring/prometheus.yml monitoring/grafana/.gitkeep
touch ansible/ansible.cfg ansible/requirements.yml
touch ansible/inventories/staging/hosts.ini ansible/inventories/staging/group_vars/all.yml
touch ansible/inventories/production/hosts.ini ansible/inventories/production/group_vars/all.yml
touch ansible/playbooks/provision.yml ansible/playbooks/deploy.yml ansible/playbooks/rollback.yml
touch ansible/roles/common/tasks/main.yml
touch ansible/roles/docker/tasks/main.yml
touch ansible/roles/app_deploy/tasks/main.yml
touch ansible/roles/app_deploy/templates/env.j2
touch ansible/roles/app_deploy/templates/docker-compose.yml.j2
touch ansible/roles/monitoring/tasks/main.yml
```

## 14.7. Creer et activer l'environnement Python local

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

## 14.8. Installer les dependances du projet

Quand `requirements.txt` est rempli :

```bash
pip install -r requirements.txt
```

Exemple si tu veux demarrer rapidement a la main :

```bash
pip install fastapi uvicorn scikit-learn joblib pytest flake8 black httpx prometheus-fastapi-instrumentator
```

## 14.9. Verifier la qualite du code localement

Apres avoir ecrit le code dans `src/` et `tests/` :

```bash
pytest
flake8 src tests
black --check src tests
```

## 14.10. Entrainer le modele localement

```bash
python -m src.train
ls models
```

## 14.11. Lancer l'API localement sans Docker

```bash
uvicorn src.app:app --host 0.0.0.0 --port 8000
```

Dans un autre terminal WSL :

```bash
curl http://127.0.0.1:8000/health
```

## 14.12. Construire l'image Docker de l'application

```bash
docker build -f docker/Dockerfile -t mlops-fastapi:local .
```

## 14.13. Lancer l'application avec Docker Compose

Si `.env` n'existe pas encore :

```bash
cp .env.example .env
```

Puis :

```bash
docker compose up --build -d
docker compose ps
curl http://127.0.0.1:8000/health
```

Pour arreter :

```bash
docker compose down
```

## 14.14. Installer Ansible dans WSL

Avec l'environnement virtuel actif :

```bash
pip install ansible
ansible --version
ansible-galaxy collection install -r ansible/requirements.yml
```

## 14.15. Tester la connectivite SSH vers le serveur cible

```bash
ssh deploy@192.168.56.20
```

Si besoin de copier ta cle publique :

```bash
ssh-copy-id deploy@192.168.56.20
```

## 14.16. Tester l'inventory Ansible

```bash
ansible -i ansible/inventories/staging/hosts.ini staging -m ping
```

## 14.17. Provisionner le serveur cible avec Ansible

```bash
ansible-playbook -i ansible/inventories/staging/hosts.ini ansible/playbooks/provision.yml
```

## 14.18. Deployer l'application avec Ansible

```bash
ansible-playbook -i ansible/inventories/staging/hosts.ini ansible/playbooks/deploy.yml \
  -e image_name="harbor.local/mlops/mlops-fastapi:latest" \
  -e harbor_registry="harbor.local" \
  -e harbor_username="robot$mlops" \
  -e harbor_password="CHANGE_ME"
```

## 14.19. Pull une image privee Harbor depuis WSL

```bash
docker login harbor.local
docker pull harbor.local/mlops/mlops-fastapi:latest
```

## 14.20. Commandes Git utiles pendant le projet

```bash
git status
git add .
git commit -m "Initialize MLOps project structure"
```

## 14.21. Pousser le code vers GitLab CE

Exemple si le depot distant existe deja :

```bash
git remote add origin http://gitlab.local/root/mlops.git
git push -u origin main
```

## 15. Detail important WSL et Docker

## Option la plus simple sous Windows

Utiliser **Docker Desktop avec integration WSL2**.

Dans ce cas :

1. Docker tourne cote Windows.
2. Tu l'utilises directement depuis Ubuntu WSL.
3. Les commandes `docker`, `docker compose`, `docker pull` fonctionnent dans WSL.

### Verification

```bash
docker version
docker compose version
```

## Comment pull une image dans WSL

Exemples :

```bash
docker pull python:3.11-slim
docker pull gitlab/gitlab-ce:latest
docker pull jenkins/jenkins:lts
docker pull quay.io/trivy/trivy:latest
```

Pour Harbor prive :

```bash
docker login harbor.mon-domaine.local
docker pull harbor.mon-domaine.local/mlops/ml-api:latest
```

## Si Docker ne marche pas dans WSL

Verifier :

1. que Docker Desktop est demarre
2. que l'integration WSL est activee
3. que ta distribution Ubuntu est cochee dans Docker Desktop

## Emplacement conseille du projet sous WSL

Preferer un projet dans le filesystem Linux pour de meilleures performances, par exemple :

```bash
/home/<user>/projects/mlops
```

Au lieu de travailler principalement dans :

```bash
/mnt/d/...
```

Ce n'est pas obligatoire, mais souvent plus rapide pour Docker et Python.

## 16. Etapes de realisation du projet

## Phase 1. Initialisation du projet

1. Creer le repo GitLab CE.
2. Initialiser la structure des dossiers.
3. Ajouter `README`, `.gitignore`, `requirements.txt`.
4. Definir le cas d'usage ML.

## Phase 2. Code ML

1. Choisir un dataset.
2. Ecrire `src/train.py`.
3. Sauvegarder le modele avec `joblib`.
4. Ecrire `src/predict.py`.
5. Stocker les metriques d'entrainement.

## Phase 3. API FastAPI

1. Ecrire `src/app.py`.
2. Ajouter route `/health`.
3. Ajouter route `/predict`.
4. Ajouter route `/metrics` avec Prometheus.

## Phase 4. Tests

1. Tester l'entrainement.
2. Tester la prediction.
3. Tester l'API avec `TestClient`.

## Phase 5. Conteneurisation

1. Ecrire `docker/Dockerfile`.
2. Ajouter `.dockerignore`.
3. Construire l'image localement.
4. Lancer le conteneur localement.

## Phase 6. Docker Compose

1. Ecrire `docker-compose.yml`.
2. Ajouter `.env.example`.
3. Lancer `docker compose up -d`.
4. Verifier le port et les endpoints.

## Phase 7. GitLab CE CI/CD

1. Configurer un runner GitLab.
2. Ecrire `.gitlab-ci.yml`.
3. Ajouter jobs lint, test, build, scan, push, deploy.
4. Configurer variables CI/CD.

## Phase 8. Harbor

1. Installer Harbor.
2. Creer un projet `mlops`.
3. Creer un utilisateur robot ou technique.
4. Configurer l'authentification du pipeline.

## Phase 9. Ansible

1. Creer `ansible/ansible.cfg`.
2. Creer les inventories `staging` et `production`.
3. Ecrire `playbooks/provision.yml`.
4. Ecrire `playbooks/deploy.yml`.
5. Ajouter des roles `docker` et `app_deploy`.
6. Integrer l'appel Ansible dans le pipeline GitLab.

## Phase 10. Monitoring

1. Configurer Prometheus.
2. Exposer les metriques FastAPI.
3. Ajouter Grafana.
4. Construire un dashboard simple.

## Phase 11. Securite

1. `gitleaks` pour secrets.
2. `bandit` ou `semgrep` pour SAST.
3. `pip-audit` pour dependances Python.
4. `trivy` pour image Docker.
5. `cosign` pour signature d'image.

## 13. Codes et fichiers a implementer

## `src/train.py`

Responsabilite : entrainer le modele et exporter `models/model.joblib`.

## `src/predict.py`

Responsabilite : charger le modele et produire une prediction locale.

## `src/app.py`

Responsabilite : exposer l'API REST.

Routes minimales :

- `GET /health`
- `POST /predict`
- `GET /metrics`

## `docker/Dockerfile`

Responsabilite : construire une image reproducible.

Regles :

1. partir d'une image Python stable
2. installer les dependances depuis `requirements.txt`
3. copier seulement le necessaire
4. lancer `uvicorn`

## `docker-compose.yml`

Responsabilite : lancer l'application et, si souhaite, la supervision.

## `.gitlab-ci.yml`

Responsabilite : automatiser lint, tests, build, scan, push et deploy.

## `ansible/playbooks/provision.yml`

Responsabilite : preparer le serveur cible.

## `ansible/playbooks/deploy.yml`

Responsabilite : deployer l'application depuis le registre.

## 14. Exemple minimal de pipeline GitLab CE

```yaml
stages:
  - lint
  - test
  - build
  - scan
  - push
  - deploy

lint:
  stage: lint
  image: python:3.11-slim
  script:
    - pip install -r requirements.txt
    - flake8 src tests
    - black --check src tests

test:
  stage: test
  image: python:3.11-slim
  script:
    - pip install -r requirements.txt
    - pytest

build:
  stage: build
  image: docker:stable
  services:
    - docker:dind
  script:
    - docker build -f docker/Dockerfile -t "$IMAGE_TAG" .

scan:
  stage: scan
  image: aquasec/trivy:latest
  script:
    - trivy image --exit-code 1 --severity HIGH,CRITICAL "$IMAGE_TAG"

deploy:
  stage: deploy
  image: python:3.11-slim
  script:
    - pip install ansible
    - ansible-playbook -i ansible/inventories/staging/hosts.ini ansible/playbooks/deploy.yml
```

## 15. Exemple minimal d'inventory Ansible

```ini
[staging]
192.168.1.50 ansible_user=ubuntu

[production]
192.168.1.60 ansible_user=ubuntu
```

## 16. Exemple minimal de playbook Ansible de deploiement

```yaml
- hosts: staging
  become: true
  vars:
    deploy_path: /opt/mlops-app
    image_name: harbor.local/mlops/ml-api:latest
  tasks:
    - name: Create deploy directory
      file:
        path: "{{ deploy_path }}"
        state: directory
        mode: "0755"

    - name: Copy docker compose file
      copy:
        src: ../../docker-compose.yml
        dest: "{{ deploy_path }}/docker-compose.yml"
        mode: "0644"

    - name: Login to registry
      community.docker.docker_login:
        registry_url: harbor.local
        username: "{{ harbor_username }}"
        password: "{{ harbor_password }}"

    - name: Start application
      community.docker.docker_compose_v2:
        project_src: "{{ deploy_path }}"
        pull: always
        state: present
```

## 17. Comment installer et utiliser GitLab CE

## Option simple pour labo ou POC

Lancer GitLab CE en conteneur sur une machine dediee ou un hote separant bien les roles.

Exemple de pull :

```bash
docker pull gitlab/gitlab-ce:latest
```

Points d'attention :

1. GitLab CE consomme beaucoup de RAM.
2. Il vaut mieux lui reserver un stockage persistant.
3. Le runner peut etre sur la meme machine ou une autre.

## 18. Comment realiser le deploiement depuis WSL

## Depuis ta machine locale

1. Tu developpes dans WSL.
2. Tu pushes vers GitLab CE.
3. Le runner GitLab execute le pipeline.
4. Le pipeline pousse l'image vers Harbor.
5. Le pipeline lance Ansible.
6. Ansible se connecte en SSH au serveur cible.
7. Le serveur cible pull l'image depuis Harbor.

## Flux de pull d'image sur le serveur cible

```text
Serveur cible -> docker login Harbor -> docker pull image -> docker compose up -d
```

## 19. Strategie de deploiement recommandee

## Environnements

1. `dev` : local dans WSL
2. `staging` : serveur de test
3. `production` : serveur final

## Cycle

1. developpement local
2. tests locaux
3. push GitLab CE
4. pipeline auto
5. deploiement staging auto
6. validation manuelle
7. deploiement production manuel

## 20. Roadmap de realisation par petites etapes

## Etape 1

Faire marcher l'application FastAPI locale sans Docker.

## Etape 2

Faire marcher le modele ML avec sauvegarde du fichier `joblib`.

## Etape 3

Ecrire les tests `pytest`.

## Etape 4

Mettre l'app dans Docker.

## Etape 5

Faire marcher `docker compose` en local.

## Etape 6

Installer GitLab CE et enregistrer un runner.

## Etape 7

Installer Harbor et tester `docker login` puis `docker push`.

## Etape 8

Mettre en place le pipeline GitLab CE.

## Etape 9

Ajouter Ansible et automatiser le deploiement `staging`.

## Etape 10

Ajouter le monitoring Prometheus/Grafana.

## Etape 11

Ajouter le scan de securite et la signature des images.

## Etape 12

Documenter et faire la demonstration finale.

## 21. Ce qu'il ne faut pas faire

1. Mettre tous les composants dans un seul mega conteneur.
2. Commit les mots de passe dans Git.
3. Deployer en production sans staging.
4. Builder une image sans tests ni scans.
5. Faire un playbook Ansible non idempotent.

## 22. Conclusion

Oui, les deux options peuvent etre open source si tu prends **GitLab CE** et non une edition fermee, et si tu gardes **Harbor** qui est deja open source.

Pour ce projet, l'approche la plus defendable et pedagogique est :

1. `GitLab CE` pour repository + pipeline.
2. `Harbor` pour le registre.
3. `Ansible` pour le provisionnement et le deploiement.
4. `Docker Compose` pour le runtime.
5. `FastAPI + scikit-learn` pour l'application ML.
6. `Prometheus + Grafana` pour la supervision.

Cette approche est a la fois :

- open source
- proche du sujet initial
- realisable sur une machine modeste
- facile a expliquer dans un rapport et une soutenance
