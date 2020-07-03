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
                    '''
                    //python3 -m pip install -r ./stress-test/requirements.txt
                }
            }
       }
       stage('Stress test') {
            steps {
                container('common') {
                    script {
                        sh 'helm list'
                        //helm install --namespace test test-${GIT_COMMIT} ./ppw-chart --set fullnameOverride=test-${GIT_COMMIT}
                        //helm delete --namespace test test-${GIT_COMMIT}
                        def node_ip
                        def node_port
                        //sh 'export NODE_IP=$(kubectl get nodes -o jsonpath="{.items[0].status.addresses[0].address}")' > node_ip
                        //echo "&{kubectl get nodes -o jsonpath='{.items[0].status.addresses[0].address}'}" > node_ip
                        echo "5" > node_ip
                        echo "${node_ip}"
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