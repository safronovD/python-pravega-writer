pipeline {
    agent {
        kubernetes {
            label 'integration-pod'
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
                container('python') {
                    sh 'echo kube test'
                    sh 'mkdir -p reports'
//                    sh 'python3 -m pip install -r ./test/container_test/pod_setup/requirements.txt'
                    sh 'python3 -m pip install robotframework'
                }

//                container('docker') {
//                    sh 'echo docker test'
//                    sh 'python3 -m pip install -r ./test/container_test/image_setup/requirements.txt'
//                    sh 'python3 ./test/container_test/image_setup/push_images.py $DOCKER_REGISTRY_USR $DOCKER_REGISTRY_PSW'
//                }
            }
       }
       stage('Test') {
            steps {
                container('python') {
                    script{
//                         sh 'python3 -m robot.run  --outputdir reports ./test/container_test/pod.robot'
                           sh 'python3 -m robot.run  --outputdir reports ./test/empty_tests.robot'
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

//                def publish_result = load(".ci/publish_result.groovy")
//                publish_result.setBuildStatus("Container tests", currentBuild.result);
            }

        }
	}
}