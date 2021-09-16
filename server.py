#  coding: utf-8 
import socketserver

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

    def get_method(self):
        method = self.data.splitlines()[0]
        return method.decode('utf-8').split()[0]
    
    # serving index.html
    def get_mimetype(self):
        return

    def get_path_info(self):
        path = self.data.splitlines()[0]
        return path

    def get_host(self):
        host = self.data.splitlines()[1]
        return host

    def get_port(self):
        port = self.data.splitlines()[0]
        return port

# reference for formatting response: https://gist.github.com/bradmontgomery/2219997
    def status_200(self, message): # OK
        head = "HTTP/1.1 200 {message}\n\n"
        content = f"<html><body><h1>{message}</h1></body></html>"
        return head.encode('utf-8'), content.encode('utf-8')

    def status_404(self, message): # Not found
        head = "HTTP/1.1 404 {message}\n\n"
        content = f"<html><body><h1>{message}</h1></body></html>"
        return head.encode('utf-8'), content.encode('utf-8')
    
    def status_405(self, message): # Method Not Allowed
        head = "HTTP/1.1 405 {message}\n\n"
        content = f"<html><body><h1>{message}</h1></body></html>"
        return head.encode('utf-8'), content.encode('utf-8')

    # TODO: add redirect path as param
    def status_301(self, message): # Redirect
        head = "HTTP/1.1 301 {message}\n\n"
        content = f"<html><body><h1>{message}</h1></body></html>"
        return head.encode('utf-8'), content.encode('utf-8')

# reference: https://ruslanspivak.com/lsbaws-part2/
    def create_response(self):
        return
    
    # services a request
    def handle(self):

        self.data = self.request.recv(1024).strip()
        # print(self.data.splitlines())
        # print ("Got a request of: %s\n" % self.data)

        if self.get_method() != "GET": # Incorrect Method
            header, response = self.status_405("Method Not Allowed")
        # elif: # Redirect
        #     pass
        # elif: # File Not Found
        #     pass
        else:
            header, response = self.status_200("OK")

        # TODO: handle header & response for methods
        # self.request.sendall(bytearray("OK",'utf-8'))
        data = header
        data += response
        self.request.sendall(data)
        self.request.close()

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
