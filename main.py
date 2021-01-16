from flask import Flask, render_template, request, make_response, send_from_directory

app = Flask(__name__)

@app.route('/')
def index(name=None):
    return render_template('index.html', name=name)

app.run()
