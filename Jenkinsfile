pipeline {
    agent any

    environment {
        IMAGE_NAME = 'multi-ai-agent'
        IMAGE_TAG = 'latest'
    }

    stages {
        stage('Cloning GitHub Repository') {
            steps {
                script {
                    echo 'Cloning GitHub repo into Jenkins...'
                    // checkout scmGit(   // ❌ scmGit is deprecated; replaced with checkout() below
                    checkout([
                        $class: 'GitSCM',
                        branches: [[name: '*/main']],
                        extensions: [],
                        userRemoteConfigs: [[
                            url: 'https://github.com/data-guru0/MULTI-AI-AGENT-PROJECTS.git',
                            credentialsId: 'github-token' // ✅ Add Jenkins credential ID
                        ]]
                    ])
                    // )
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    echo 'Building Docker image...'
                    sh """
                    docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .
                    """
                }
            }
        }

        stage('Run Docker Container (Test)') {
            steps {
                script {
                    echo 'Running container locally for testing...'
                    // Added pre-cleanup to avoid duplicate container issues
                    sh """
                    docker rm -f ${IMAGE_NAME}_container || true
                    docker run -d -p 8080:8080 --name ${IMAGE_NAME}_container ${IMAGE_NAME}:${IMAGE_TAG} || true
                    sleep 5
                    docker ps
                    """
                }
            }
        }

        stage('Clean Up') {
            steps {
                script {
                    echo 'Cleaning up temporary containers...'
                    sh """
                    docker stop ${IMAGE_NAME}_container || true
                    docker rm ${IMAGE_NAME}_container || true
                    """
                }
            }
        }

        // ───────────────────────────────────────────────
        // OPTIONAL STAGES (disabled for now)
        // ───────────────────────────────────────────────

        // // SonarQube Analysis (Uncomment later when SonarQube is configured)
        // stage('SonarQube Analysis') {
        //     steps {
        //         withCredentials([string(credentialsId: 'sonarqube-token', variable: 'SONAR_TOKEN')]) {
        //             withSonarQubeEnv('SonarQubeServerName') {
        //                 sh """
        //                     sonar-scanner \
        //                     -Dsonar.projectKey=LLMOPS \
        //                     -Dsonar.sources=. \
        //                     -Dsonar.host.url=http://sonarqube-dind:9000 \
        //                     -Dsonar.login=${SONAR_TOKEN}
        //                 """
        //             }
        //         }
        //     }
        // }

        // // AWS ECR Build and Push (Enable when AWS credentials are added)
        // stage('Build and Push Docker Image to ECR') {
        //     steps {
        //         withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-token']]) {
        //             script {
        //                 def accountId = sh(script: "aws sts get-caller-identity --query Account --output text", returnStdout: true).trim()
        //                 def ecrUrl = "${accountId}.dkr.ecr.${env.AWS_REGION}.amazonaws.com/${env.ECR_REPO}"

        //                 sh """
        //                     aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ecrUrl}
        //                     docker build -t ${env.ECR_REPO}:${IMAGE_TAG} .
        //                     docker tag ${env.ECR_REPO}:${IMAGE_TAG} ${ecrUrl}:${IMAGE_TAG}
        //                     docker push ${ecrUrl}:${IMAGE_TAG}
        //                 """
        //             }
        //         }
        //     }
        // }

        // // ECS Deployment (Enable later)
        // stage('Deploy to ECS Fargate') {
        //     steps {
        //         withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-token']]) {
        //             script {
        //                 sh """
        //                     aws ecs update-service \
        //                         --cluster multi-ai-agent-cluster \
        //                         --service multi-ai-agent-def-service-shqlo39p \
        //                         --force-new-deployment \
        //                         --region ${AWS_REGION}
        //                 """
        //             }
        //         }
        //     }
        // }
    }

    post {
        always {
            echo 'Pipeline completed.'
        }
        failure {
            echo 'Pipeline failed. Check logs for errors.'
        }
        success {
            echo 'Pipeline executed successfully!'
        }
    }
}
