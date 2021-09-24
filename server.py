#  coding: utf-8 
import socketserver
import os.path
from datetime import datetime, timedelta
# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/

class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip().decode("utf-8")
        request_buffer = self.data.split()
        # Checks to see if the request is a GET request, otherwise return 405 Method not found
        # https://umbraco.com/knowledge-base/http-status-codes/
        if (request_buffer[0].upper() == 'GET'):
            # For checking if '/www' is retrieved from the GET request and formatting
            # for parsing
            path = None
            if (request_buffer[1].startswith("/www")):
                path = 'www' + request_buffer[1][4:]
            else:
                path = 'www' + request_buffer[1]
            # If the path is a file or directory attempt to parse its request and send it to the
            # webserver, otherwise return 404 Not Found
            # https://www.geeksforgeeks.org/python-os-path-isfile-method/
            if os.path.isfile(path) or os.path.isdir(path) or os.path.exists(path):
                ftype = path.split(".")[-1].lower()
                # if path does not end in '/' or css or html/htm add /index.html
                if path[-1] != "/" and ftype != 'css' and ftype != 'html' and ftype != "htm":
                    # if path exists, return 301 Moved Permanently
                    # if the path doesn't exists, then 404 Not Found
                    # https://stackoverflow.com/questions/82831/how-do-i-check-whether-a-file-exists-without-exceptions
                    if os.path.exists(path):
                        request_message = open(path + "/index.html").read()
                        self.message("301 Moved Permanently",content_type="html", file = request_message)
                    else:
                        self.message("404 Not Found")
                    return
                # if path does end in '/' then add index.html and send the message, otherwise send the message as is
                if path[-1] == "/":
                    request_message = open(path + "index.html").read()
                    self.message("200 OK", content_type = 'html', file = request_message)
                else: 
                    request_message = open(path).read()
                    self.message("200 OK", content_type = ftype, file = request_message)
            else:
                self.message("404 Not Found")
        else:
            self.message("405 Method Not Allowed")
    '''
    Purpose: To format a proper HTTP/1.1 messsage for request.sendall() 
    Parameters: status_code (int) - a intger to identify status of a request
                content_type (string) - a string to identify the content (css/html)
                file (string) - the status message returned by the request
    Return: None
    References: https://docs.python.org/3/library/socketserver.html
                https://www.programiz.com/python-programming/datetime/strftime
                https://www.geeksforgeeks.org/python-datetime-timedelta-function/
    '''
    def message(self, status_code, location = "", content_type = "", file = ""):
        time = datetime.now() + timedelta(hours= 6)
        message =  "HTTP/1.1 " + status_code + "\r\n"
        message += time.strftime("Date: %m/%d/%Y, %H:%M:%S GMT")+ "\r\n"
        if location:
            message += "Location: " + location + "\r\n"
        if file:
            message += "Content-Length: " + str(len(file)) + "\r\n"
        message += "Connection: close\r\n"
        if content_type:
            message += "Content-Type: text/" + content_type + "\r\n"
        if file:
            message += "\r\n" + file 
        #print(message)
        self.request.sendall(bytearray(message + "\r\n", 'utf-8'))
        
if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)
    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()