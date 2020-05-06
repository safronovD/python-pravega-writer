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
    sh "/usr/local/bin/helm lint ${chart_dir}"
}

void helmDeploy(Map args) {
    //configure helm client and confirm tiller process is installed

    if (args.dry_run) {
        println "Running dry-run deployment"

        sh "/usr/local/bin/helm upgrade --dry-run --debug --install ${args.name} ${args.chart_dir} --set Replicas=${args.replicas} --namespace=default"
    } else {
        println "Running deployment"
        sh "/usr/local/bin/helm upgrade --install ${args.name} ${args.chart_dir} --set Replicas=${args.replicas} --namespace=default"

        echo "Application ${args.name} successfully deployed. Use helm status ${args.name} to check"
    }
}

def chart_dir = "/ppw-chart"

pipeline {
    agent {
        kubernetes {
            label 'jenkins-pod'
            yamlFile '.ci/jenkinsPodTemplate.yaml'
        }
    }

   stages {

       stage ('Helm test') {
            steps {
                container('helm') {
                    sh 'echo Helm test'

                    // run helm chart linter
                    helmLint(chart_dir)

                    // run dry-run helm chart installation
                    helmDeploy(
                        dry_run       : true,
                        name          : config.app.name,
                        chart_dir     : chart_dir,
                        replicas      : config.app.replicas
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