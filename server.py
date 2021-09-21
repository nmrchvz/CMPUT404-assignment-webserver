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
# inspect - https://docs.python.org/3/library/inspect.html
# http status code - https://umbraco.com/knowledge-base/http-status-codes/

class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip().decode("utf-8")
        request_buffer = self.data.split()
        
        #print ("Got a request of: %s\n" % self.data_array)
        if (request_buffer[0].upper() == 'GET'):
            url = 'www' + request_buffer[1]
            if os.path.isfile(url) or os.path.isdir(url):
                ftype = url.split(".")[-1].lower()
                if url[-1] != "/" and ftype != 'css' and ftype != 'html':
                    print("301 Moved Permanently")
                    moved = url.split("/")[-1] + "/"
                    print(moved)
                    self.message("301 Moved Permanently")
                    return
                if url[-1] == "/":
                    url = url + "index.html"
                request = open(url).read()
                self.message("200 OK", file_type = ftype, file = request)
            else:
                self.message("404 Not found")
        else:
            self.message("405 Method not found")
    
    def message(self, error_code, file_type = None, file = None):
        message = "HTTP/1.1 " + error_code + "\r\n"
        if file_type != None:
            message += "Content-Type: text/" + file_type + "\r\n"
        if file != None:
            message += file + "\r\n"
        self.request.sendall(bytearray(message, 'utf-8'))
        

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
