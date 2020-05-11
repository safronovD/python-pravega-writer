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
       stage('Preparation') {
            steps {
                container('python') {
                    sh 'echo End-to-end tests'
                    sh 'python --version'
                    // sh 'pip install -r Connector/requirements.txt'
                    // sh 'pip install -r Server/requirements.txt'
                    // sh 'pip install -r Tests/requirements.txt'
                }
            }
       }
   }
    post {
          success {
            setBuildStatus("Tests succeeded", "Tests", "SUCCESS");
          }
          failure {
            setBuildStatus("Tests failed", "Tests", "FAILURE");
          }
         
	}
}
