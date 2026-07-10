pipeline {
  agent any

  environment {
    DOCKER_REGISTRY = 'docker.io'
    DOCKERHUB_NAMESPACE = 'mananjolavisy2'
    IMAGE_NAME = "${env.DOCKERHUB_NAMESPACE}/mlops-fastapi:${env.BUILD_NUMBER}"
    ANSIBLE_HOST_KEY_CHECKING = 'False'
    HOST_WORKSPACE = "${env.HOST_WORKSPACE_BASE}/mlops-pipeline"
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Lint') {
      steps {
        sh '''docker run --rm \
          -v "$HOST_WORKSPACE":/workspace \
          -w /workspace \
          python:3.12-slim \
          sh -lc "pip install -r requirements.txt -r requirements-dev.txt && python -m flake8 src tests && python -m black --check src tests"'''
      }
    }

    stage('Test') {
      steps {
        sh '''docker run --rm \
          -v "$HOST_WORKSPACE":/workspace \
          -w /workspace \
          python:3.12-slim \
          sh -lc "pip install -r requirements.txt -r requirements-dev.txt && python -m pytest"'''
      }
    }

    stage('Build Image') {
      steps {
        sh 'docker build -f docker/Dockerfile -t "$IMAGE_NAME" .'
      }
    }

    stage('Scan Image') {
      steps {
        sh 'docker run --rm -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy:0.53.0 image --exit-code 1 --severity HIGH,CRITICAL "$IMAGE_NAME"'
      }
    }

    stage('Push Image') {
      steps {
        withCredentials([
          usernamePassword(credentialsId: 'dockerhub-account', usernameVariable: 'DOCKER_REGISTRY_USERNAME', passwordVariable: 'DOCKER_REGISTRY_PASSWORD')
        ]) {
          sh 'echo "$DOCKER_REGISTRY_PASSWORD" | docker login "$DOCKER_REGISTRY" -u "$DOCKER_REGISTRY_USERNAME" --password-stdin'
          sh 'docker push "$IMAGE_NAME"'
        }
      }
    }

    stage('Deploy Dev') {
      when {
        branch 'dev'
      }
      steps {
        withCredentials([
          usernamePassword(credentialsId: 'dockerhub-account', usernameVariable: 'DOCKER_REGISTRY_USERNAME', passwordVariable: 'DOCKER_REGISTRY_PASSWORD'),
          sshUserPrivateKey(credentialsId: 'dev-ssh-key', keyFileVariable: 'SSH_KEY')
        ]) {
          sh '''docker run --rm -v "$HOST_WORKSPACE":/workspace -w /workspace -v "$SSH_KEY":/tmp/staging_key python:3.12-slim sh -lc 'pip install ansible && ansible-galaxy collection install -r ansible/requirements.yml && ansible-playbook -i ansible/inventories/dev/hosts.ini ansible/playbooks/deploy.yml --private-key /tmp/staging_key -e image_name="'$IMAGE_NAME'" -e docker_registry="'$DOCKER_REGISTRY'" -e docker_registry_username="'$DOCKER_REGISTRY_USERNAME'" -e docker_registry_password="'$DOCKER_REGISTRY_PASSWORD'"' '''
        }
      }
    }

    stage('Deploy Preprod') {
      when {
        branch 'main'
      }
      steps {
        withCredentials([
          usernamePassword(credentialsId: 'dockerhub-account', usernameVariable: 'DOCKER_REGISTRY_USERNAME', passwordVariable: 'DOCKER_REGISTRY_PASSWORD'),
          sshUserPrivateKey(credentialsId: 'preprod-ssh-key', keyFileVariable: 'SSH_KEY')
        ]) {
          sh '''docker run --rm -v "$HOST_WORKSPACE":/workspace -w /workspace -v "$SSH_KEY":/tmp/staging_key python:3.12-slim sh -lc 'pip install ansible && ansible-galaxy collection install -r ansible/requirements.yml && ansible-playbook -i ansible/inventories/preprod/hosts.ini ansible/playbooks/deploy.yml --private-key /tmp/staging_key -e image_name="'$IMAGE_NAME'" -e docker_registry="'$DOCKER_REGISTRY'" -e docker_registry_username="'$DOCKER_REGISTRY_USERNAME'" -e docker_registry_password="'$DOCKER_REGISTRY_PASSWORD'"' '''
        }
      }
    }

    stage('Deploy Prod') {
      when {
        buildingTag()
      }
      steps {
        input 'Deploy to production?'
        withCredentials([
          usernamePassword(credentialsId: 'dockerhub-account', usernameVariable: 'DOCKER_REGISTRY_USERNAME', passwordVariable: 'DOCKER_REGISTRY_PASSWORD'),
          sshUserPrivateKey(credentialsId: 'prod-ssh-key', keyFileVariable: 'SSH_KEY')
        ]) {
          sh '''docker run --rm -v "$HOST_WORKSPACE":/workspace -w /workspace -v "$SSH_KEY":/tmp/staging_key python:3.12-slim sh -lc 'pip install ansible && ansible-galaxy collection install -r ansible/requirements.yml && ansible-playbook -i ansible/inventories/production/hosts.ini ansible/playbooks/deploy.yml --private-key /tmp/staging_key -e image_name="'$IMAGE_NAME'" -e docker_registry="'$DOCKER_REGISTRY'" -e docker_registry_username="'$DOCKER_REGISTRY_USERNAME'" -e docker_registry_password="'$DOCKER_REGISTRY_PASSWORD'"' '''
        }
      }
    }
  }
}
