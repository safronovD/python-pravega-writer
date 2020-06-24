*** Settings ***
Library             RequestsLibrary
Library             server.test.setup.Setup    ${tag}      WITH NAME    obj
Library             OperatingSystem

Test Setup          Create connection
Test Teardown       Close connection

*** Variables ***
${base_url}         http://localhost:666
${tag}              123

*** Test Cases ***
Check connection to container


     Log            ${tag}

*** Keywords ***
Create connection
    obj.build_image
    

Close connection

    obj.remove_image