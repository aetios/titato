#/usr/bin/env python3

from tinydb import TinyDB, Query, where
from flask import Flask, request, jsonify
from time import strftime
from datetime import datetime, timedelta

core = Flask(__name__)


db = TinyDB('tasks.json')


class Task:
    def __init__(self, task_id, starttime):
        self.starttime=starttime
        self.task_id=task_id

with open('tlist') as f:
    tasks=f.readlines()
    tasks=[x.strip() for x in tasks if x.strip() != ""]






@core.route('/newtask', methods=['POST'])
def newtask():
    # POST body should contain the new task name
    tn = request.form['taskname']
    print(tn)
    tn=tn.strip()
    if tn not in tasks and tn != "":
        tasks.append(tn)
        with open('tlist', 'a') as f:
           f.write(f'\n{tn}')
    #permanentize tasks?
    return 'OK'


@core.route('/switchtask', methods=['POST'])
def switchtask():
    #POST body should contain the task id
    ds = strftime('%G%m%d')
    old_tasks = db.search(where('date') == ds)
    lot = len(old_tasks)

    new_data = (request.form['id'], strftime('%H%M%S'))
    if lot is 0:
        new_tasks = [new_data]
        db.insert({'date': ds, 'tasks':new_tasks})
    else:
        ot = old_tasks[0]['tasks']
        if ot is not None:
            ot.append(new_data)
        else:
            ot = [new_data]
        db.update({'tasks': ot}, where('date')== ds)
    
    #print(db.all())
    return 'OK'
   

@core.route('/taskslist')
def taskslist():
    return jsonify(tasks)


@core.route('/get/<days>', methods=['GET']) #this returns a JSON with the tasks between today and the last <<days>>
def getlist(days):
    result=[]
    for i in range(int(days)):
        ds = (datetime.now()-timedelta(days=i)).strftime('%G%m%d')
        query_result = db.search(where('date') == ds)
        if len(query_result) != 0:
            entry = query_result[0]
            
            result.append(entry)
    response=""

    for d in result[::-1]:
        ds=d['date']
        response+=f"{ds[:4]}-{ds[4:6]}-{ds[6:]}{'.'*20}\n"
        
        tl = d['tasks']
        for t in tl:
            ts=t[1]
            response+=f"\t{ts[:2]}:{ts[2:4]}:{ts[4:]}   |  {tasks[int(t[0])]}\n"

    
    return response
