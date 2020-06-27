*** Settings ***
Library             RequestsLibrary
Library             Process
Library             e2e.setup.Setup     WITH NAME   helm
Test Setup          Install chart
Test Teardown       Uninstall chart

*** Variables ***
${chartId}
${nodePort}
${nodeIP}

*** Test Cases ***
Check connection to NodePort by RequestsLibrary
    ${nodeIP}           helm.get_node_ip
    ${nodePort}         helm.get_node_port    ${chartId}
    Create Session      connection            http://${nodeIP}:${nodePort}
    ${resp}             Get request           connection         /
    Should be equal     ${resp.status_code}   ${200}
    Log                 ${resp.status_code}

Check connection to NodePort by Process Library
    ${nodeIP}           helm.get_node_ip
    ${nodePort}         helm.get_node_port    ${chartId}
    ${resp}             Run Process           curl -i ${nodeIP}:${nodePort}    shell=True
    Should Contain      ${resp.stdout}        200 OK
    Log                 ${resp.stdout}

*** Keywords ***
Install chart
    helm.install_helm_chart     ${chartId}

Uninstall chart
    helm.delete_helm_chart      ${chartId}