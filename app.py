from flask import Flask, render_template, jsonify
from pdf_rename import start_observer
import threading
import time

app = Flask(__name__)
observer = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start')
def start():
    global observer
    if observer is None:
        folder_to_watch = '/Users/subhadipdas/Desktop'
        observer = start_observer(folder_to_watch)
        return jsonify(success=True, message="Monitoring started.")
    else:
        return jsonify(success=False, message="Already monitoring.")

@app.route('/stop')
def stop():
    global observer
    if observer is not None:
        observer.stop()
        observer.join()
        observer = None
        return jsonify(success=True, message="Monitoring stopped.")
    else:
        return jsonify(success=False, message="Not monitoring.")

if __name__ == "__main__":
    app.run(debug=True)
