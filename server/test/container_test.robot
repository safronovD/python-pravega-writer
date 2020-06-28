*** Settings ***
Library             RequestsLibrary
Library             server.test.setup.Setup    ${tag}      WITH NAME    obj
Library             OperatingSystem

Test Setup          Create connection
Test Teardown       Close connection

*** Variables ***
${base_url}         http://http://192.168.70.216:666
${tag}

*** Test Cases ***
Check connection to container

    ${response}     Get request     conn    /v1
    Log             ${response.status_code}
                    Should be equal     ${response.status_code}    ${200}

    Log             ${tag}

*** Keywords ***
Create connection
    obj.build_image
#    obj.show_all_containers
    obj.run_container
#    obj.show_all_containers
    Create session     conn     ${base_url}

Close connection
    Delete all sessions
#    obj.show_all_containers
    obj.remove_container
#    obj.show_all_containers
    obj.remove_image