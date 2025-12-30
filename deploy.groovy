def deploy(String environment) {
    sshagent(['jenkins-user']) {
        withCredentials([string(credentialsId: environment, variable: 'IP_ADDR')]) {
            sh """
                ssh -o StrictHostKeyChecking=no jenkins@\${IP_ADDR} << 'EOF'

                    if [ ${env.frontend_built} = true ]; then
                        docker compose pull frontend
                    fi

                    if [ ${env.backend_built} = true ]; then
                        docker compose pull backend
                    fi

                    if [ ${env.database_built} = true ]; then
                        docker compose pull database
                    fi
                    
                    docker compose up -d
EOF
            """
        }
    }
}

return this