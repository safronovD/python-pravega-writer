*** Settings ***
Library             RequestsLibrary
Library             server.test.setup.Setup    ${tag}      WITH NAME    obj
Library             OperatingSystem

Test Setup          Create connection
Test Teardown       Close connection

*** Variables ***
${base_url}         http://localhost:666
${tag}              %{BUILD_NUMBER}

*** Test Cases ***
Check connection to container
    ${response}     Get request     conn   /v1/
                    Should be equal     ${response.status_code}    ${200}

     Log            ${tag}

*** Keywords ***
Create connection
    obj.build_image
    obj.run_container
    Create session     conn     ${base_url}    disable_warnings=1

Close connection
    Delete all sessions
    obj.remove_container
    obj.remove_image