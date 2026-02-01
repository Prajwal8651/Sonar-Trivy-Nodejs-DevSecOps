pipeline {
    agent any

    environment {
        APP_NAME       = "devsecops-landing-page"
        IMAGE_REPO     = "prajwal8651/devsecops-landing-page"
        IMAGE_NAME     = "prajwal8651/devsecops-landing-page:${GIT_COMMIT}"
        SONARQUBE_ENV  = "SonarQube"
        SONAR_TOKEN    = credentials('sonar-token')
        TRIVY_JSON     = "trivy-report.json"
        TRIVY_HTML     = "trivy-report.html"
    }

    stages {

        stage('Git Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/manjukolkar/Sonar-Travia-Poc.git'
            }
        }

        stage('Cleanup Old Container') {
            steps {
                sh 'docker rm -f ${APP_NAME} || true'
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
                sh 'docker build -t ${IMAGE_NAME} .'
            }
        }

        stage('Security Scan - Trivy (JSON Report)') {
            steps {
                sh '''
                    trivy image \
                      --severity HIGH,CRITICAL \
                      --format json \
                      --output ${TRIVY_JSON} \
                      ${IMAGE_NAME}
                '''
            }
        }

        stage('Convert Trivy JSON → HTML') {
            steps {
                sh '''
                    trivy convert \
                      --format html \
                      --output ${TRIVY_HTML} \
                      ${TRIVY_JSON}
                '''
            }
        }

        stage('Publish Trivy Reports') {
            steps {
                archiveArtifacts artifacts: "${TRIVY_JSON}, ${TRIVY_HTML}", fingerprint: true
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
                sh 'docker push ${IMAGE_NAME}'
            }
        }

        stage('Run Container (Test)') {
            steps {
                sh '''
                    docker run -d \
                      --name ${APP_NAME} \
                      -p 8000:8000 \
                      ${IMAGE_NAME}
                '''
            }
        }
    }

    post {

        always {
            echo "🧹 Cleaning Docker images"

            sh '''
                docker image prune -f
                docker images ${IMAGE_REPO} --format "{{.ID}} {{.Tag}}" \
                | grep -v ${GIT_COMMIT} \
                | awk '{print $1}' \
                | xargs -r docker rmi -f || true
            '''
        }

        success {
            echo "✅ Pipeline completed successfully"
            echo "✔ Trivy JSON & HTML reports generated"
            echo "✔ Docker image pushed"
            echo "🌐 App running on port 8000"
        }

        failure {
            echo "❌ Pipeline failed. Check logs."
        }
    }
}

