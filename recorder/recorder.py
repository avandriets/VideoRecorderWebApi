from flask import Flask, request, jsonify, redirect, render_template
from flask_cors import CORS

from recorder.database import db
from recorder.error_helper import InvalidUsage
from flask_wtf.csrf import CSRFProtect
from recorder.json_encoder import CustomDecimalJSONEncoder

app = Flask(__name__)
app.config.from_object('config')


db.init_app(app)

app.json_encoder = CustomDecimalJSONEncoder

CORS(app)
csrf = CSRFProtect(app)

from recorder.api.records.views import blueprint_records

app.register_blueprint(blueprint_records, url_prefix='/media/api/records')

# disable csrf protection for api urls
csrf.exempt(blueprint_records)


@app.cli.command('initdb')
def initdb_command():
    """Creates the database tables."""
    from recorder.database import init_db
    init_db()
    print('Initialized the database.')


@app.context_processor
def site_name():
    """
    inject site name in context
    :return:
    """
    return {'site_name': app.config['SITE_NAME']}


from flask_wtf.csrf import CSRFError


@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    if '/api/' in request.path:
        response = jsonify({
            'status': 400,
            'sub_code': 1,
            'message': "csrf protection error"
        })
        return response, 400

    return render_template('error/csrf_error.html', reason=e.description), 400


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.errorhandler(404)
def not_found(error):
    """
    Simple 404 page
    :param error:
    :return:
    """
    if '/api/' in request.path:
        response = jsonify({
            'status': 404,
            'sub_code': 1,
            'message': "not found."
        })
        return response, 404

    return render_template('error/404.html'), 404


@app.errorhandler(403)
def not_found(error):
    """
    Simple 403 page
    :param error:
    :return:
    """
    if '/api/' in request.path:
        response = jsonify({
            'status': 403,
            'sub_code': 1,
            'message': "forbidden"
        })
        return response, 403

    return render_template('error/403.html'), 403


@app.errorhandler(401)
def not_found(error):
    """
    Simple 401 page
    :param error:
    :return:
    """
    if '/api/' in request.path:
        response = jsonify({
            'status': 401,
            'sub_code': 1,
            'message': "Client not authenticated."
        })
        return response, 401

    return render_template('error/401.html'), 401


@app.errorhandler(405)
def not_found(error):
    """
    Simple 401 page
    :param error:
    :return:
    """
    if '/api/' in request.path:
        response = jsonify({
            'status': 405,
            'sub_code': 1,
            'message': "Method nod allowed."
        })
        return response, 405

    return render_template('error/405.html'), 405


@app.teardown_appcontext
def shutdown_session(exception=None):
    from recorder.database import db
    db.session.remove()
