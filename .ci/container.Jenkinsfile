
pipeline {
     agent {
        kubernetes {
            label 'jenkins-pod'
            yamlFile '.ci/pod-templates/pod-python.yaml'
        }
     }

    options {
        timestamps()
    }
   stages {
       stage ('Preparation'){
             steps {
                      container('docker'){

                         sh 'python3 --version'
                         sh 'docker --version'
                         sh 'mkdir -p reports'

                         sh 'python3 -m pip install -r ./server/test/requirements.txt'
//                         sh 'python3 ./server/test/setup.py'
                      }
            }

       }
       stage('Test') {
            steps {
                      container('docker'){
                         sh 'python3 -m robot.run  --outputdir reports --variable tag:${BUILD_NUMBER}-${GIT_COMMIT} ./server/test/container_test.robot'
                      }
            }
        }

   }

    post {
          always {
            script {
              step(
                  [
                    $class              : 'RobotPublisher',
                    outputPath          : 'reports',
                    outputFileName      : 'output.xml',
                    reportFileName      : 'report.html',
                    logFileName         : 'log.html',
                    disableArchiveOutput: false,
                    passThreshold       : 60,
                    unstableThreshold   : 40,
                    otherFiles          : "**/*.png,**/*.jpg",
                  ]
                )
            }
            externalMethod = load("publish_result.groovy")
          }

          success {
            externalMethod.setBuildStatus("Container succeeded", "Container", "SUCCESS");
          }
          failure {
            externalMethod.setBuildStatus("Container failed", "Container", "FAILURE");
          }

	}
}