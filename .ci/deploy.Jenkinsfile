void helmLint(String chart_dir) {
    sh "helm lint ./${chart_dir}"
}

void helmDeploy(Map args) {
    if (args.dry_run) {
        sh "helm upgrade --dry-run --debug --install ${args.name} ./${args.chart_dir} --set Replicas=${args.replicas}"
    } else {
        sh "helm upgrade --install ${args.name} ./${args.chart_dir} --set Replicas=${args.replicas}"
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

    stages {
        stage ('Helm test') {
            steps {
                container('helm') {

                    sh 'echo Helm test'

                    helmLint('ppw-chart')

                    helmDeploy(
                        dry_run       : true,
                        name          : 'pravega-writer',
                        chart_dir     : 'ppw-chart',
                        replicas      : 1
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
                    //    name          : 'pravega-writer',
                    //    chart_dir     : 'ppw-chart',
                    //    replicas      : 1
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
