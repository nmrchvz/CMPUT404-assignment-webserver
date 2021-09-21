#  coding: utf-8 
import socketserver
import os.path
import inspect

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

# os.path - https://www.geeksforgeeks.org/os-path-module-python/
# http status code - https://umbraco.com/knowledge-base/http-status-codes/
# request.sendall () - https://docs.python.org/3/library/socketserver.html

class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip().decode("utf-8")
        request_buffer = self.data.split()
        # Checks to see if the request is a GET request, otherwise return 405 Method not found
        if (request_buffer[0].upper() == 'GET'):
            path = 'www' + request_buffer[1]
            # If the path is a file or directory attempt to parse its request and send it to the
            # webserver, otherwise return 404 Not Found
            if os.path.isfile(path) or os.path.isdir(path) or os.path.exists(path):
                ftype = path.split(".")[-1].lower()
                # if path ends in '/', return index html from directories
                
                # if path does not end in '/' or css or html/htm return 301 Moved Permamently
                if path[-1] != "/" and ftype != 'css' and ftype != 'html' and ftype != "htm":
                    try:
                        request_message = open(path+ "/index.html").read()
                        self.message("301 Moved Permanently", "", request_message)
                    except ValueError:
                        self.message("404 Not found")
                    return

                if path[-1] == "/":
                    request_message = open(path + "index.html").read()
                    self.message("200 OK", 'html',request_message)
                else: 
                    request_message = open(path).read()
                    self.message("200 OK", content_type = ftype, file = request_message)
            else:
                self.message("404 Not found")
        else:
            # Returns status code 405 Method Not Allowed (POST/PUT/DELETE)
            self.message("405 Method  Method Not Allowed")
    
    def message(self, status_code, content_type = "", file = ""):
        message = "HTTP/1.1 " + status_code + "\r\n"
        if content_type:
            message += "Content-Type: text/" + content_type + "\r\n"
        if file:
            message += "\r\n" + file 
        self.request.sendall(bytearray(message + "\r\n", 'utf-8'))
        
if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
