# /usr/bin/env python3

from tinydb import TinyDB, Query, where
from flask import Flask, request, jsonify
from time import strftime
from datetime import datetime, timedelta

core = Flask(__name__)


db = TinyDB("tasks.json")

@core.route("/switchtask", methods=["POST"])
def switchtask():
    #POST body should contain the task text
    ds = strftime("%G%m%d")
    old_tasks = db.search(where("date") == ds)
    lot = len(old_tasks)

    new_data = (request.form["log-entry"], strftime("%H%M%S"))
    if lot is 0:
        new_tasks = [new_data]
        db.insert({"date": ds, "tasks": new_tasks})
    else:
        ot = old_tasks[0]["tasks"]
        if ot is not None:
            ot.append(new_data)
        else:
            ot = [new_data]
        db.update({"tasks": ot}, where("date") == ds)

    return "OK"


@core.route("/get/<days>", methods=["GET"])  # this returns a formatted plaintext with the tasks of the past few <<days>>
def getlist(days):
    result = [] # result is a list of days with their tasks
    for i in range(int(days)):
        target_date = (datetime.now() - timedelta(days=i)).strftime("%G%m%d") #this is the date we will query the database for
        query_result = db.search(where("date") == target_date)
        if len(query_result) != 0:
            entry = query_result[0]

            result.append(entry)
    response = ""

    for day in result[::-1]:
        date_stamp = day["date"]
        response += f"{date_stamp[:4]}-{date_stamp[4:6]}-{date_stamp[6:]}{'.'*20}\n"

        days_tasks = day["tasks"] #a list of this day's tasks, with their timestamps
        for task in days_tasks:
            time_stamp = task[1]
            response += f"\t{time_stamp[:2]}:{time_stamp[2:4]}:{time_stamp[4:]}   |  {task[0]}\n"

    return response
