"""REST API for stock-predictor."""
import flask
import predictor

@predictor.app.route('/api/v1/', methods=['GET'])
def get_services():
    """Return services provided by api."""
    # flask.session.clear()
    if 'logged_in' in flask.session:
        if flask.request.method == 'GET':
            context = {
                "posts": "/api/v1/p/",
                "url": flask.request.path,
            }
            return flask.jsonify(**context)