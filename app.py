import os

# from utils import PdfGenerator
import big_commerce

import flask

app = flask.Flask(__name__)
username = 'username'
password = 'password'
session_hash = 'g34th239hs934'

def is_logged_in():
    return flask.request.cookies.get('session') == session_hash

@app.route('/')
def index():
    resp = flask.make_response(flask.render_template('index.html'))
    if is_logged_in():
        resp.set_cookie('session', '')
    return resp

@app.route('/login', methods=['POST'])
def login():
    args = flask.request.get_json()
    if args['username'] == username and args['password'] == password:
        resp = flask.make_response()
        resp.set_cookie('session', session_hash)
        return resp
    else:
        return 'failure'

@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if not is_logged_in():
        return flask.redirect('/')

    if flask.request.method == 'POST':
        if len(flask.request.files) == 0:
            return flask.redirect('/upload')

        file = flask.request.files.values()[0]
        name = flask.request.files.keys()[0]
        file.save('files/' + name + '.csv')
        return flask.redirect('/upload?text=File uploaded')

    else:
        return flask.render_template('upload.html', text=flask.request.args.get('text') or '')

@app.route('/download_config/<path:filename>', methods=['GET'])
def download_config(filename):
    if not is_logged_in():
        return

    return flask.send_from_directory(
        directory='files',
        filename=filename+'.csv',
        as_attachment=True
    )

@app.route('/favicon.ico')
def favicon():
    return flask.send_from_directory(os.path.join(app.root_path, 'static', 'images'),
                               'favicon.ico', mimetype='image/png')

@app.route('/process_orders', methods=['POST'])
def process_orders():
    if not is_logged_in():
        return 'not logged in'
        
    # orders = big_commerce.Parser().get_orders_from_csv_file(None)
    # PDFGenerator = PdfGenerator()
    # directory = PDFGenerator.create_directory(username)
    # if not directory:
    #     return flask.abort(400)
    # PDFs = [PDFGenerator.create_file(order.id, directory) for order in orders]  
    # PDFGenerator.compress_directory(directory)
    # compressed_file = "{directory}.zip".format(directory=directory)
    # response = flask.send_file(compressed_file, attachment_filename=compressed_file, as_attachment=True)
    # PDFGenerator.remove_file(compressed_file)
    return ''

if __name__ == '__main__':
    app.run(debug=True)