import os
from flask import Flask, request, redirect, flash, jsonify
from werkzeug.utils import secure_filename
import argparse
import glob

import uuid


import gevent as g
from gevent.queue import Queue
from gevent.wsgi import WSGIServer
from gevent import monkey; monkey.patch_all()
from colors.segment import segment
from style_type.decide import check_on_best
from matplotlib import pyplot as plt
import pickle

UPLOAD_FOLDER = '/home/ubuntu/model/'
RESULTS_FOLDER = '/home/ubuntu/results/'

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
job_queue = Queue()


@app.route('/', methods=['POST', 'GET'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            filename = str(uuid.uuid4()) + secure_filename(file.filename)
            saved_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(saved_file_path)
            job_queue.put(filename)
            return jsonify({"success": True})
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''


@app.route('/season', methods=['GET'])
def check_season():
    list_of_files = glob.glob(RESULTS_FOLDER + '*')  # * means all if need specific format then *.csv
    latest_file = max(list_of_files, key=os.path.getctime)
    if request.method == 'GET':
        img = plt.imread(latest_file).astype("uint8")
        img = img[:, :, :3]
        print(img)
        answer = check_on_best(img, request.json["season"], miss_color=(0, 0, 0))
        return jsonify({"seems good": answer})


def background_worker():
    for filename in job_queue:
        result = segment(filename)
        plt.imsave(os.path.join(RESULTS_FOLDER, filename), result)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, help="port to listen", required=True)
    parser.add_argument("--address", type=str, default='', help="address to listen")
    args = parser.parse_args()
    http_server = WSGIServer((args.address, args.port), app)
    g.spawn(background_worker)
    http_server.serve_forever()
    app.debug = True
    app.run()
