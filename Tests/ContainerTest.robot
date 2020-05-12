Documentation   Robot test

*** Settings ***
Library             RequestsLibrary
# Test Setup          Create container
# Test Teardown       Teardown



*** Variables ***
${base_url}         http://localhost:666
${url}              /

*** Test Cases ***
Проверить доступность Wiki
                    Create session     conn     ${base_url}    disable_warnings=1
    ${response}     Get request        conn     ${url}
                    Delete all sessions
                    Should be equal    ${response.status_code}    ${200}

*** Keywords ***