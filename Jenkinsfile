pipeline {
    agent any
    
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
                        // First, get the latest workflow run
                        def workflowResponse = sh(
                            script: """
                                curl -s -H "Authorization: token \${GITHUB_TOKEN}" \
                                "https://api.github.com/repos/anrayliu/url-shortener/actions/workflows/cicd.yml/runs?per_page=1"
                            """,
                            returnStdout: true
                        )
                        
                        def workflowJson = readJSON text: workflowResponse
                        def runId = workflowJson.workflow_runs[0].id
                        
                        // Now get jobs for that run
                        def jobsResponse = sh(
                            script: """
                                curl -s -H "Authorization: token \${GITHUB_TOKEN}" \
                                "https://api.github.com/repos/anrayliu/url-shortener/actions/runs/${runId}/jobs"
                            """,
                            returnStdout: true
                        )
                        
                        def jobsJson = readJSON text: jobsResponse
                        
                        // Find specific job by name
                        def targetJob = jobsJson.jobs.find { it.name == 'build-and-push' }
                        
                        if (!targetJob) {
                            error("Job 'your-job-name' not found in GitHub Actions run")
                        }
                        
                        if (targetJob.conclusion != 'success') {
                            error("GitHub Actions job '${targetJob.name}' failed with: ${targetJob.conclusion}")
                        }
                        
                        echo "GitHub Actions job '${targetJob.name}' passed"
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