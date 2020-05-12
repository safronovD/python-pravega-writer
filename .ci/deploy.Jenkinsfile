void setBuildStatus(String context, String message, String state) {
  step([
      $class: "GitHubCommitStatusSetter",
      reposSource: [$class: "ManuallyEnteredRepositorySource", url: "https://github.com/safronovD/python-pravega-writer"],
      contextSource: [$class: "ManuallyEnteredCommitContextSource", context: context],
      errorHandlers: [[$class: "ChangingBuildStatusErrorHandler", result: "UNSTABLE"]],
      statusResultSource: [ $class: "ConditionalStatusResultSource", results: [[$class: "AnyBuildResult", message: message, state: state]] ]
  ]);
}

void helmLint(String chart_dir) {
    // lint helm chart
    sh "helm lint ./${CHART}"
}

void helmDeploy(Map args) {
    //configure helm client and confirm tiller process is installed

    if (args.dry_run) {
        sh 'echo Running dry-run deployment'

        sh "helm upgrade --dry-run --debug --install ${args.name} ./${args.chart_dir} --set Replicas=${args.replicas}"
    } else {
        sh 'echo Running deployment'
        sh "helm upgrade --install ${args.name} ./${args.chart_dir} --set Replicas=${args.replicas}"

        sh 'echo Application ${args.name} successfully deployed. Use helm status ${args.name} to check'
    }
}

pipeline {
    environment {
         CHART = "ppw-chart"
         //CONFIG = new groovy.json.JsonSlurperClassic().parseText(readFile(".ci/config.json"))
    }

    agent {
        kubernetes {
            label 'jenkins-pod'
            yamlFile '.ci/pod-templates/pod-helm.yaml'
        }
    }

   stages {

       stage ('Helm test') {
            steps {
                container('helm') {

                    sh 'echo Helm test'

                    // run helm chart linter
                    helmLint(CHART)

                    // run dry-run helm chart installation
                    helmDeploy(
                        dry_run       : true,
                        name          : CHART,
                        chart_dir     : CHART,
                        replicas      : 1
                    )
                }
            }
        }
    }

    post {
          success {
            setBuildStatus("Deploy succeeded", "Deploy", "SUCCESS");
          }
          failure {
            setBuildStatus("Deploy failed", "Deploy", "FAILURE");
          }
         
	  }
}