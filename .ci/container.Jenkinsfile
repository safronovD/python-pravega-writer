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
            yamlFile '.ci/pod-templates/pod-python.yaml'
        }
     }
   // options {
   //      timestamps()
   //      }
   stages {
       stage('Container') {
            steps {
                  container('docker'){
                      container('python'){
                      sh 'echo Container'
                      //sh 'mkdir -p reports'
                      //sh 'python3 -m pip install -r ./server/requirements.txt'
                      //sh 'python3 -m robot.run  --outputdir reports ./server/test/container_test.robot'
                      sh 'docker --version'
                      }

                  }
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