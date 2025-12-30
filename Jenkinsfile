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
                        // repeat until github actions run is complete
                        waitUntil {
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

                            echo "Latest GitHub Actions run: ${run.status}, ${run.conclusion}"

                            // check that latest run is completed
                            if (run.status != 'completed') {
                                echo 'Latest run not completed yet'
                                sleep(time: 1, unit: 'MINUTES')
                                return false
                            }

                            if (run.conclusion != 'success') {
                                error('Last run not successful.')
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

                            for (component in ['frontend', 'backend', 'database']) {
                                if (env."${component}_built" == true) {
                                    continue
                                }

                                def jobName = "build-and-push-${component}"

                                // Find the specific job in the JSON payload
                                // adds build-and-push if job was ran, otherwise only contains jobName
                                def targetJob = jobsJson.jobs.find { it.name == "${jobName} / build-and-push" || it.name == "${jobName}" }

                                if (!targetJob) {
                                    error("GitHub Actions job not found: ${jobName}")
                                }

                                // Check for success and set a dynamic environment variable
                                if (targetJob.conclusion == 'success') {
                                    echo "Successfully verified ${jobName}"
                                    env."${component}_built" = true
                                    continue
                                }

                                echo "GitHub Actions job '${jobName}' failed with status: ${targetJob.conclusion}"
                            }

                            echo "Frontend status: ${env.frontend_built}"
                            echo "Backend status: ${env.backend_built}"
                            echo "Database status: ${env.database_built}"

                            return true
                        }
                    }
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    // parameters evaluated as strings

                    def externalScript = load "deploy.groovy"

                    echo "Branch: ${env.GIT_BRANCH}"

                    if (env.frontend_built.toBoolean() || env.backend_built.toBoolean() || env.database_built.toBoolean()) {
                        externalScript.deploy("dev-ip-addr")

                        if (env.BRANCH_NAME == "origin/feat-deploy-prod") {
                            externalScript.deploy("prod-ip-addr")
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
