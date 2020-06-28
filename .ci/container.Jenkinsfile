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
    stages {
        stage ('Preparation') {
            steps {
                container('docker') {
//                    sh 'python3 --version'
//                    sh 'docker --version'
                    sh 'mkdir -p reports'
                    sh 'python3 -m pip install -r ./server/test/requirements.txt'
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
                        sh 'python3 -m robot.run  --outputdir reports --variable tag:${GIT_COMMIT} ./server/test/container_test.robot'
                        }
                }
            }
        }

   }

    post {
        always {
            script {
                def publish_result = load(".ci/parse_robot_results.groovy")
                publish_result.parseRobotResults()

                def publish_result = load(".ci/publish_result.groovy")
                publish_result.setBuildStatus("Container test", currentBuild.result)
            }

        }

	}
}