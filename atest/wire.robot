*** Settings ***
Library    SeleniumWireLibrary

*** Variables ***
&{options}
...    disable_encoding=${True}
...    enable_har=${True}

@{scopes}    .*yahoo.*

*** Test Cases ***
Network Logs Check
    Launch Web Browser    ${options}
    Set Request Scope    ${scopes}
    Go To URL    https://www.google.com/
    # ${requests}=    Get All Requests
    # Log    ${requests}    
    # ${request}=    Get Request By Name    accounts.google.com    request
    # Log    ${request} 
    # HAR Archive    ${EXECDIR}/test.har
    # Clear Requests
    Wait Until Page Contains Element    name:q
    Input Text    name:q    demo
    Click Element    xpath://a[text()='Gmail']
    Sleep   3s
    [Teardown]    Quit Browser