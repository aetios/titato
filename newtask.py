#!/usr/bin/env python3

from subprocess import run
import requests
import os


s="http://127.0.0.1:45222"

out = run(['dmenu', '-p', 'New log entry', '-lines', '0'], capture_output=True)

log_text = out.stdout.decode().strip()

if log_text != "":
    requests.post(f'{s}/switchtask', data={'log-entry':f'{out.stdout.decode().strip()}'})
    os.remove('/tmp/timepassed')

