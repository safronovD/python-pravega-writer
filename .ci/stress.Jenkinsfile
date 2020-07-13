pipeline {
    agent {
        kubernetes {
            label 'jenkins-pod-kubectl'
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
                       echo Stress tests
                       mkdir -p reports
                       python3 -m pip install -r ./stress-test/requirements.txt
                    '''
                    //curl https://gettaurus.org/builds/bzt-1.14.2.13904-py2.py3-none-any.whl -o bzt-1.14.2.13904-py2.py3-none-any.whl
                }
            }
        }
        stage('Stress test') {
            steps {
                container('common') {
                    script {
                        sh 'python3 ./stress-test/setup_stress.py st-${GIT_COMMIT}'
                        //sh 'bzt ./stress-test/stress-test.yml -report'
                    }
                  }
             }
        }
    }
    post {
        always {
            script {
                //perfReport 'result.xml'

                def publish_result = load(".ci/publish_result.groovy")
                publish_result.setBuildStatus("Stress tests", currentBuild.result);
            }
        }
	}
}