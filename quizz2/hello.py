from flask import Flask
from flask import request, url_for
index_add_counter = 1
my_dict = {}
from flask import jsonify
import requests
import json
from flask import Response

class HTTPMethodOverrideMiddleware(object):
    allowed_methods = frozenset([
        'GET',
        'HEAD',
        'POST',
        'DELETE',
        'PUT',
        'PATCH',
        'OPTIONS'
    ])
    bodyless_methods = frozenset(['GET', 'HEAD', 'OPTIONS', 'DELETE'])

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        method = environ.get('HTTP_X_HTTP_METHOD_OVERRIDE', '').upper()
        if method in self.allowed_methods:
            method = method.encode('ascii', 'replace')
            environ['REQUEST_METHOD'] = method
        if method in self.bodyless_methods:
            environ['CONTENT_LENGTH'] = '0'
        return self.app(environ, start_response)


app = Flask(__name__)
app.wsgi_app = HTTPMethodOverrideMiddleware(app.wsgi_app)

@app.route("/")
def hello():
    return "Hello World"

@app.route('/users', methods=['POST'])
def new_users():
    global index_add_counter
    global my_dict
    key = index_add_counter
    if request.method == 'POST':
        name = request.form["name"]
        my_dict[index_add_counter] = name
        for item in my_dict:
            data = {'id': item,'name':my_dict[item]}
        index_add_counter = index_add_counter + 1  
        js = json.dumps(data)
        r = Response(js, status=201, mimetype="application/json")
        r.headers["Content-Type"] = "text/json; charset=utf-8"
        return r

@app.route('/users/<id>', methods=["GET"])
def get_user(id):
    global my_dict
    json_data = my_dict
    id1 = id
    data = {}
    if request.method == 'GET':
        for item in json_data:
            if int(id1) == item:
                data = {'id': item,'name':my_dict[item]}
    else :
        del my_dict[int(id)]
    return jsonify(data)

@app.route('/users/<id>', methods=["DELETE"])
def delete_user(id):
    global my_dict
    json_data = my_dict
    data = {}
    del my_dict[int(id)]
    return Response(status=204)
