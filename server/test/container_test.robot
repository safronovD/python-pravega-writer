*** Settings ***
Library             RequestsLibrary
Library             server.test.container_setup.ContainerSetup    ${tag}      WITH NAME    obj

Test Setup          Create connection
Test Teardown       Close connection

*** Variables ***
${tag}

*** Test Cases ***
Check connection to pod
    ${response}     Get request     conn    /v1
                    Should be equal     ${response.status_code}    ${200}

    Log             ${tag}

*** Keywords ***
Create connection
    ${pod_ip}           obj.get_pod_ip      server
    obj.run_pod         server
    obj.wait
    Create session      conn     http://${pod_ip}:666     max_retries=10

Close connection
    Delete all sessions
    obj.delete_pod      server
    