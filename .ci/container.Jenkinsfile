
pipeline {
   agent any
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
            // }
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
