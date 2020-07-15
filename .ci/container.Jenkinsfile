pipeline {
    agent {
        kubernetes {
            label 'container-pod'
            yamlFile '.ci/pod-templates/pod-python-docker-kubectl-helm.yaml'
        }
     }

    options {
        timestamps()
        buildDiscarder(logRotator(numToKeepStr: '20', artifactNumToKeepStr: '20'))
    }

    environment {
        DOCKER_REGISTRY = credentials('Jenkins-docker-registry')
        PYTHONPATH = "${WORKSPACE}"
    }
    stages {
        stage ('Preparation') {
            steps {
                container('kube') {
                    sh 'mkdir -p reports'
                    sh 'python3 -m pip install -r ./server/test/pod_setup/requirements.txt'
                }

                container('docker') {
                    sh 'python3 -m pip install -r ./server/test/image_setup/requirements.txt'
                    sh 'python3 ./server/test/push_images.py $DOCKER_REGISTRY_USR $DOCKER_REGISTRY_PSW'

                }
            }

       }
       stage('Test') {
            steps {
                container('kube') {
                    script {
                        sh 'python3 -m robot.run  --outputdir reports ./server/test/pod.robot'
//                        sh 'python3 ./server/test/container_setup.py'
                    }
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
                publish_result.setBuildStatus("Container tests", currentBuild.result);
            }

        }
	}
}