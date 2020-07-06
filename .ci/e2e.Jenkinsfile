pipeline {
    agent {
        kubernetes {
            label 'jenkins-pod-python'
            yamlFile '.ci/pod-templates/python-kubectl-helm-pod.yaml'
        }
    }
    options {
         timestamps()
         buildDiscarder(logRotator(numToKeepStr: '20', artifactNumToKeepStr: '20'))

    }
   stages {
       stage('Preparation') {
            steps {
                container('common') {
                    sh '''
                       echo End-to-end tests
                       export PYTHONPATH=${WORKSPACE}
                       mkdir -p reports
                       python3 -m pip install -r ./e2e/requirements.txt
                    '''
                }
            }
       }
       stage('End-to-End test') {
            steps {
                container('common') {
                    //sh 'python3 -m robot.run --outputdir reports --variable chartId:test-${GIT_COMMIT} ./e2e/e2e.robot'
                    sh 'python3 ./e2e/setup_helm.py'
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
