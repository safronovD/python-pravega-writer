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
    Log                 ${resp.status_code}
    Should be equal     ${resp.status_code}   ${200}

Check connection to NodePort by Process Library
    ${nodeIP}           helm.get_node_ip
    ${nodePort}         helm.get_node_port    ${chartId}
    ${resp}             Run Process           curl -i ${nodeIP}:${nodePort}    shell=True
    Log                 ${resp.stdout}
    Should Contain      ${resp.stdout}        HTTP/1.1 200 OK

*** Keywords ***
Install chart
    helm.install_helm_chart     ${chartId}

Uninstall chart
    helm.delete_helm_chart      ${chartId}