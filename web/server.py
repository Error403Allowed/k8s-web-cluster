import http.server
import socket
import os
import json
from datetime import datetime

HOSTNAME = socket.gethostname()
START_TIME = datetime.now()

PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Kubernetes Container App</title>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; display: flex; align-items: center; justify-content: center; }}
  .card {{ background: white; border-radius: 16px; padding: 48px; box-shadow: 0 20px 60px rgba(0,0,0,0.3); text-align: center; max-width: 500px; width: 90%; }}
  .badge {{ display: inline-block; background: #667eea; color: white; padding: 8px 24px; border-radius: 20px; font-size: 14px; font-weight: 600; margin-bottom: 20px; text-transform: uppercase; letter-spacing: 1px; }}
  h1 {{ font-size: 28px; color: #333; margin-bottom: 12px; }}
  .hostname {{ font-size: 20px; color: #667eea; font-weight: 700; margin: 16px 0; padding: 12px; background: #f0f0ff; border-radius: 8px; }}
  p {{ color: #666; margin: 8px 0; font-size: 14px; }}
  .status {{ display: inline-flex; align-items: center; gap: 8px; margin-top: 24px; padding: 12px 24px; background: #e8f5e9; border-radius: 8px; color: #2e7d32; font-weight: 600; }}
  .dot {{ width: 10px; height: 10px; border-radius: 50%; background: #4caf50; display: inline-block; animation: pulse 2s infinite; }}
  @keyframes pulse {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: 0.4; }} }}
  .peers {{ margin-top: 24px; padding-top: 24px; border-top: 1px solid #eee; }}
</style>
</head>
<body>
<div class="card">
  <div class="badge">Container App</div>
  <h1>Request Handled By</h1>
  <div class="hostname">{hostname}</div>
  <p>Started: {started}</p>
  <p>Uptime: {uptime}</p>
  <div class="status"><span class="dot"></span> Healthy</div>
  <div class="peers">
    <p>Peer containers: web1, web2, web3</p>
    <p style="font-size:12px;color:#999;margin-top:8px;">Try killing this container — the app keeps running via nginx load balancing</p>
  </div>
</div>
</body>
</html>"""

class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Cache-Control', 'no-store')
            self.end_headers()
            uptime = str(datetime.now() - START_TIME).split('.')[0]
            self.wfile.write(json.dumps({
                'status': 'healthy',
                'hostname': HOSTNAME,
                'uptime': uptime
            }).encode())
        else:
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            uptime = str(datetime.now() - START_TIME).split('.')[0]
            html = PAGE.format(
                hostname=HOSTNAME,
                started=START_TIME.strftime('%Y-%m-%d %H:%M:%S'),
                uptime=uptime
            )
            self.wfile.write(html.encode())

    def log_message(self, format, *args):
        print(f"[{HOSTNAME}] {args[0]} {args[1]} {args[2]}")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    server = http.server.HTTPServer(('0.0.0.0', port), Handler)
    print(f"[{HOSTNAME}] Server running on port {port}")
    server.serve_forever()
