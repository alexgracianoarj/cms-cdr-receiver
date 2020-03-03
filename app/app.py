import os
from dotenv import load_dotenv
from pathlib import Path
from flask import Flask, request, Response
from pymongo import MongoClient
import xmltodict
from bson.json_util import dumps
from datetime import datetime
from waitress import serve
from paste.translogger import TransLogger

app = Flask(__name__)
app.url_map.strict_slashes = False

if os.getenv("PY_ENV")=="prod":
    load_dotenv(dotenv_path=Path('.')/'prod.env')
else:
    load_dotenv(dotenv_path=Path('.')/'dev.env')

conn = MongoClient(os.getenv("MONGO_URI"))
db = conn.cms

@app.route('/api/saveCdr', methods=['POST'])
def save_cdr():
    cdr = xmltodict.parse(request.data)
    cdr["createdAt"] = datetime.utcnow()
    db.cdrs.insert_one(cdr)
    return Response(dumps({'response':'OK'}), status=201, mimetype='application/json')

@app.route('/api/getCdrsBetweenDates/<dateStart>/<dateEnd>', methods=['GET']) 
def get_cdrs_between_dates(dateStart, dateEnd):
    start = datetime.strptime(dateStart, '%Y-%m-%d')
    end = datetime.strptime(dateEnd, '%Y-%m-%d')
    result = db.cdrs.find({'createdAt': {'$gte': start, '$lt': end}})
    return Response(dumps({'response':result}), status=200, mimetype='application/json')

if __name__ == "__main__":
    if os.getenv("PY_ENV")=="prod":
        serve(TransLogger(app, setup_console_handler=False), port=3000, threads=1000)
    else:
        app.run(port=3000, threaded=True, debug=True)
