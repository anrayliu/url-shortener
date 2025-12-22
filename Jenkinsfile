pipeline {
    agent any
    
    triggers {
        pollSCM('H/5 * * * *')
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo '🔍 Checking out code from GitHub...'
                checkout scm
            }
        }
        
        stage('Detect Changes') {
            steps {
                script {
                    echo '📋 Recent commits:'
                    sh 'git log --oneline -5'
                    
                    if (fileExists('.github/workflows')) {
                        echo '✅ GitHub Actions workflows detected'
                        dir('.github/workflows') {
                            sh 'ls -la'
                        }
                    }
                }
            }
        }
        
    }
    
    post {
        always {
            echo '🏁 Pipeline completed'
            cleanWs()
        }
    }
}