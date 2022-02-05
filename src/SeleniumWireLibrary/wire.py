import json
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from robot.libraries.BuiltIn import BuiltIn
from robot.api.deco import keyword
from robot.api import logger
from .version import VERSION

class SeleniumWireLibrary():

    """
    |  = Repo =      |  = URL =  |
    |  SeleniumWire  |  https://github.com/wkeeling/selenium-wire  |

    Used to capture browser network traffic in robotframework uses seleniumwire internally
    """

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = VERSION

    def __init__(self):
        self.driver = None
        self.requests = None
    
    @keyword
    def launch_web_browser(self, options=None):
        """
        Launches chrome browser using selenium wire

        |  = Attribute =  |  = Description =  |
        |  options        |  seleniumwire_options passed as dictionary.  |
        
        Supported options - https://github.com/wkeeling/selenium-wire?ref=https://githubhelp.com#all-options  |
        
        
        Example:
        
        |  *** Variables ***  |    |    |
        |  &{options}  |  disable_encoding=${True}  |    |
        |    |    |    |
        |  *** Test Cases ***  |    |    |
        |  Launch SeleniumWire Browser  |    |
        |    |  Launch Web Browser  |  options=${options}  |
        
        """
        self.driver = webdriver.Chrome(seleniumwire_options=options)
    
    @keyword
    def go_to_url(self, url):
        """
        Navigates to mentioned url in launched chrome browser
        
        |  = Attribute =  |  = Description =  |
        |  url        |  url to be navigated  |
        """
        self.driver.get(url)

    @keyword
    def quit_browser(self):
        """
        Close all browsers. Uses `driver.quit()` internally
        """
        self.driver.quit()
    
    @keyword
    def get_all_requests(self):
        """
        Return list of captured requests in chronological order.
        """
        self.requests = self.driver.requests
        return self.requests

    @keyword
    def get_last_request(self):
        """
        Return the most recently captured request.
        """
        return self.driver.last_request
    
    @keyword
    def get_request_by_index(self, index):
        """
        Return request by index

        |  = Attribute =  |  = Description =  |
        |  index        |  index of request  |

        """
        return self.requests[int(index)]
    
    @keyword
    def wait_for_request(pattern, timeout=10):
        """
        Keyword will wait until it sees a request matching a `pattern`
         - `pattern` can be a simple substring or a regular expression.
         - Keyword doesnt make a new request, it wait for previous request
         - A `TimeoutException` is raised if no match is found within the timeout period

        |  = Attribute =  |  = Description =  |
        |  pattern        |  substring or regular expression  |
        |  timeout        |  Wait time before raising timeout exception. Default value is 10  |

        Example:

        |  Wait For Request  |  /api/products/12345/  |
        """
        self.driver.wait_for_request(pattern, timeout=timeout)
    
    @keyword
    def clear_requests(self):
        """
        Clear all captured requests
        """
        del self.driver.requests
    
    @keyword
    def set_request_scope(self, scope=[]):
        """
        Captures network which matches regular expression. Accepts list of regular expressions.
        
        |  = Attribute =  |  = Description =  |
        |  scope[]        |  list of regular expression  |

        Example:

        |  Set Request Scope    |  ['.*robot.*', '.*google.*']  |

        Changes reflects in new requests made after this keyword
        """
        del self.driver.requests
        self.driver.scopes = scope

    @keyword
    def har_archive(self, file):
        """
        Save HAR file to specified location

        |  = Attribute =  |  = Description =  |
        |  file        |  file name. ex: `test.har`  |
        """
        result = self.driver.har
        with open(file, 'w') as f:
            f.write(result)

    @keyword
    def get_request_by_name(self, partialText, type="request"):
        """
        Return request result matching with `partialText`. 

        |  = Attribute =  |  = Description =  |
        |  partialText    |  partial url/text which contains `request.url` context  |
        |  type           |  Type can be `request` or `response`. Default is `request`  |

        Note: This keyword doesnt make any new requests. Should be used after `Get All Requests` keywords
        """
        result_dict = []
        for request in self.requests:
            if partialText in request.url:
                if type == "response":
                    if request.response:
                        result_dict = {
                            "Request URL" : request.url,
                            "Status Code" : request.response.status_code,
                            "Reason" : request.response.reason,
                            "Header" : request.response.headers,
                            "Host" : request.headers['Host'],
                            "Date" : request.response.date,
                            "Body" : request.response.body
                        }
                else:
                    result_dict = {
                        "Method" : request.method,
                        "Request URL" : request.url,
                        "Path" : request.path,
                        "Query String" : request.querystring,
                        "Params" : request.params,                    
                        "Headers" : request.headers,
                        "Host" : request.headers['Host'],
                        "Date" : request.date,
                        "Body" : request.body,
                        "Response" : request.response,
                    }
                break
            
        return result_dict

    @keyword
    def log_request_object(self, type="request"):
        """
        Log all requests. 

        |  = Attribute =  |  = Description =  |
        |  type           |  Type can be `request` or `response`. Default is `request`  |

        Note: This keyword doesnt make any new requests. Should be used after `Get All Requests` keywords
        """
        result_dict = []
        for request in self.requests:
            if type == "response":
                if request.response:
                    result_dict = {
                        "Request URL" : request.url,
                        "Status Code" : request.response.status_code,
                        "Reason" : request.response.reason,
                        "Header" : request.response.headers,
                        "Host" : request.headers['Host'],
                        "Date" : request.response.date,
                        "Body" : request.response.body
                    }
            else:
                result_dict = {
                    "Method" : request.method,
                    "Request URL" : request.url,
                    "Path" : request.path,
                    "Query String" : request.querystring,
                    "Params" : request.params,                    
                    "Headers" : request.headers,
                    "Host" : request.headers['Host'],
                    "Date" : request.date,
                    "Body" : request.body,
                    "Response" : request.response,
                }
            
            logger.info(result_dict)
    
    @keyword
    def click_element(self, locator):
        """
        click on webelement

        |  = Attribute =  |  = Description =  |
        |  locator        |  Webelement to click.  |

         > Locator should be like <startagie>:<locator>
         > Uses `driver.find(By.<stratagies>, <locator>)` method internally. 
         > Refer - https://selenium-python.readthedocs.io/locating-elements.html

        Example:

        |  Click Element   |  xpath://div[text(),'robot']  |
        |  Click Element   |  id:RobotID  |
        |  Click Element   |  name:Robot  |

        """
        locs = locator.split(':', 1)
        webelement = self.driver.find_element(locs[0].lower(), locs[-1])
        webelement.click()
    
    @keyword
    def input_text(self, locator, value):
        """
        Input text into textbox
        
        |  = Attribute =  |  = Description =  |
        |  locator        |  textbox locator  |
        |  value        |  value to be enetered in textbox  |

        Example:

        |  Input Text   |  xpath://div[text(),'robot']  |  Demo  |
        |  Input Text   |  id:RobotID  |  Demo  |

        """
        locs = locator.split(':', 1)
        webelement = self.driver.find_element(locs[0].lower(), locs[-1])
        webelement.send_keys(value)
    
    @keyword
    def select_from_list(self, locator, type, value):
        """
        Select value from drop down list
        
        |  = Attribute =  |  = Description =  |
        |  locator        |  drop down locator  |
        |  type        |  select value based on type. Supported type `index`, `value`, `text`  |
        |  value       |  value to be selected  |

        Example:

        |  Select From List   |  xpath://div[text(),'robot']  |  index  |  0  |
        |  Select From List   |  id:RobotID  |  text  |  Robot  |

        """
        locs = locator.split(':', 1)
        select = Select(self.driver.find_element(locs[0].lower(), locs[-1]))
        if type == "index":
            select.select_by_index(value)
        elif type == "text":
            select.select_by_visible_text(value)
        elif type == "value":
            select.select_by_value(value)
        else:
            pass
    
    @keyword
    def wait_until_page_contains_element(self, locator, timeout=30):
        """
        Wait until page contains element.

        |  = Attribute =  |  = Description =  |
        |  locator        |  wait for specific element to be loaded in page  |
        |  timeout        |  Wait time before throwing exception  |

        """
        locs = locator.split(':', 1)
        element = WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((locs[0].lower(), locs[-1])))