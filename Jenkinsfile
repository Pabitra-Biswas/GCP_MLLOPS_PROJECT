pipeline{
    agent any

    stages{
        stage('Cloning Github repo to jenkins'){
            steps{
                script{
                    echo 'Cloning the repository...'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/Pabitra-Biswas/GCP_MLLOPS_PROJECT.git']])
                }
            }
        }
    }
}