from flask import Flask
from werkzeug.middleware.profiler import ProfilerMiddleware
import logging


def create_app():
    app = Flask(__name__)
    # Configure Flask app logging
    app.logger.setLevel(logging.INFO)  # Set the desired log level
    app.logger.addHandler(logging.StreamHandler())  # Output logs to console

    # Optionally, configure Werkzeug logging (for development server)
    log = logging.getLogger("werkzeug")
    log.setLevel(logging.INFO)
    log.addHandler(logging.StreamHandler())
    # app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[30])
    # Configurations
    app.config.from_pyfile("config.py")

    # Register blueprints
    from app.routes import main

    app.register_blueprint(main)

    return app
