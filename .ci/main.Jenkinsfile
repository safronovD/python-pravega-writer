pipeline {
    agent any

    options {
         buildDiscarder(logRotator(numToKeepStr: '20', artifactNumToKeepStr: '20'))
         timestamps()
    }
    stages {
        stage('Preparation') {
            steps {
                echo 'Preparations are running...'
            }
        }
    
       stage('Unit tests') {
           steps {
               echo 'Unit tests are running...'
//               build 'Tests'
           }
        }
       stage('Container tests') {
           steps {
               echo 'Container tests are running...'
               build 'Container'
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
                def externalMethod = load(".ci/publish_result.groovy")
                externalMethod.setBuildStatus("Build", currentBuild.result);
            }
        }
	}
}
