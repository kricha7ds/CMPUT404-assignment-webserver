#  coding: utf-8 
import socketserver
from time import gmtime, strftime
import time
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
# RESOURCES:
# Good resource: https://www.codementor.io/@joaojonesventura/building-a-basic-http-server-from-scratch-in-python-1cedkg0842
# Anotha one: https://ruslanspivak.com/lsbaws-part2/
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/

BASEURL = "http://127.0.0.1:8080"

class MyWebServer(socketserver.BaseRequestHandler):

    def get_gmtime(self):
        return time.strftime("Date: %a, %d %b %Y %I:%M:%S %p GMT\r\n", time.gmtime())

    def get_method(self):
        method = self.data.splitlines()[0]
        return method.split()[0]

    def get_len(self, msg):
        length = len(msg)
        return f"Content-Length: {length}\r\n" # specification
    
    # identify media type of response to be sent
    def get_mimetype(self, fp):
        spec = "Content-Type: " # specification
        if fp.endswith(".css"):
            ftype = "text/css\r\n\r\n"
        elif fp.endswith(".html"):
            ftype = "text/html\r\n\r\n"
        else:
            ftype = "application/octet-stream\r\n\r\n"
        return spec + ftype

    def valid_file(self, path):
        return os.path.isfile(path)

    def valid_path(self, path):
        _dir = "/www"
        return os.path.exists(os.path.abspath(os.getcwd() + _dir + path))

    def get_path_info(self, path):
        _dir = "/www"
        if path.endswith('/'):
            path = os.path.abspath(os.getcwd() + _dir + path + 'index.html') 
        else:
            path = os.path.abspath(os.getcwd() + _dir + path)
        return path

    def get_path(self):
        return self.data.splitlines()[0].split()[1]

    def read_file(self, fp):
        with open(fp, 'rb') as f:
            return f.read()

    def status_200(self): # OK
        head = 'HTTP/1.1 200 OK\r\n'
        return head

    def status_404(self): # Not found
        head = 'HTTP/1.1 404 Not Found\r\n'
        content = f'<h1>Error 404</h1><p>File Not Found.</p>'
        return head, content.encode('utf-8')

    def status_405(self): # Method Not Allowed
        head = 'HTTP/1.1 405 Method Not Allowed\r\n'
        content = f'<h1>Error 405</h1><p>Method Not Allowed.</p>'
        return head, content.encode('utf-8')

    def status_301(self, path): # Redirect
        head = f'HTTP/1.1 301 Moved Permanently\r\nLocation: {BASEURL}{path}/\r\n'
        content = f'<h1>Error 301</h1><p>We have moved!</p>'
        return head, content.encode('utf-8')
    
    def handle(self):
        # print ("Got a request of: %s\n" % self.data)
        self.data = self.request.recv(1024).strip().decode('utf-8')

        # print(self.data.splitlines())
        
        path = self.get_path()
        fp = self.get_path_info(path)

        # print("FILEPATH: %s" % fp)
        # print("PATH: %s" % path)

        if self.get_method() != "GET": # Incorrect Method
            header, body = self.status_405()
        # invalid filepath requested, but the path (file) does exist
        elif ((not self.valid_file(fp)) and self.valid_path(path)): # Redirect
            header, body = self.status_301(path)
        # filepath requested not found (does not overlap with cwd)
        elif os.getcwd() not in fp: # File Not Found
            header, body = self.status_404()
        else: # 200 OK
            try: # build the response
                body = self.read_file(fp)
                header = self.status_200() # status
                # header += self.get_gmtime() # date
                # header += self.get_len(body) # content-length
                # header += "Connection: close\r\n" # connection is closed
                # header += self.get_mimetype(fp)
            except Exception as e: # Some error occurred during response build
                header, body = self.status_404()

        # tack on the rest of the header specs
        header += self.get_gmtime() # date
        header += self.get_len(body) # content-length
        header += "Connection: close\r\n" # connection is closed
        header += self.get_mimetype(fp)

        data = header.encode('utf-8')
        data += body
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
