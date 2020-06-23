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
            yamlFile 'Jenkinsfiles/jenkinsPodTemplate.yaml'
     }
       }
   // options {
   //      timestamps()
   //      }
   stages {
       stage('Container') {
            steps {
                  sh 'echo Container'
            //     sh 'pip install -r Connector/requirements.txt'
            //     sh 'pip install -r Server/requirements.txt'
            //     sh 'pip install -r Tests/requirements.txt'
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