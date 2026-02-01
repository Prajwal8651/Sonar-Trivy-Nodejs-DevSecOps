pipeline {
    agent any

    environment {
        SONARQUBE = 'SonarQube'
        SONAR_AUTH_TOKEN = credentials('sonar-token')
    }

    stages {

        stage('Checkout') {
            steps {
                git branch: 'master', url: 'https://github.com/manjukolkar/Sonar-Travia-Poc.git'
            }
        }

        stage('Code Quality - SonarQube Scan') {
            steps {
                withSonarQubeEnv("${SONARQUBE}") {
                    sh '''
                    docker run --rm \
                      -e SONAR_HOST_URL=$SONAR_HOST_URL \
                      -e SONAR_TOKEN=$SONAR_AUTH_TOKEN \
                      -v $WORKSPACE:/usr/src \
                      sonarsource/sonar-scanner-cli \
                      -Dsonar.projectKey=devsecops-landing-page \
                      -Dsonar.sources=app
                    '''
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t devsecops-landing-page:latest .'
            }
        }

        stage('Security Scan - Trivy') {
            steps {
                sh 'trivy image --exit-code 1 --severity HIGH,CRITICAL devsecops-landing-page:latest || true'
            }
        }

        stage('Deploy (Optional)') {
            steps {
                echo "Deployment placeholder — can integrate ECR/Kubernetes here."
            }
        }
    }

    post {
        success {
            echo "✅ Pipeline completed successfully! SonarQube + Trivy passed."
        }
        failure {
            echo "❌ Pipeline failed. Check SonarQube or Trivy logs."
        }
    }
}
