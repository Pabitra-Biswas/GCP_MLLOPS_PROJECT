pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
        GCP_PROJECT = 'my-bigquery-test-466512'
        GCLOUD_PATH = "/var/jenkins/google-cloud-sdk/bin"
    }

    stages {
        stage('Cloning Github repo to Jenkins') {
            steps {
                script {
                    echo 'Cloning the repository...'
                    checkout scmGit(
                        branches: [[name: '*/main']],
                        extensions: [],
                        userRemoteConfigs: [[
                            credentialsId: 'github-token',
                            url: 'https://github.com/Pabitra-Biswas/GCP_MLLOPS_PROJECT.git'
                        ]]
                    )
                }
            }
        }

        stage('Setting up Virtual Environment & Installing Dependencies') {
            steps {
                script {
                    echo 'Setting up Virtual Environment and installing dependencies...'
                    sh '''
                    #!/bin/bash
                    python -m venv $VENV_DIR
                    source $VENV_DIR/bin/activate
                    pip install --upgrade pip
                    pip install -e .
                    '''
                }
            }
        }

        stage('Building Docker Image and Pushing to GCR') {
            steps {
                withCredentials([file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                    script {
                        echo 'Building Docker Image and pushing to GCR...'
                        sh '''
                        #!/bin/bash
                        export PATH=$PATH:${GCLOUD_PATH}
                        gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
                        gcloud config set project ${GCP_PROJECT}
                        gcloud auth configure-docker --quiet
                        docker build -t gcr.io/${GCP_PROJECT}/gcp-mlops-project:latest .
                        docker push gcr.io/${GCP_PROJECT}/gcp-mlops-project:latest
                        '''
                    }
                }
            }
        }
    }
}
