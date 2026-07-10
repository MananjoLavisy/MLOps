# Plan d'architecture final

## Objectif

Mettre en place une chaine MLOps CI/CD open source pour une application FastAPI de prediction Machine Learning, avec build, scan, publication d'image et deploiement automatise.

## Stack retenue

- `GitLab CE` : gestion du code source et pipeline CI/CD principal
- `Jenkins` : pipeline alternatif ou complementaire pour la demo CI/CD
- `Harbor` : registre prive open source pour stocker les images Docker
- `Ansible` : provisionnement des serveurs et deploiement idempotent
- `Docker Compose` : execution de l'application sur le serveur cible
- `FastAPI + scikit-learn` : service ML
- `Prometheus + Grafana` : monitoring
- `Trivy` : scan des images Docker

## Vue d'ensemble

```text
Developpeur
  |
  v
GitLab CE -----------------------> Jenkins (option demo)
  |                                   |
  | CI/CD                             | build/test/scan/push/deploy
  v                                   v
Lint -> Tests -> Build -> Scan -> Push image vers Harbor
                                         |
                                         v
                                      Harbor
                                         |
                                         v
                             Ansible deploy sur serveur cible
                                         |
                                         v
                            Docker Compose + FastAPI + model
                                         |
                                         v
                               Prometheus / Grafana
```

## Responsabilites des composants

## GitLab CE

- heberge le depot Git
- execute le pipeline principal
- stocke les variables CI/CD et credentials

## Jenkins

- sert de pipeline alternatif si une demonstration Jenkins est demandee
- reprend les memes etapes que GitLab CI

## Harbor

- stocke les images construites
- centralise la distribution des images vers staging et production

## Ansible

- prepare les serveurs cibles
- installe Docker et Docker Compose si besoin
- deploie `docker-compose.yml` et `.env`
- fait le `docker login`, le pull et le redemarrage du service
- verifie la disponibilite de l'API apres deploiement

## Docker Compose

- decrit le runtime de l'application
- reference l'image publiee dans Harbor
- gere les variables d'environnement et volumes necessaires

## Flux de deploiement

1. push du code sur `main`
2. lint et tests
3. build de l'image Docker
4. scan de l'image avec `Trivy`
5. push de l'image vers `Harbor`
6. lancement du playbook `Ansible`
7. le serveur cible pull l'image et relance `docker compose`
8. verification de `GET /health`

## Environnements

## Local

- developpement dans WSL
- tests unitaires
- build Docker local
- `docker compose up` pour validation rapide

## Staging

- premier environnement distant automatise
- deploiement automatique depuis `main`
- verification fonctionnelle et technique

## Production

- deploiement manuel apres validation staging
- meme structure que staging avec variables propres

## Organisation Ansible recommandee

```text
ansible/
├── ansible.cfg
├── inventories/
│   ├── staging/
│   │   ├── hosts.ini
│   │   └── group_vars/
│   │       └── all.yml
│   └── production/
│       ├── hosts.ini
│       └── group_vars/
│           └── all.yml
├── playbooks/
│   ├── provision.yml
│   ├── deploy.yml
│   └── rollback.yml
└── roles/
    ├── common/
    ├── docker/
    ├── app_deploy/
    └── monitoring/
```

## Decisions de conception

1. ne pas mettre tous les composants dans un seul conteneur
2. utiliser un seul hote avec plusieurs conteneurs si les ressources sont limitees
3. garder `Harbor` car il est deja open source et pertinent pour le sujet
4. utiliser `Ansible` pour l'automatisation infra/deploiement, pas pour remplacer l'application
5. conserver `Docker Compose` pour rester proche du cahier des charges

## Priorites d'implementation

1. application ML et API
2. conteneurisation
3. pipeline CI/CD
4. registre Harbor
5. deploiement Ansible
6. monitoring
7. securite avancee et signature d'image
