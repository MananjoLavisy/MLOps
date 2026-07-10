# Jenkins Setup

## Run Jenkins locally

```bash
docker compose -f docker-compose.jenkins.yml up -d
docker compose -f docker-compose.jenkins.yml ps
```

Jenkins UI:

```text
http://127.0.0.1:8091
```

## Get initial admin password

```bash
docker exec -it mlops-jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

## Minimum plugins

- Pipeline
- Git
- Docker Pipeline
- Credentials Binding
- SSH Agent

## Docker Hub credential

Create in Jenkins:

- Kind: `Username with password`
- ID: `dockerhub-account`
- Username: your Docker Hub username
- Password: your Docker Hub password or token

## SSH credential for deployment

Create in Jenkins:

- Kind: `SSH Username with private key`
- ID: `staging-ssh-key`
- Username: deploy user on target server

## Use the project

Point Jenkins to this repo and use the root `Jenkinsfile`.
