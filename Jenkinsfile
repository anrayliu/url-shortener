pipeline {
    agent any

    triggers {
        pollSCM('H/2 * * * *') 
    }

    parameters {
        booleanParam(name: 'frontend_built', defaultValue: false)
        booleanParam(name: 'backend_built', defaultValue: false)
        booleanParam(name: 'database_built', defaultValue: false)
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'checkout code'
                checkout scm
            }
        }
        
        stage('Check GitHub Actions Job') {
            steps {
                script {
                    withCredentials([string(credentialsId: 'github-pat', variable: 'GITHUB_TOKEN')]) {
                        // get workflow history
                        def workflowResponse = sh(
                            script: """
                                curl -s -H "Authorization: token \${GITHUB_TOKEN}" \
                                "https://api.github.com/repos/anrayliu/url-shortener/actions/workflows/cicd.yaml/runs?per_page=1"
                            """,
                            returnStdout: true
                        )
                        def workflowJson = readJSON text: workflowResponse

                        // get latest run
                        def run = workflowJson.workflow_runs[0]

                        echo "Latest GitHub Actions run: '${run.status}', '${run.conclusion}'"
                        
                        // check that latest run is completed and successful
                        if (run.status != 'completed' || run.conclusion != 'success') {
                            echo "Latest run status: ${run.status}, conclusion: ${run.conclusion}"
                            sleep(time: 1, unit: 'MINUTES')
                            build job: env.JOB_NAME
                            currentBuild.result = 'ABORTED'
                            error("Starting new pipeline.")
                        }
                        
                        // get jobs for latest run
                        def jobsResponse = sh(
                            script: """
                                curl -s -H "Authorization: token \${GITHUB_TOKEN}" \
                                "https://api.github.com/repos/anrayliu/url-shortener/actions/runs/${run.id}/jobs"
                            """,
                            returnStdout: true
                        )
                        def jobsJson = readJSON text: jobsResponse
                        
                        def components = ['frontend', 'backend', 'database']

                        components.each { component ->
                            if (env."${component}_built" == true) {
                                return
                            }

                            def jobName = "build-and-push-${component}"
                            
                            // Find the specific job in the JSON payload
                            // adds build-and-push if job was ran, otherwise only contains jobName
                            def targetJob = jobsJson.jobs.find { it.name == "${jobName} / build-and-push" || it.name == "${jobName}"}

                            if (!targetJob) {
                                error("GitHub Actions job not found: '${jobName}'")
                            }
                            
                            // Check for success and set a dynamic environment variable
                            if (targetJob.conclusion == 'success') {
                                echo "Successfully verified ${jobName}"
                                env."${component}_built" = true
                                return
                            }

                            echo "GitHub Actions job '${jobName}' failed with status: ${targetJob.conclusion}"
                        }

                        echo "Frontend status: ${env.frontend_built}"
                        echo "Backend status: ${env.backend_built}"
                        echo "Database status: ${env.database_built}"
                    }
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    if (env.frontend_built == true || env.backend_built == true || env.database_built) {
                        sshagent(['jenkins-user']) {
                            withCredentials([string(credentialsId: 'dev-ip-addr', variable: 'IP_ADDR')]) {
                                sh """
                                    [ -d ~/.ssh ] || mkdir ~/.ssh && chmod 0700 ~/.ssh
                                    ssh-keyscan -t rsa,dsa example.com >> ~/.ssh/known_hosts  
                                    ssh -o StrictHostKeyChecking=no jenkins@${IP_ADDR} << 'EOF'
                                        docker compose pull
                                        docker compose up
EOF

                                """
                            }
                        }
                    }
                }
            }
        }

    }
        
    post {
        always {
            cleanWs()
        }
    }
}