void setBuildStatus(String message, String state) {
  step([
      $class: "GitHubCommitStatusSetter",
      reposSource: [$class: "ManuallyEnteredRepositorySource", url: "https://github.com/safronovD/python-pravega-writer"],
      contextSource: [$class: "ManuallyEnteredCommitContextSource", context: "Robot tests"],
      errorHandlers: [[$class: "ChangingBuildStatusErrorHandler", result: "UNSTABLE"]],
      statusResultSource: [ $class: "ConditionalStatusResultSource", results: [[$class: "AnyBuildResult", message: message, state: state]] ]
  ]);
}
pipeline {
   agent any

   stages {
       stage('Preparation') {
            steps {
                sh 'pip install -r Connector/requirements.txt'
                sh 'pip install -r Server/requirements.txt'
                sh 'pip install -r Tests/requirements.txt'
            }
        }
    
       stage('Run Robot Tests') {
         steps {
               sh 'mkdir -p results'
               sh 'python3 -m coverage run -m robot.run  --outputdir results  .'
               sh 'python3 -m coverage xml'
               }
        }
    }
    post {
          always {
            script {
              step(
                  [
                    $class              : 'RobotPublisher',
                    outputPath          : 'results',
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
            setBuildStatus("Build succeeded", "SUCCESS");
          }
          failure {
            setBuildStatus("Build failed", "FAILURE");
          }
         
	}
}
