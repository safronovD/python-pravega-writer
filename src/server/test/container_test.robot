*** Settings ***
Library             RequestsLibrary
Library             server.test.container_setup.ContainerSetup    ${tag}      WITH NAME    obj

Test Setup          Create connection
Test Teardown       Close connection

*** Variables ***
${base_url}         http://192.168.70.216:666
${tag}

*** Test Cases ***
Check connection to container

    #${response}     Get request     conn    /v1
    #                Should be equal     ${response.status_code}    ${200}

    Log             ${tag}

*** Keywords ***
Create connection
    obj.build_image     server
    obj.run_container   server
    #Create session      conn     ${base_url}     max_retries=10

Close connection
    #Delete all sessions
    obj.remove_container        server
    obj.remove_image            server
    