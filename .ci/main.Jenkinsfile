pipeline {
    agent any

    options {
         timestamps()
    }

    stages {
       stage('Unit tests') {
           steps {
               echo 'Unit tests are running...'
               build 'Unit tests'
           }
        }

       stage('Integration tests') {
           steps {
               echo 'Integration tests are running...'
               build 'Integration tests'
           }
        }
       stage('E2E tests') {
            steps {
                echo 'E2E is running...'
                build 'E2E tests'
            }
        }

        stage('Perfomance tests') {
            steps {
                echo 'Perfomance tests are running...'
//                build 'Stress'
                build 'Unit tests'
            }
        }

//        stage('Deploy') {
//            steps {
//                echo 'Deploy is running...'
//                build 'Deploy'
//            }
//        }
    }
    post {
        always {
            script {
                def publish_result = load(".ci/publish_result.groovy")
                publish_result.setBuildStatus("All", currentBuild.result);
            }
        }
	}
}
