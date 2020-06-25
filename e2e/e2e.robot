*** Settings ***
Library             RequestsLibrary
Library             e2e.helm.Helm     WITH NAME   helm
Test Setup          Install chart
Test Teardown       Uninstall chart

*** Variables ***
${chartId}
${nodePort}
${nodeIP}

*** Test Cases ***
Check connection to NodePort
    #${nodeIP}           helm.get_node_ip
    #${nodePort}         helm.get_node_port    ${chartId}
    #Create Session      connection            ${nodeIP}:${nodePort}
    #${resp}             Get request           connection         /
    #Should be equal     ${resp.status_code}   ${200}
    Log     ${chartId}

*** Keywords ***
Install chart
    helm.install_helm_chart     ${chartId}

Uninstall chart
    helm.delete_helm_chart      ${chartId}