#!/usr/bin/env python3
import http.server
import socketserver
import crypt
from io import BytesIO
from string import Template
from secrets import *

# HTTP Server file request responses
class KickstartHandler(http.server.SimpleHTTPRequestHandler):
    def send_head(self):
        if self.translate_path(self.path).endswith(f"/{KICKSTART_FILE}"):
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=ascii")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            return BytesIO(body.encode("ascii"))
        else:
            self.send_response(404)
            self.end_headers()


# User password + MD5 + Salt
USER_PASS = crypt.crypt(USER_PASS, crypt.mksalt())

# Check for Full Disk Encryption password
try:
    if FDE_PASS:
        FDE_PASS = f'--encrypted --luks-version=luks2 --passphrase="{FDE_PASS}"'
except:
    pass

# Check for bootloader password
try:
    if BOOTLOADER_PASS:
        BOOTLOADER_PASS = f"--password={BOOTLOADER_PASS}"
except:
    pass


# Pass the variables to the Kickstart file
with open(KICKSTART_FILE, "r") as f:
    t = Template(f.read())
    body = t.safe_substitute(
        username=USER_NAME,
        userpass=USER_PASS,
        fdepass=FDE_PASS,
        hostname=HOST_NAME,
        blpass=BOOTLOADER_PASS,
    )

# HTTP server for the installation media to pull the Kickstart file from
with socketserver.TCPServer((LISTEN_ADDR, LISTEN_PORT), KickstartHandler) as httpd:
    print(f"Serving kickstart file on http://{LISTEN_ADDR}:{LISTEN_PORT}.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Exiting.")
        exit(0)
