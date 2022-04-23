import json
import socket
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

import controller
import route as route
from errors import YunError

route = route.setup_routes()


# Vercel Api
class handler(BaseHTTPRequestHandler):
    def send_json(self, data):
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def handle_one_request(self):
        """Handle a single HTTP request.

        You normally don't need to override this method; see the class
        __doc__ string for information on how to handle specific HTTP
        commands such as GET and POST.

        """
        try:
            self.raw_requestline = self.rfile.readline(65537)
            if len(self.raw_requestline) > 65536:
                self.requestline = ''
                self.request_version = ''
                self.command = ''
                self.send_error(HTTPStatus.REQUEST_URI_TOO_LONG)
                return
            if not self.raw_requestline:
                self.close_connection = True
                return
            if not self.parse_request():
                # An error code has been sent, just exit
                return

            url = urlparse(self.path)
            route_result = route.match(url.path, self.command)
            if route_result is None:
                self.send_response(404)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write("404 Not Found".encode())
            else:
                try:
                    body_len = int(self.headers.get('Content-Length'))
                    body = self.rfile.read(body_len)

                    query_string = parse_qs(url.query)
                    for key in query_string:
                        if len(query_string[key]) == 1:
                            query_string[key] = query_string[key][0]

                    obj = controller.MainController({
                        'body': body,
                        'queryString': query_string
                    }, route_result)

                    resp = getattr(obj, route_result['action'])()
                    self.send_response(200)
                    if body in resp:
                        self.send_json({"code": 0, "msg": resp['body']})
                except YunError as e:
                    self.send_response(200)
                    self.send_json({"code": e.code, "msg": e.message})
                except Exception as e:
                    self.send_response(500)

            self.wfile.flush() #actually send the response if not already done.
        except socket.timeout as e:
            # a read or a write timed out.  Discard this connection
            self.log_error("Request timed out: %r", e)
            self.close_connection = True
            return
