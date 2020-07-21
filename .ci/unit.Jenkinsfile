pipeline {
    agent {
        kubernetes {
            label 'jenkins-pod'
            yamlFile '.ci/pod-templates/pod-python.yaml'
        }
    }
    options {
         buildDiscarder(logRotator(numToKeepStr: '20', artifactNumToKeepStr: '20'))
         timestamps()
    }
    environment {
        PYTHONPATH = "${WORKSPACE}"
    }
    stages {
        stage('Preparation') {
            steps {
                container('python'){
                    sh 'pip3 install pylint'
                    sh 'pip3 install pycodestyle'
                    sh 'pip3 install -r ./src/connector/requirements.txt'
                    sh 'pip3 install -r ./src/server/requirements.txt'
                    sh 'pip3 install -r ./src/ml-controller/requirements.txt'
                    sh 'pip3 install -r ./src/connector/test/requirements.txt'
                    sh 'pip3 install -r ./src/server/test/requirements.txt'
                    sh 'pip3 install -r ./src/ml-controller/test/requirements.txt'
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
                    sh 'pycodestyle --max-line-length=100 ./src/ml-controller ./src/server ./src/connector > reports/pep8.log | exit 0'

                    recordIssues(
                        tool: pyLint(pattern: 'reports/pylint.log'),
                        unstableTotalAll: 125
                    )
                    recordIssues(
                        tool: pep8(pattern: 'reports/pep8.log'),
                        unstableTotalAll: 125
                    )
                }
            }
        }

        stage('connector unit') {
            steps {
                container('python'){
                    sh 'python3 -m robot.run  --outputdir reports/connector ./src/connector/test/unit.robot'
                }
            }
        }

        stage('ml-controller unit') {
            steps {
                container('python'){
                    sh 'python3 -m robot.run  --outputdir reports/ml-controller ./src/ml-controller/test/unit.robot'
                }
            }
        }

        stage('server unit') {
            steps {
                container('python'){
                    sh 'python3 -m robot.run  --outputdir reports/server ./src/server/test/unit.robot'
                }
            }
        }
    }

    post {
        always {
            script {
                def parse_robot_results = load(".ci/parse_robot_results.groovy")

                parse_robot_results.parseRobotResults('reports/connector')
                parse_robot_results.parseRobotResults('reports/ml-controller')
                parse_robot_results.parseRobotResults('reports/server')

                def publish_result = load(".ci/publish_result.groovy")
                publish_result.setBuildStatus("Unit tests", currentBuild.result);
            }
        }
    }
}