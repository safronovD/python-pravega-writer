*** Settings ***
Library             RequestsLibrary
Library             setup.py
Test Setup          Create connection
Test Teardown       Close connection

*** Variables ***
${base_url}          http://localhost:666

*** Test Cases ***
Check connection to container
    ${response}     Get request     conn   /
                    Should be equal     ${response.status_code}    ${200}

*** Keywords ***
Create connection
    Build image
    Run container
    Create session     conn     ${base_url}    disable_warnings=1

Close connection
    Delete all sessions
    Remove container
    Remove image