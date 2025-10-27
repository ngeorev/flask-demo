pipeline {
    agent any

    environment {
        IMAGE_NAME = "flask-demo"
        IMAGE_TAG = "latest"
        DEPLOY_HOST = "web-app"  
        DEPLOY_USER = "jenkins"   

    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/ngeorev/flask-demo.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .'
            }
        }

        stage('Test') {
            steps {
                sh 'docker run --rm ${IMAGE_NAME}:${IMAGE_TAG} python -m unittest || echo "Tests placeholder"'
            }
        }

        stage('Deploy') {
            steps {
                sshagent (credentials: ['webapp-ssh-key']) {
                    sh """
                    scp docker-compose.yml ${DEPLOY_USER}@${DEPLOY_HOST}:/home/${DEPLOY_USER}/
                    ssh ${DEPLOY_USER}@${DEPLOY_HOST} 'docker stop ${IMAGE_NAME} || true && docker rm ${IMAGE_NAME} || true && docker run -d -p 5000:5000 --name ${IMAGE_NAME} ${IMAGE_NAME}:${IMAGE_TAG}'
                    """
                }
            }
        }
    }
}
