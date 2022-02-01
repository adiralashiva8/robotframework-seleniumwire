# robotframework-seleniumwire

Wrapper of [python selenium-wire]() to capture browser network using robotframework

![PyPI version](https://badge.fury.io/py/robotframework-seleniumwire.svg)
[![Downloads](https://pepy.tech/badge/robotframework-seleniumwire)](https://pepy.tech/project/robotframework-seleniumwire)
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)
![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)

## Installation

 To install robotframework-seleniumwire
 ```
 $ pip install robotframework-seleniumwire==0.1.0
 ```
 Keyword documentation [link](https://robotframework-seleniumwire.netlify.app/)


## Usage:

 ```
*** Settings ***
Library    SeleniumWireLibrary

*** Variables ***
&{options}
...    disable_encoding=${True}
...    enable_har=${True}

@{scopes}    .*google.com.*

*** Test Cases ***
Capture Google Home Page Network Logs
    # launch chrome browser
    Launch Web Browser    ${options}

    # capture requests only matching `@{scopes}` regular expression
    Set Request Scope    ${scopes}
    
    # navigate to home page
    Go To URL    https://google.com/
    
    # log all requests in google home page
    ${requests}=    Get All Requests
    Log    ${requests}
    
    # get & log request matching specific text 
    ${request}=    Get Request By Name    accounts.google.com    request
    Log    ${request}
    
    # create HAR file
    HAR Archive    ${EXECDIR}/test.har
    
    # clear all captured requests
    Clear Requests

    [Teardown]    Quit Browser
 ```

---

:star: repo if you like it

---