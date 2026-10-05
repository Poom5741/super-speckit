"""Real HTTP public seam used to evaluate verification controls, never a host."""
import json
import os
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer

count = 0
class Handler(BaseHTTPRequestHandler):
    def body(self):
        value = dict(instance=os.environ['PSTACK_INSTANCE'],build_id=os.environ['PSTACK_BUILD_ID'],healthy=True,count=count)
        self.send_response(200); self.send_header('Content-Type','application/json'); self.end_headers(); self.wfile.write(json.dumps(value).encode())
    def do_GET(self): self.body()
    def do_POST(self):
        global count
        if len(sys.argv) < 3 or sys.argv[2] != 'broken': count += 1
        self.body()
    def log_message(self,*args): pass
HTTPServer(('127.0.0.1',int(sys.argv[1])),Handler).serve_forever()
