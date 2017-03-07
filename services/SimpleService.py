import os

from flask import Flask, request

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = '/srv/salt/'


@app.route('/upload', methods=['POST'])
def upload():
    upload_file = request.files['file']
    filename = upload_file.filename
    upload_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return ''


@app.route('/read', methods=['POST'])
def read():
    filename = request.form['name']
    contents = open(filename,'rb').read()
    return contents


@app.route('/rouster', methods=['POST'])
def rouster():
    content = request.form['content']
    with open('/etc/salt/roster') as file:
        file.write(content)
    return ''


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
