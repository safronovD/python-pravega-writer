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
        GH_TOKEN = credentials('github-jenkins-token')
        PYTHONPATH = "${WORKSPACE}"
    }
    stages {
        stage ('Pushing') {
            steps {
//                container('node') {
//                    sh 'npm install -g semantic-release @semantic-release/changelog @semantic-release/commit-analyzer @semantic-release/exec @semantic-release/git @semantic-release/release-notes-generator'
//                    sh 'semantic-release'
//                }
                container('docker') {
                    sh 'echo $VERSION'
//                    sh "echo ${params.VERSION}"
//                    sh 'echo $DOCKER_REGISTRY'
//                    sh 'docker login docker.pkg.github.com -u REGIORGIO -p $DOCKER_REGISTRY'
                    sh 'echo docker test'
                    sh 'docker images'
                    sh 'docker -v'
                    sh 'python3 -m pip install -r ./test/container_test/image_setup/requirements.txt'
                    sh 'python3 ./test/container_test/image_setup/container_setup.py REGIORGIO ff840c5fe3307a9249df27b8f7e3535da7e4e6a0 $VERSION docker.pkg.github.com/safronovd/python-pravega-writer'
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