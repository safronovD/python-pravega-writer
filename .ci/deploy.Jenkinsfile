void helmLint(String chart_dir) {
    sh "helm lint ./${CHART}"
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

    stages {
        stage ('Helm test') {
            steps {
                container('helm') {

                    sh 'echo Helm test'

                    script {
                        def config = readJSON file: './ci/config.json'
                    }
                    sh "echo ${config.name}"

                    //helmLint(CHART)

                    //helmDeploy(
                    //    dry_run       : true,
                    //    name          : NAME,
                    //    chart_dir     : CHART,
                    //    replicas      : 1
                    //)
                }
            }
        }

        stage ('Deploy') {
            steps {
                container('helm') {

                    sh 'echo Deploy'

                    //helmDeploy(
                    //    dry_run       : false,
                    //    name          : NAME,
                    //    chart_dir     : CHART,
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