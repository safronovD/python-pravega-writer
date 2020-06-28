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
                       python --version
                       python3 -m pip install -r ./e2e/requirements.txt
                    '''
                }
            }
       }
       stage('End-to-End test') {
            steps {
                container('common') {
                    //script {
                    //    def commit_id = sh(returnStdout: true, script: 'git rev-parse HEAD')
                    //    def chart_id = commit_id[1..10] + "-${currentBuild.number}"
                    //}
                    sh 'python3 -m robot.run --outputdir reports/e2e --variable chartId:test3 ./e2e/e2e.robot'
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
                publish_result.setBuildStatus("Container test", currentBuild.result);
            }
        }
	}
}