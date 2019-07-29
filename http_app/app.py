from initialize import InitConfig, InitLogger, InitAdapter
from organizations import Organizations
from flask import Flask, request, jsonify
from .controller import Controller
from .exceptions import HttpException

flask_app = Flask(__name__)

app = {}

config = InitConfig(app)
app['config'] = config

logger = InitLogger(app)
app['logger'] = logger

adapter = InitAdapter(app)
app['organizations_adapter'] = adapter

organizations = Organizations(app)
app['organizations'] = organizations

ctrl = Controller(app)


def success_response(payload={}, meta={}, http_code=200):
    return jsonify({
        'success': True,
        'payload': payload,
        'meta': meta
    }), http_code


@flask_app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        start = request.args.get('start')
        payload, meta = ctrl.list_organizations(start)
        return success_response(payload=payload, meta=meta)
    else:
        inputs = request.json
        payload = ctrl.create_organizations(inputs)
        return success_response(payload=payload, http_code=201)


@flask_app.route('/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def update(id):
    if request.method == 'GET':
        payload = ctrl.get_organizations(id)
        return success_response(payload=payload)
    elif request.method == 'PUT':
        inputs = request.json
        payload = ctrl.update_organizations(id, inputs)
        return success_response(payload=payload)
    else:
        ctrl.delete_organizations(id)
        return success_response()


@flask_app.route('/search', methods=['GET'])
def search():
    if request.method == 'GET':
        query = request.args.get('query')
        start = request.args.get('start', None)
        user_lat = request.args.get('user_lat', None)
        user_lng = request.args.get('user_lng', None)
        payload, meta = ctrl.search_organizations(query,
                                                  user_lat=user_lat,
                                                  user_lng=user_lng,
                                                  start=start)
        return success_response(payload=payload, meta=meta)


@flask_app.errorhandler(HttpException)
def handle_http_exceptions(error):
    app['logger'].error(error, exc_info=True)
    response = {
        'success': False,
        'message': error.message
    }
    return jsonify(response), error.http_code


@flask_app.errorhandler(Exception)
def handle_exceptions(error):
    app['logger'].error(error, exc_info=True)
    response = {
        'success': False,
        'message': 'Unexpected error occurred'
    }
    return jsonify(response), 500
