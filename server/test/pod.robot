*** Settings ***
Library             RequestsLibrary
Library             server.test.pod_setup.pod_setup.PodSetup    WITH NAME    obj

Test Setup          Create connection
Test Teardown       Close connection


*** Test Cases ***
Check connection to pod
    ${response}     Get request     conn    /v1
                    Should be equal     ${response.status_code}    ${200}

*** Keywords ***
Create connection
    obj.run_pod         server
    ${pod_ip}           obj.get_pod_ip      server
    Create session      conn     http://${pod_ip}:666     max_retries=10

Close connection
    Delete all sessions
    obj.delete_pod      server
    