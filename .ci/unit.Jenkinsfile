void setBuildStatus(String context, String message, String state) {
  step([
      $class: "GitHubCommitStatusSetter",
      reposSource: [$class: "ManuallyEnteredRepositorySource", url: "https://github.com/safronovD/python-pravega-writer"],
      contextSource: [$class: "ManuallyEnteredCommitContextSource", context: context],
      errorHandlers: [[$class: "ChangingBuildStatusErrorHandler", result: "UNSTABLE"]],
      statusResultSource: [ $class: "ConditionalStatusResultSource", results: [[$class: "AnyBuildResult", message: message, state: state]] ]
  ]);
}

pipeline {
    agent {
        kubernetes {
            label 'jenkins-pod'
            yamlFile '.ci/pod-templates/pod-python.yaml'
        }
    }

    stages {
        stage('Preparation') {
            steps {
                container('python'){
                    sh 'pip install pylint'
                    sh 'pip install pycodestyle'
                    sh 'pip install -r ./connector/test/requirements.txt'
                    sh 'pip install -r ./server/test/requirements.txt'
                    sh 'pip install -r ./ml-controller/test/requirements.txt'
                }
            }
        }

        stage('Lint') {
            steps {
                container('python') {
                    sh 'pylint --rcfile=pylint.cfg --exit-zero server/ connector/ ml-controller/ > reports/pylint.log'
                    sh 'pycodestyle ./ml-controller ./server ./connector > reports/pep8.log'
                }
            }
        }
       
        stage('connector unit') {
            steps {
                container('python'){
                    sh 'python3 -m robot.run  --outputdir reports ./connector/test/unit.robot'
                    step(
                        [
                            $class              : 'RobotPublisher',
                            outputPath          : 'reports',
                            outputFileName      : 'connector_output.xml',
                            reportFileName      : 'connector_report.html',
                            logFileName         : 'connector_log.html',
                            disableArchiveOutput: false,
                            passThreshold       : 60,
                            unstableThreshold   : 40,
                            otherFiles          : "**/*.png,**/*.jpg",
                        ]
                    )
                }
            }
        }

        stage('ml-controller unit') {
            steps {
                container('python'){
                    sh 'python3 -m robot.run  --outputdir reports ./ml-controller/test/unit.robot'
                    step(
                        [
                            $class              : 'RobotPublisher',
                            outputPath          : 'reports',
                            outputFileName      : 'ml-controller_output.xml',
                            reportFileName      : 'ml-controller_report.html',
                            logFileName         : 'ml-controller_log.html',
                            disableArchiveOutput: false,
                            passThreshold       : 60,
                            unstableThreshold   : 40,
                            otherFiles          : "**/*.png,**/*.jpg",
                        ]
                    )
                }
            }
        }

        stage('server unit') {
            steps {
                container('python'){
                    sh 'python3 -m robot.run  --outputdir reports ./server/test/unit.robot'
                    step(
                        [
                            $class              : 'RobotPublisher',
                            outputPath          : 'reports',
                            outputFileName      : 'server_output.xml',
                            reportFileName      : 'server_report.html',
                            logFileName         : 'server_log.html',
                            disableArchiveOutput: false,
                            passThreshold       : 60,
                            unstableThreshold   : 40,
                            otherFiles          : "**/*.png,**/*.jpg",
                        ]
                    )
                }
            }
        }
    }

    post {
        always{
            recordIssues(
                tool: pep8(pattern: 'reports/pylint.log'),
                unstableTotalAll: 150,
                failedTotalAll: 200
            )
            recordIssues(
                tool: pyLint(pattern: 'reports/pep8.log'),
                unstableTotalAll: 20,
                failedTotalAll: 30
            )
        }

        success {
            setBuildStatus("Unit & Lint succeeded", "Unit & Lint", "SUCCESS");
        }
        failure {
            setBuildStatus("Unit & Lint failed", "Unit & Lint", "FAILURE");
        }
    }
}