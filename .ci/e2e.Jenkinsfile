pipeline {
    agent {
        kubernetes {
            label 'jenkins-pod-python'
            yamlFile '.ci/pod-templates/pod-python-kubectl-helm.yaml'
        }
    }
    options {
        timestamps()
        buildDiscarder(logRotator(numToKeepStr: '20', artifactNumToKeepStr: '20'))

    }
    environment {
        PYTHONPATH = "${WORKSPACE}"
    }

    stages {
        stage('Preparation') {
            steps {
                container('common') {
                    sh '''
                       echo End-to-end tests
                       mkdir -p reports
                       python3 -m pip install -r ./test/e2e/requirements.txt
                    '''
                }
            }
        }
        stage('End-to-End test') {
            steps {
                container('common') {
                    sh 'python3 -m robot.run --outputdir reports --variable tag:${GIT_COMMIT} ./test/e2e/e2e.robot'
                  }
             }
        }
    }
    post {
        always {
            script {
                def parse_robot_results = load(".ci/parse_robot_results.groovy")
                parse_robot_results.parseRobotResults('reports')

                def publish_result = load(".ci/publish_result.groovy")
                publish_result.setBuildStatus("E2E tests", currentBuild.result);
            }
        }
	}
}
