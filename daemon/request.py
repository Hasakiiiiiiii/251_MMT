#
# Copyright (C) 2025 pdnguyen of HCMC University of Technology VNU-HCM.
# All rights reserved.
# This file is part of the CO3093/CO3094 course.
#
# WeApRous release
#
# The authors hereby grant to Licensee personal permission to use
# and modify the Licensed Source Code for the sole purpose of studying
# while attending the course
#

"""
daemon.request
~~~~~~~~~~~~~~~~~

This module provides a Request object to manage and persist 
request settings (cookies, auth, proxies).
"""
from .dictionary import CaseInsensitiveDict

class Request():
    """The fully mutable "class" `Request <Request>` object,
    containing the exact bytes that will be sent to the server.

    Instances are generated from a "class" `Request <Request>` object, and
    should not be instantiated manually; doing so may produce undesirable
    effects.

    Usage::

      >>> import deamon.request
      >>> req = request.Request()
      ## Incoming message obtain aka. incoming_msg
      >>> r = req.prepare(incoming_msg)
      >>> r
      <Request>
    """
    __attrs__ = [
        "method",
        "url",
        "headers",
        "body",
        "reason",
        "cookies",
        "body",
        "routes",
        "hook",
    ]

    def __init__(self):
        #: HTTP verb to send to the server. => "POST"
        self.method = None 

        #: HTTP URL to send the request to. => "/login?redirect=/home"
        self.url = None
        
        #: dictionary of HTTP headers. => {"Host": "localhost:8080", "User-Agent": "curl/7.81.0", "Content-Type": "application/x-www-form-urlencoded", "Cookie": "auth=true"}
        self.headers = None
       
        #: HTTP path => "/login"
        self.path = None         
       
        # The cookies set used to create Cookie header => {"auth": "true", "theme": "dark"}
        self.cookies = None
       
        #: request body to send to the server. => "username=admin&password=123456"
        self.body = None
       
        #: Routes => {"/login": login_handler, "/": index_handler}
        self.routes = {}
        
        #: Hook point for routed mapped-path => callback to route handler function
        self.hook = None

    def extract_request_line(self, request):  # Request Line: POST /login HTTP/1.1
        try:
            lines = request.splitlines()
            first_line = lines[0]
            method, path, version = first_line.split()

            if path == '/':
                path = '/index.html'
            elif path == '/login':
                path = '/login.html'
        except Exception:
            return None, None, None

        return method, path, version
    
    """
    headers = {
        "host": "localhost:8080",
        "content-type": "application/json",
        "cookie": "auth=true"
    }
    """         
    def prepare_headers(self, request): # Host: localhost:8080
        """Prepares the given HTTP headers."""
        lines = request.split('\r\n')
        headers = {}
        # for line in lines[1:-1]: # (lines 1 -> n - 1)
        for line in lines[1:]: 
            if ': ' in line:
                key, val = line.split(': ', 1)
                headers[key.lower()] = val # headers[host] = localhost:8080

        print("[Request] HEADERS {}".format(headers))
        return headers

    def prepare(self, request, routes=None):
        """Prepares the entire request with the given parameters."""

        # Prepare the request line from the request header
        self.method, self.path, self.version = self.extract_request_line(request)
        print("[Request] {} path {} version {}".format(self.method, self.path, self.version))

        #
        # @bksysnet Preapring the webapp hook with WeApRous instance
        # The default behaviour with HTTP server is empty routed
        #
        # TODO manage the webapp hook in this mounting point
        #
   
        if not routes == {}:
            self.routes = routes
            self.hook = routes.get((self.method, self.path))
            #
            # self.hook manipulation goes here
            # ...
            #
        self.headers = self.prepare_headers(request)

        lines = request.split("\r\n\r\n", 1)

        self.prepare_body(lines[-1], None, None)

        cookies = self.headers.get('cookie', '') # cookie: sessionid=abc123; theme=dark; auth=true

        print ("[Request] COOKIES {}".format(cookies))
            # 
            #  TODO: implement the cookie function here
            #        by parsing the header            
            # 
        cookies = self.parse_cookies(cookies) # my code
        self.prepare_cookies(cookies) # my code

        print ("[Request] COOKIES {}".format(cookies))

        """
        {
            "sessionid": "abc123",
            "theme": "dark",
            "logged": "true"
        }
        """

        return

    def prepare_body(self, data, files, json=None):
        self.prepare_content_length(self.body)
        self.body = data
        #self.body = body
        #
        # TODO prepare the request authentication
        #
	# self.auth = ...
        return


    def prepare_content_length(self, body):
        # self.headers["Content-Length"] = "0"
        #
        # TODO prepare the request authentication
        #
	# self.auth = ...
        if body is None:
            length = 0
        elif isinstance(body, bytes):
            length = len(body)
        else:
            length = len(str(body).encode("utf-8"))

        self.headers["Content-Length"] = str(length)

    def prepare_auth(self, auth, url=""):
        #
        # TODO prepare the request authentication
        #
	# self.auth = ...
        if auth is None:
            return
        
        if (url.find("login") != -1):
            self.headers["Authorization"] = auth # Authorization: Basic YWRtaW46MTIzNDU2
         
        return

    def prepare_cookies(self, cookies): 
        # self.headers["Cookie"] = cookies # Cookie: auth=true
        self.cookies = {}
        self.cookies = cookies

    # My code
    def parse_cookies(self, init_cookies):
        new_cookies = {}
        if init_cookies:
            parts = init_cookies.split("; ")
            for part in parts:
                key, value = part.split("=", 1)
                new_cookies[key] = value
        return new_cookies
