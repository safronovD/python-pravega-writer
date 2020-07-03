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
                        sh "helm install --namespace test test-${GIT_COMMIT} ./ppw-chart --set fullnameOverride=test-${GIT_COMMIT}"
                        
                        def node_ip = sh(script: 'kubectl get nodes -o jsonpath={.items[0].status.addresses[0].address}', returnStdout: true)
                        def node_port = sh(script: 'kubectl get --namespace test -o jsonpath={.spec.ports[0].nodePort} services test-${GIT_COMMIT}', returnStdout: true)
                        
                        sh "locust -f ./stress-test/setup.py --csv=reports/result --host=http://${node_ip}:${node_port} --headless -u 1000 -r 100 --run-time 15s"
                        
                        sh "helm delete --namespace test test-${GIT_COMMIT}"
                        //sh 'bzt ./stress-test/stress-test.yml'
                    }
                  }
             }
        }
   }
    post {
        always {
            script {
                //perfReport 'result_stats_history.csv'

                def publish_result = load(".ci/publish_result.groovy")
                publish_result.setBuildStatus("Stress tests", currentBuild.result);
            }
        }
	}
}