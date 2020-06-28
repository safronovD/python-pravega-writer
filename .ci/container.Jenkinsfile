
pipeline {
     agent {
        kubernetes {
            label 'jenkins-pod'
            yamlFile '.ci/pod-templates/pod-python.yaml'
        }
     }
     parameters {
        string(name: 'BUILD_NUMBER', defaultValue: '123')
     }

    options {
        timestamps()
        buildDiscarder(logRotator(numToKeepStr: '20', artifactNumToKeepStr: '20'))
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
//                         sh 'printenv'
//                         sh 'docker ps'
                      }
            }

       }
       stage('Test') {
            steps {
                      container('docker'){
                         sh 'python3 -m robot.run  --outputdir reports --variable tag:${params.BUILD_NUMBER}-${GIT_COMMIT} ./server/test/container_test.robot'
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
            script{
//                echo currentBuild.result
                def externalMethod
                externalMethod = load(".ci/publish_result.groovy")
                externalMethod.setBuildStatus("Container test", currentBuild.result);
            }

          }

	}
}