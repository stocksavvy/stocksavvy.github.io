"""REST API for stock-predictor."""
import flask
import predictor

@predictor.app.route('/', methods=['GET'])
def get_index():
    """Return home page of app."""
    return flask.render_template("index.html")