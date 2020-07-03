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
   stages {
       stage('Preparation') {
            steps {
                container('common') {
                    sh '''
                       echo Stress tests
                       python3 -m pip install -r ./stress-test/requirements.txt
                    '''
                }
            }
       }
       stage('Stress test') {
            steps {
                container('common') {
                    script {
                        //sh "helm install --namespace test test-${GIT_COMMIT} ./ppw-chart --set fullnameOverride=test-${GIT_COMMIT}"
                        //sh "helm delete --namespace test test-${GIT_COMMIT}"
                        //def node_ip = sh(script: 'kubectl get nodes -o jsonpath={.items[0].status.addresses[0].address}', returnStdout: true)
                        //echo "${node_ip}"
                        //sh "locust -f ./stress-test/setup.py --host=http://192.168.70.211:30798 --headless -u 1000 -r 100 --run-time 15s"
                        bzt ./stress-test/stress-test.yml
                    }
                  }
             }
        }
   }
    post {
        always {
            script {
                def publish_result = load(".ci/publish_result.groovy")
                publish_result.setBuildStatus("Stress tests", currentBuild.result);
            }
        }
	}
}