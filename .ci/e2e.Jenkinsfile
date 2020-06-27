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
            label 'jenkins-pod-python'
            yamlFile '.ci/pod-templates/python-kubectl-helm-pod.yaml'
        }
    }
   // options {
   //      timestamps()
   //      }
   stages {
       stage('Preparation') {
            steps {
                container('common') {
                    sh '''
                       echo End-to-end tests
                       python --version
                       python3 -m pip install -r ./e2e/requirements.txt
                    '''
                }
            }
       }
       stage('End-to-End test') {
            steps {
                container('common') {
                    //script {
                    //    def commit_id = sh(returnStdout: true, script: 'git rev-parse HEAD')
                    //    def chart_id = commit_id[1..10] + "-${currentBuild.number}"
                    //}
                    sh 'python3 -m robot.run --outputdir reports --variable chartId:test3 ./e2e/e2e.robot'
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
          }  

          success {
            setBuildStatus("Tests succeeded", "Tests", "SUCCESS");
          }
          failure {
            setBuildStatus("Tests failed", "Tests", "FAILURE");
          }
         
	}
}