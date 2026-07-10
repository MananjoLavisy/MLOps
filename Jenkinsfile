pipeline {
  agent any

  environment {
    DOCKER_REGISTRY = 'docker.io'
    DOCKERHUB_NAMESPACE = 'mananjolavisy2'
    IMAGE_NAME = "${env.DOCKERHUB_NAMESPACE}/mlops-fastapi:${env.BUILD_NUMBER}"
    ANSIBLE_HOST_KEY_CHECKING = 'False'
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Lint') {
      steps {
        sh 'python3 -m pip install --user -r requirements.txt'
        sh 'python3 -m flake8 src tests'
        sh 'python3 -m black --check src tests'
      }
    }

    stage('Test') {
      steps {
        sh 'python3 -m pytest'
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

    stage('Deploy Staging') {
      when {
        branch 'main'
      }
      steps {
        sh 'python3 -m pip install --user ansible'
        withCredentials([
          usernamePassword(credentialsId: 'dockerhub-account', usernameVariable: 'DOCKER_REGISTRY_USERNAME', passwordVariable: 'DOCKER_REGISTRY_PASSWORD'),
          sshUserPrivateKey(credentialsId: 'staging-ssh-key', keyFileVariable: 'SSH_KEY')
        ]) {
          sh 'ansible-galaxy collection install -r ansible/requirements.yml'
          sh 'ansible-playbook -i ansible/inventories/staging/hosts.ini ansible/playbooks/deploy.yml --private-key "$SSH_KEY" -e image_name="$IMAGE_NAME" -e docker_registry="$DOCKER_REGISTRY" -e docker_registry_username="$DOCKER_REGISTRY_USERNAME" -e docker_registry_password="$DOCKER_REGISTRY_PASSWORD"'
        }
      }
    }
  }
}
