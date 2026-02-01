pipeline {
    agent any

    environment {
        APP_NAME        = "devsecops-landing-page"
        IMAGE_NAME      = "prajwal8651/devsecops-landing-page:${GIT_COMMIT}"
        SONARQUBE_ENV   = "SonarQube"
        SONAR_TOKEN     = credentials('sonar-token')
        TRIVY_REPORT    = "trivy-report.html"
    }

    stages {

        stage('Git Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/manjukolkar/Sonar-Travia-Poc.git'
            }
        }

        stage('Code Quality - SonarQube Scan') {
            steps {
                withSonarQubeEnv("${SONARQUBE_ENV}") {
                    sh '''
                        docker run --rm \
                          -e SONAR_HOST_URL=$SONAR_HOST_URL \
                          -e SONAR_TOKEN=$SONAR_TOKEN \
                          -v $WORKSPACE:/usr/src \
                          sonarsource/sonar-scanner-cli \
                          -Dsonar.projectKey=${APP_NAME} \
                          -Dsonar.sources=app
                    '''
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build -t ${IMAGE_NAME} .
                '''
            }
        }

        stage('Security Scan - Trivy (CLI)') {
            steps {
                sh '''
                    trivy image \
                      --severity HIGH,CRITICAL \
                      --exit-code 0 \
                      ${IMAGE_NAME}
                '''
            }
        }

        stage('Security Scan - Trivy HTML Report') {
            steps {
                sh '''
                    trivy image \
                      --format html \
                      --output ${TRIVY_REPORT} \
                      ${IMAGE_NAME}
                '''
            }
        }

        stage('Publish Trivy Report') {
            steps {
                archiveArtifacts artifacts: "${TRIVY_REPORT}", fingerprint: true
            }
        }

        stage('Docker Login') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'docker-hub-creds',
                        usernameVariable: 'DOCKER_USERNAME',
                        passwordVariable: 'DOCKER_PASSWORD'
                    )
                ]) {
                    sh '''
                        echo "$DOCKER_PASSWORD" | docker login \
                        -u "$DOCKER_USERNAME" --password-stdin
                    '''
                }
            }
        }

        stage('Push Image to Docker Hub') {
            steps {
                sh '''
                    docker push ${IMAGE_NAME}
                '''
            }
        }

        stage('Run Container (Test)') {
            steps {
                sh '''
                    docker rm -f ${APP_NAME} || true
                    docker run -d \
                      --name ${APP_NAME} \
                      -p 8000:8000 \
                      ${IMAGE_NAME}
                '''
            }
        }

        stage('Deploy (Optional Placeholder)') {
            steps {
                echo "🚀 Future: ECR / Kubernetes deployment"
            }
        }
    }

    post {
        success {
            echo "✅ Pipeline completed successfully!"
            echo "✔ SonarQube scan completed"
            echo "✔ Trivy security scan completed"
            echo "✔ Docker image pushed to Docker Hub"
            echo "📄 Trivy HTML report archived"
            echo "🌐 App running on port 8000"
        }
        failure {
            echo "❌ Pipeline failed. Check logs."
        }
    }
}


