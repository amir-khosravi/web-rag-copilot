pipeline {
    agent any

    environment {
        // Project Configuration
        APP_NAME = 'enterprise-rag-copilot'
        AWS_REGION = 'us-east-1'
        ECR_REPO = 'rag-copilot-repo'
        ECS_CLUSTER = 'production-cluster'
        ECS_SERVICE = 'rag-copilot-service'
        IMAGE_TAG = 'latest'
        
        // Quality Gates
        SONAR_PROJECT_KEY = 'enterprise-rag-copilot'
        SONAR_SCANNER_HOME = tool 'Sonarqube'
    }

    stages {
        stage('SCM Checkout') {
            steps {
                script {
                    echo 'Checking out source code...'
                    // UPDATED: Points to your new repository
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/amir-khosravi/enterprise-rag-copilot.git']])
                }
            }
        }

        stage('Code Quality Analysis') {
            steps {
                withCredentials([string(credentialsId: 'sonarqube-token', variable: 'SONAR_TOKEN')]) {
                    withSonarQubeEnv('Sonarqube') {
                        sh """
                        ${SONAR_SCANNER_HOME}/bin/sonar-scanner \
                        -Dsonar.projectKey=${SONAR_PROJECT_KEY} \
                        -Dsonar.sources=. \
                        -Dsonar.host.url=http://sonarqube-dind:9000 \
                        -Dsonar.login=${SONAR_TOKEN}
                        """
                    }
                }
            }
        }

        stage('Build & Push to AWS ECR') {
            steps {
                withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-token']]) {
                    script {
                        def accountId = sh(script: "aws sts get-caller-identity --query Account --output text", returnStdout: true).trim()
                        def ecrUrl = "${accountId}.dkr.ecr.${env.AWS_REGION}.amazonaws.com/${env.ECR_REPO}"

                        echo "Building and Pushing Docker Image to: ${ecrUrl}"
                        
                        sh """
                        aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ecrUrl}
                        docker build -t ${env.ECR_REPO}:${IMAGE_TAG} .
                        docker tag ${env.ECR_REPO}:${IMAGE_TAG} ${ecrUrl}:${IMAGE_TAG}
                        docker push ${ecrUrl}:${IMAGE_TAG}
                        """
                    }
                }
            }
        }

        stage('Deploy to AWS Fargate') {
            steps {
                withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-token']]) {
                    script {
                        echo "Updating ECS Service: ${ECS_SERVICE}"
                        sh """
                        aws ecs update-service \
                          --cluster ${ECS_CLUSTER} \
                          --service ${ECS_SERVICE} \
                          --force-new-deployment \
                          --region ${AWS_REGION}
                        """
                    }
                }
            }
        }
    }
}