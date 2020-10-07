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
        DOCKER_REGISTRY = credentials('github-jenkins-token')
        PYTHONPATH = "${WORKSPACE}"
    }
    stages {
        stage ('Preparation') {
            steps {
                container('docker') {
                    sh 'echo $DOCKER_REGISTRY'
                    sh 'docker login docker.pkg.github.com -u REGIORGIO -p $DOCKER_REGISTRY'
//                    sh 'echo docker test'
//                    sh 'python3 -m pip install -r ./test/container_test/image_setup/requirements.txt'
//                    sh 'python3 ./test/container_test/image_setup/push_images.py $DOCKER_REGISTRY_USR $DOCKER_REGISTRY_PSW'
                }
            }
       }

   }

//    post {
//        always {
//            script {
//
//                def publish_result = load(".ci/publish_result.groovy")
//                publish_result.setBuildStatus("release", currentBuild.result);
//            }
//
//        }
//	}
}