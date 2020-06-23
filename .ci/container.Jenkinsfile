void setBuildStatus(String context, String message, String state) {
  step([
      $class: "GitHubCommitStatusSetter",
      reposSource: [$class: "ManuallyEnteredRepositorySource", url: "https://github.com/safronovD/python-pravega-writer"],
      contextSource: [$class: "ManuallyEnteredCommitContextSource", context: context],
      errorHandlers: [[$class: "ChangingBuildStatusErrorHandler", result: "UNSTABLE"]],
      statusResultSource: [ $class: "ConditionalStatusResultSource", results: [[$class: "AnyBuildResult", message: message, state: state]] ]
  ]);
}
pipeline {
     agent {
        kubernetes {
            label 'jenkins-pod'
            yamlFile '.ci//pod-templates/pod-python.yaml'
        }
     }
   // options {
   //      timestamps()
   //      }
   stages {
       stage('Container') {
            steps {
                  sh 'echo Container'
                  sh 'python --version'
                  sh 'python3 --version'
                  sh 'mkdir -p reports'
                  sh 'python3 -m pip install -r ./server/requirements.txt'
                  sh 'python3 -m robot.run  --outputdir reports ./server/test/container_test.robot'

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
        }

      }

    post {
          success {
            setBuildStatus("Container succeeded", "Container", "SUCCESS");
          }
          failure {
            setBuildStatus("Container failed", "Container", "FAILURE");
          }

	}
}