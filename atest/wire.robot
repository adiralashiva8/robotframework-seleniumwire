*** Settings ***
Library    SeleniumWireLibrary
Force Tags    449

*** Variables ***
&{options}
...    disable_encoding=${True}
...    enable_har=${True}

@{scopes}    .*yahoo.*

*** Test Cases ***
Network Logs Check
    Launch Web Browser    ${options}
    # Set Request Scope    ${scopes}
    Go To URL    https://gmail.com/

    ${requests}=    Get All Requests
    Log    ${requests}

    ${request}=    Get Request By Name    accounts.google.com    request
    Log    ${request}

    HAR Archive    ${EXECDIR}/test.har
    
    Clear Requests
    [Teardown]    Quit Browser