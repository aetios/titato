#!/usr/bin/env python3

from subprocess import run
import json
import requests
import sys

s = 'http://127.0.0.1:45222'

raw_tasks = requests.get(f'{s}/taskslist')

tasks_array=json.loads(raw_tasks.text)

options=''
for i in tasks_array:
   options=options + f'{i}\n'

out = run(['dmenu','-p','Switch to task'], input=options.encode(), capture_output=True)

new_task=out.stdout.decode().strip()

try:
   task_id=tasks_array.index(new_task)
except ValueError:
   sys.exit()


requests.post(f'{s}/switchtask', data={'id':task_id})
