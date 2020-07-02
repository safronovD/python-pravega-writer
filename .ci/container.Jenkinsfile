pipeline {
    agent {
        kubernetes {
            label 'container-pod'
            yamlFile '.ci/pod-templates/pod-python.yaml'
        }
     }

    options {
        timestamps()
        buildDiscarder(logRotator(numToKeepStr: '20', artifactNumToKeepStr: '20'))
    }

    environment {
        DOCKER_REGISTRY = credentials('Jenkins-docker-registry')
    }
    stages {
        stage ('Preparation') {
            steps {
                container('docker') {
//                    sh 'python3 --version'
//                    sh 'docker --version'
//                    sh 'mkdir -p reports'
//                    sh 'python3 -m pip install -r ./server/test/requirements.txt'
//                    sh 'printenv'
//                    sh 'python3 ./server/test/setup.py'
//                    sh 'docker ps'
                }
            }

       }
       stage('Test') {
            steps {
                container('docker') {
                    script{
                          echo '$DOCKER_REGISTRY_USR'
//                        sh 'python3 -m robot.run  --outputdir reports --variable tag:${GIT_COMMIT} ./server/test/container_test.robot'
                    }
                }
            }
        }

   }

    post {
        always {
            script {
//                def parse_robot_results = load(".ci/parse_robot_results.groovy")
//                parse_robot_results.parseRobotResults('reports')

                def publish_result = load(".ci/publish_result.groovy")
                publish_result.setBuildStatus("Container tests", currentBuild.result);
            }

        }

	}
}