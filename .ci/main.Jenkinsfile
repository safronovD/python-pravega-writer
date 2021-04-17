pipeline {
    agent any

    options {
         buildDiscarder(logRotator(numToKeepStr: '20', artifactNumToKeepStr: '20'))
         timestamps()
    }

    stages {

       stage('Container tests') {
           steps {
               echo 'Container tests are running...'
//               build 'Container'
           }
        }
       stage('E2E tests') {
            steps {
                echo 'E2E is running...'
//                build 'e2e'
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
