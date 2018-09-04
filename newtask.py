#!/usr/bin/env python3

from subprocess import run
import requests

s="http://127.0.0.1:45222"

out = run(['dmenu', '-p', 'New task name', '-lines', '0'], capture_output=True)

requests.post(f'{s}/newtask', data={'taskname':f'{out.stdout.decode().strip()}'})
