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
                        if (run.status != 'completed') {
                            currentBuild.result = 'ABORTED'
                            error("Latest GitHub Actions run hasn't completed. Jenkins will retry on next poll.")
                        }
                        
                        if (run.conclusion != 'success') {
                            currentBuild.result = 'ABORTED'
                            error("Latest GitHub Actions wasn't successful. Jenkins will retry on next poll.")
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
                        
                        // get build and push job
                        def targetJob = jobsJson.jobs.find { it.name == 'build-and-push' }

                        if (!targetJob) {
                            error("GitHub Actions job not found: '${targetJob.name}'")
                        }
                        
                        // check that target job in GitHub Actions was successful, thereby triggering rest of jenkins pipeline
                        if (targetJob.conclusion != 'success') {
                            error("GitHub Actions job '${targetJob.name}' failed with: ${targetJob.conclusion}")
                        }
                        
                        echo "All checks have passed. Jenkins pipeline will now continue."
                    }
                }
            }
        }

        stage('Deploy') {
            echo "deployments will happen here"
        }

    }
        
    post {
        always {
            cleanWs()
        }
    }
}