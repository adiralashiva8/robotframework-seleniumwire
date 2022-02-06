*** Settings ***
Library    SeleniumWireLibrary

*** Variables ***
&{options}
...    disable_encoding=${True}
...    enable_har=${True}
...    exclude_hosts=['google-analytics.com', 'cdn.sstatic.net']

@{scopes}    .*stackoverflow.*

*** Test Cases ***
Network Logs Check
    # launch selenium-wire chrome browser
    Open Browser    ${options}

    # set domains to be captured
    Set Request Scope    ${scopes}
    
    # navigate to stackoverflow questions page
    Go To    https://stackoverflow.com/questions

    # get and log all stackoverflow requests
    ${stack_requests}=    Get All Requests
    Log    ${stack_requests}

    ${questions_request}=    Get Request By Name    /questions    request
    Log    ${questions_request}

    ${questions_response}=    Get Request By Name    /questions    response
    Log    ${questions_response}

    # clear stack requests
    Clear Requests

    # enter some random text
    Wait Until Page Contains Element    name:q
    Input Text    name:q    Robotframework
    Sleep   3s

    # click on about
    Wait Until Element Is Visible    link text:About
    Click Element    link text:About

    Wait Until Page Contains Element    xpath://a[text()='Leadership']
    Wait Until Element Is Visible    xpath://a[text()='Leadership']
    Wait For Request    /company

    ${about_requests}=    Get All Requests
    Log    ${about_requests}

    &{request}=    Get Request By Name    /company    request
    Log    ${request.Method}
    Log    ${request.RequestURL}
    Log    ${request.Path}
    Log    ${request.Response}

    HAR Archive    ${EXECDIR}/stackoverflow.har

    [Teardown]    Close All Browsers