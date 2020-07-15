*** Settings ***
Library             RequestsLibrary
Library             e2e.helm_setup.Setup     ${chartId}      WITH NAME   helm
Test Setup          Install chart
Test Teardown       Uninstall chart

*** Variables ***
${chartId}

*** Test Cases ***
Check connection to NodePort by RequestsLibrary
    ${nodeIP}           helm.get_node_ip
    ${nodePort}         helm.get_node_port
    Create Session      connection              http://${nodeIP}:${nodePort}       max_retries=15
    ${resp}             Get request             connection         /v1
    Should be equal     ${resp.status_code}     ${200}

*** Keywords ***
Install chart
    helm.install_helm_chart

Uninstall chart
    helm.delete_helm_chart