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
                    sh 'pip3 install pylint'
                    sh 'pip3 install pycodestyle'
                    sh 'pip3 install -r ./connector/requirements.txt'
                    sh 'pip3 install -r ./server/requirements.txt'
                    sh 'pip3 install -r ./ml-controller/requirements.txt'
                    sh 'pip3 install -r ./connector/test/requirements.txt'
                    sh 'pip3 install -r ./server/test/requirements.txt'
                    sh 'pip3 install -r ./ml-controller/test/requirements.txt'
                    sh 'mkdir -p reports'
                    sh 'mkdir -p reports/connector'
                    sh 'mkdir -p reports/server'
                    sh 'mkdir -p reports/ml-controller'
                }
            }
        }

        stage('Lint') {
            steps {
                container('python') {
                    sh 'pylint --rcfile=pylint.cfg --exit-zero server/ connector/ ml-controller/ --msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}" > reports/pylint.log'
                    sh 'pycodestyle --max-line-length=100 ./ml-controller ./server ./connector > reports/pep8.log | exit 0'

                    recordIssues(
                        tool: pyLint(pattern: 'reports/pylint.log'),
                        unstableTotalAll: 25
                    )
                    recordIssues(
                        tool: pep8(pattern: 'reports/pep8.log'),
                        unstableTotalAll: 25
                    )
                }
            }
        }
       
        stage('connector unit') {
            steps {
                container('python'){
                    sh 'python3 -m robot.run  --outputdir reports/connector ./connector/test/unit.robot'
                    step(
                        [
                            $class              : 'RobotPublisher',
                            outputPath          : 'reports/connector',
                            outputFileName      : 'output.xml',
                            reportFileName      : 'report.html',
                            logFileName         : 'log.html',
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
                    sh 'python3 -m robot.run  --outputdir reports/ml-controller ./ml-controller/test/unit.robot'
                    step(
                        [
                            $class              : 'RobotPublisher',
                            outputPath          : 'reports/ml-controller',
                            outputFileName      : 'output.xml',
                            reportFileName      : 'report.html',
                            logFileName         : 'log.html',
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
                    sh 'python3 -m robot.run  --outputdir reports/server ./server/test/unit.robot'
                    step(
                        [
                            $class              : 'RobotPublisher',
                            outputPath          : 'reports/server',
                            outputFileName      : 'output.xml',
                            reportFileName      : 'report.html',
                            logFileName         : 'log.html',
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
        success {
            setBuildStatus("Unit & Lint succeeded", "Unit & Lint", "SUCCESS");
        }
        failure {
            setBuildStatus("Unit & Lint failed", "Unit & Lint", "FAILURE");
        }
    }
}