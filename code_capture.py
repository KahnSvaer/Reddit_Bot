from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import logging

__all__ = ["get_authorization_code"]
logging.basicConfig(level=logging.ERROR)

class CodeHandler(BaseHTTPRequestHandler):
    """
    A class that is basically used to talk with
    """
    authorization_code = None

    def log_message(self, format, *args):
        pass

    def do_GET(self):
        query = self.path.split("?")[-1]
        if "code=" in query:
            CodeHandler.authorization_code = query.split("code=")[-1].split("&")[0]
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"<html><body><h1>Authorization complete!</h1><p>You can close this tab now.</p></body></html>")
        else:
            self.send_response(400)
            self.wfile.write(b"Error: No code received.")

def get_authorization_code(port=8080):
    server = HTTPServer(("localhost", port), CodeHandler)
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()

    while CodeHandler.authorization_code is None:
        pass
    server.shutdown()
    return CodeHandler.authorization_code
