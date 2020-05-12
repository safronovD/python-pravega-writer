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
   agent any
   // options {
   //      timestamps()
   //      }
   stages {
       stage('Preparation') {
            steps {
                sh 'echo Preparations'

                // sh 'pip install -r Connector/requirements.txt'
                // sh 'pip install -r Server/requirements.txt'
                // sh 'pip install -r Tests/requirements.txt'
            }
        }
    
       stage('Unit tests') {
         steps {
                sh 'echo Unit tests'
                build 'Tests'
               // sh 'mkdir -p results'
               // sh 'python3 -m coverage run -m robot.run  --outputdir results  .'
               // sh 'python3 -m coverage xml'
               }
        }
        stage('Container tests') {
         steps {
                sh 'echo Container tests'
                build 'Container'
               // sh 'mkdir -p results'
               // sh 'python3 -m coverage run -m robot.run  --outputdir results  .'
               // sh 'python3 -m coverage xml'
               }
        }
        stage('Deploy') {
         steps {
                sh 'echo Deploy'
                build 'Deploy'
               // sh 'mkdir -p results'
               // sh 'python3 -m coverage run -m robot.run  --outputdir results  .'
               // sh 'python3 -m coverage xml'
               }
        }
    }
    post {
          // always {
          //   script {
          //     step(
          //         [
          //           $class              : 'RobotPublisher',
          //           outputPath          : 'results',
          //           outputFileName      : 'output.xml',
          //           reportFileName      : 'report.html',
          //           logFileName         : 'log.html',
          //           disableArchiveOutput: false,
          //           passThreshold       : 60,
          //           unstableThreshold   : 40,
          //           otherFiles          : "**/*.png,**/*.jpg",
          //         ]
          //       )
          //   }
          // }  
          success {
            setBuildStatus("Build succeeded", "Build", "SUCCESS");
          }
          failure {
            setBuildStatus("Build failed", "Build", "FAILURE");
          }
         
	}
}
