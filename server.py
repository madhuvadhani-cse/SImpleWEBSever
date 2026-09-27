import http.server
import socketserver
import platform
import ctypes

PORT = 8000

def get_ram():
    class MEMORYSTATUSEX(ctypes.Structure):
        _fields_ = [
            ("dwLength", ctypes.c_ulong),
            ("dwMemoryLoad", ctypes.c_ulong),
            ("ullTotalPhys", ctypes.c_ulonglong),
            ("ullAvailPhys", ctypes.c_ulonglong),
            ("ullTotalPageFile", ctypes.c_ulonglong),
            ("ullAvailPageFile", ctypes.c_ulonglong),
            ("ullTotalVirtual", ctypes.c_ulonglong),
            ("ullAvailVirtual", ctypes.c_ulonglong),
            ("ullAvailExtendedVirtual", ctypes.c_ulonglong)
        ]

    memory = MEMORYSTATUSEX()
    memory.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
    ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(memory))

    return round(memory.ullTotalPhys / (1024 ** 3), 2)

class MyRequestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        device_name = platform.node()
        operating_system = platform.system() + " " + platform.release()
        processor = platform.processor()
        ram = get_ram()

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Laptop Device Specifications</title>
        </head>
        <body>
            <h1>My Laptop Device Specifications</h1>

            <p><b>Name:</b> Madhuvadhani S</p>
            <p><b>Register Number:</b> 26012082</p>
            <p><b>Device Name:</b> {device_name}</p>
            <p><b>Operating System:</b> {operating_system}</p>
            <p><b>Processor:</b> {processor}</p>
            <p><b>RAM:</b> {ram} GB</p>
        </body>
        </html>
        """

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(html.encode())

with socketserver.TCPServer(("", PORT), MyRequestHandler) as httpd:
    print(f"Server running at http://127.0.0.1:{PORT}")
    httpd.serve_forever()