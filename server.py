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
# https://ruslanspivak.com/lsbaws-part2/
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/

class MyWebServer(socketserver.BaseRequestHandler):

    def get_method(self):
        method = self.data.splitlines()[0]
        return method.decode('utf-8')
    
    def get_path_info(self):
        path = self.data.splitlines()[0]
        return path

    def get_host(self):
        host = self.data.splitlines()[1]
        return host

    def get_port(self):
        port = self.data.splitlines()[0]
        return port

    def status_404(self): # Not found
        return
    
    def status_405(self): # Method Not Allowed
        return

    # TODO: add redirect path as param
    def status_301(self): # Redirect
        return
    
    # services a request
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print(self.data.splitlines())
        # print ("Got a request of: %s\n" % self.data)

        # TODO: handle header & response for methods
        self.request.sendall(bytearray("OK",'utf-8'))

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
