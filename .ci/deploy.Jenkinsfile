void helmLint(String chart_dir) {
    sh "helm lint ./${chart_dir}"
}

void helmDeploy(Map args) {
    if (args.dry_run) {
        sh '''
            echo Running dry-run deployment
            helm upgrade --dry-run --debug --install ${args.name} ./${args.chart_dir} --set Replicas=${args.replicas}
        '''
    } else {
        sh '''
            echo Running deployment
            helm upgrade --install ${args.name} ./${args.chart_dir} --set Replicas=${args.replicas}
            echo Application ${args.name} successfully deployed. Use helm status ${args.name} to check
        '''
    }
}

pipeline {
    agent {
        kubernetes {
            label 'jenkins-pod-helm'
            yamlFile '.ci/pod-templates/pod-helm.yaml'
        }
    }
    options {
        buildDiscarder(logRotator(numToKeepStr: '20', artifactNumToKeepStr: '20'))
        timestamps()
    }

    environment {
        CONFIG = readJSON file: '.ci/config.json'
    }

    stages {
        stage ('Helm test') {
            steps {
                container('helm') {

                    sh 'echo Helm test'

                    helmLint(CONFIG.app.chart)

                    helmDeploy(
                        dry_run       : true,
                        name          : CONFIG.app.name,
                        chart_dir     : CONFIG.app.chart,
                        replicas      : CONFIG.app.replicas
                    )
                }
            }
        }

        stage ('Deploy') {
            steps {
                container('helm') {

                    sh 'echo Deploy'

                    //helmDeploy(
                    //    dry_run       : false,
                    //    name          : CONFIG.app.name,
                    //    chart_dir     : CONFIG.app.chart,
                    //    replicas      : CONFIG.app.replicas
                    //)
                }
            }
        }
    }

    post {
        always {
            script {
                def publish_result = load(".ci/publish_result.groovy")
                publish_result.setBuildStatus("Deploy", currentBuild.result);
            }
        }

	}
}