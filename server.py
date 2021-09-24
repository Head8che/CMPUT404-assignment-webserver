#  coding: utf-8 
import socketserver
import os

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
# https://realpython.com/python-requests/#the-get-request
# https://docs.python.org/3/library/stdtypes.html

class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).decode("utf-8")
        try:
            request = self.data.splitlines()[0].split()
            method, uri = request[0], request[1]
            if method != "GET":
                self.request.sendall("HTTP/1.1 405 Method Not Allowed\r\n\r\n".encode())
                return
            if "/../" in uri:
                self.request.sendall(bytearray("HTTP/1.1 404 Not Found\r\n", "utf-8"))
                return
            
            try:
                if os.path.isdir("www" + uri):
                    if uri.endswith("/"):  # Returning the default index
                        uri += "index.html"
                        uri = "www" + uri # to serve files from ./www
                        with open(uri, "r") as f:
                            self.request.sendall(bytearray("HTTP/1.1 200 OK\r\nContent-Type: text/%s; charset=utf-8\r\n\r\n"%(uri.split(".")[1])+f.read(), 'utf-8'))
                    else:
                        self.request.sendall(bytearray("HTTP/1.1 301 Moved Permanently\n", "utf-8"))
                elif not os.path.isfile("www" + uri): # Not Found or File Not Found error message
                    self.request.sendall(bytearray("HTTP/1.1 404 Not Found\r\n", "utf-8"))
                    return
                else:
                    uri = "www" + uri
                    with open(uri, "r") as f:
                            self.request.sendall(bytearray("HTTP/1.1 200 OK\r\nContent-Type: text/%s; charset=utf-8\r\n\r\n"%(uri.split(".")[1])+f.read(), 'utf-8'))
            except: # Not Found or File Not Found error message
                self.request.sendall(bytearray("HTTP/1.1 404 Not Found\r\n", "utf-8"))
                return
        except: # Not Found or File Not Found error message
            self.request.sendall(bytearray("HTTP/1.1 404 Not Found\r\n", "utf-8"))
            return

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
