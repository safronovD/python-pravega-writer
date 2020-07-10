pipeline {
    agent {
        kubernetes {
            label 'jenkins-pod-kubectl'
            yamlFile '.ci/pod-templates/python-kubectl-helm-pod.yaml'
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
                       echo Stress tests
                       mkdir -p reports
                       python3 -m pip install -r ./stress-test/requirements.txt
                    '''
                }
            }
       }
       stage('Stress test') {
            steps {
                container('common') {
                    script {
                        //sh 'python3 ./stress-test/setup_stress.py st-${GIT_COMMIT}'
                        sh 'bzt ./stress-test/stress-test.yml'
                    }
                  }
             }
        }
   }
    post {
        always {
            script {
                //perfReport 'reports/result_stats.csv'

                def publish_result = load(".ci/publish_result.groovy")
                publish_result.setBuildStatus("Stress tests", currentBuild.result);
            }
        }
	}
}