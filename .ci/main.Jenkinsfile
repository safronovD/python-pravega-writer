pipeline {
    agent any

    options {
         buildDiscarder(logRotator(numToKeepStr: '20', artifactNumToKeepStr: '20'))
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
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploy is running...'
//                build 'Deploy'
            }
        }
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
