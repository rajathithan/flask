import logging

from flask import current_app, Flask, redirect, url_for


def create_app(config, debug=False, testing=False, config_overrides=None):
    app = Flask(__name__)
    app.config.from_object(config)

    app.debug = debug
    app.testing = testing

    if config_overrides:
        app.config.update(config_overrides)

    # Configure logging
    if not app.testing:
        logging.basicConfig(level=logging.INFO)

    # Setup the data model.
    with app.app_context():
        model = get_model()
        model.init_app(app)

    # Register the orders orders_crud blueprint.
    from .orders_crud import orders_crud
    app.register_blueprint(orders_crud, url_prefix='/orders')

    # Register the orders orders_crud blueprint.
    from .giftcards_crud import giftcards_crud
    app.register_blueprint(giftcards_crud, url_prefix='/giftcards')

    # Add a default root route.
    @app.route("/")
    def index():
        return redirect(url_for('orders_crud.list'))

    # Add an error handler. This is useful for debugging the live application,
    # however, you should disable the output of the exception for production
    # applications.
    @app.errorhandler(500)
    def server_error(e):
        return """
        An internal error occurred: <pre>{}</pre>
        See logs for full stacktrace.
        """.format(e), 500

    return app


def get_model():
    model_backend = current_app.config['DATA_BACKEND']
    if model_backend == 'cloudsql':
        from . import model_cloudsql
        model = model_cloudsql
    else:
        raise ValueError(
            "No appropriate databackend configured. "
            "Please use cloudsql backend")

    return model
