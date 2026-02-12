pipeline {
    agent any

    tools {
        nodejs 'nodeJs_23'
    }

    environment {
        IMAGE_NAME = 'devosp_showcase_stock_service'
        IMAGE_TAG = "${env.BUILD_ID}"
        DOCKER_IMAGE = "${IMAGE_NAME}:${IMAGE_TAG}"
        GIT_REPO_URL = 'https://github.com/genocem/devops_showcase_stock_service.git'
        GIT_BRANCH = 'main'

        // SCANNER_HOME = tool 'SonarScanner'
        TRIVY_REPORT_IMAGE = 'trivy_report_image.json'

        // azure container registry
        // ACR_NAME = 'stageMicroservices'
        // ACR_REPO = "${ACR_NAME}.azurecr.io/${IMAGE_NAME}"
        // ACR_CREDENTIALS_ID = 'ACR_CREDENTIALS_ID'
    }

    stages {
        stage('Clean Workspace') {
            steps {
                cleanWs()
            }
        }

        stage('Checkout Code') {
            steps {
                git branch: "${GIT_BRANCH}", url: "${GIT_REPO_URL}"
            }
        }

        // stage("Sonarqube Analysis") {

        //     steps {
        //         withSonarQubeEnv('sonar-server') {
        //             sh '''
        //             ${SCANNER_HOME}/bin/sonar-scanner -Dsonar.projectName=commercial \
        //             -Dsonar.projectKey=commercial
        //             '''
        //         }
        //     }
        // }

        stage('Build Docker Image') {
            steps {
                script {
                    sh "docker build -t ${DOCKER_IMAGE} ."
                }
            }
        }

        stage('image Scan') {
            steps {
                sh '''
                    trivy image --severity HIGH,CRITICAL --report summary --output ${TRIVY_REPORT_IMAGE} --no-progress ${DOCKER_IMAGE}
                '''
            }
            }

// this part will be commented untill i finish testing the previous parts
        // stage('Push to Azure Container Registry') {
        //     steps {
        //         withCredentials([usernamePassword(credentialsId: "${ACR_CREDENTIALS_ID}", usernameVariable: 'AZURE_USERNAME', passwordVariable: 'AZURE_PASSWORD')]) {
        //             script {
        //                 sh "echo ${AZURE_PASSWORD} | docker login ${ACR_NAME}.azurecr.io -u ${AZURE_USERNAME} --password-stdin"
        //                 sh "docker tag ${DOCKER_IMAGE} ${ACR_REPO}:${IMAGE_TAG}"
        //                 sh "docker push ${ACR_REPO}:${IMAGE_TAG}"
        //                 sh "docker tag ${DOCKER_IMAGE} ${ACR_REPO}:latest"
        //                 sh "docker push ${ACR_REPO}:latest"
        //             }
        //         }
        //     }
        //         }
    }

    post {
        always {
            archiveArtifacts artifacts: "${TRIVY_REPORT_IMAGE}", allowEmptyArchive: true
        }
        success {
            echo 'Pipeline succeeded!'
        }

        failure {
            echo 'Pipeline failed!'
        }
    }
}