pipeline {
    agent any

    environment {
        IMAGE_NAME = "flask-demo"
        IMAGE_TAG = "latest"
        DEPLOY_HOST = "web-app"   // or IP of your web-app VM
        DEPLOY_USER = "jenkins"    // your SSH user
    }

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
                sh 'echo "No tests yet, continuing..."'
            }
        }

        stage('Deploy') {
            steps {
                sshagent(credentials: ['webapp-ssh-key']) {
                    sh """
                    ssh ${DEPLOY_USER}@${DEPLOY_HOST} 'docker stop ${IMAGE_NAME} || true && docker rm ${IMAGE_NAME} || true'
                    scp Dockerfile ${DEPLOY_USER}@${DEPLOY_HOST}:/home/${DEPLOY_USER}/
                    ssh ${DEPLOY_USER}@${DEPLOY_HOST} 'docker build -t ${IMAGE_NAME}:${IMAGE_TAG} /home/${DEPLOY_USER}/ && docker run -d -p 5000:5000 --name ${IMAGE_NAME} ${IMAGE_NAME}:${IMAGE_TAG}'
                    """
                }
            }
        }
    }
}
