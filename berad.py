#!/usr/bin/env python3
"""
Berad Tech — Управление производством
Запуск: python berad.py
Данные сохраняются в файл data.json в этой же папке.
"""
import http.server
import socketserver
import webbrowser
import json
import os
import sys
from urllib.parse import urlparse, parse_qs

PORT = 8765
DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(DIR, 'data.json')

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIR, **kwargs)

    def do_GET(self):
        if self.path == '/api/data':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            if os.path.exists(DATA_FILE):
                with open(DATA_FILE, 'r', encoding='utf-8') as f:
                    self.wfile.write(f.read().encode('utf-8'))
            else:
                self.wfile.write(b'{}')
            return
        return super().do_GET()

    def do_POST(self):
        if self.path == '/api/data':
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length)
            try:
                data = json.loads(body.decode('utf-8'))
                with open(DATA_FILE, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(b'{"ok":true}')
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(str(e).encode())
            return
        self.send_response(404)
        self.end_headers()

    def log_message(self, format, *args):
        pass

if __name__ == '__main__':
    os.chdir(DIR)
    with socketserver.TCPServer(('', PORT), Handler) as httpd:
        url = f'http://localhost:{PORT}/index.html'
        print(f'Berad Tech запущен: {url}')
        print(f'Данные сохраняются в: {DATA_FILE}')
        print('Закройте это окно для остановки.')
        webbrowser.open(url)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print('\nОстановлено.')
