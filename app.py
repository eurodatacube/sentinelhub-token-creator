import logging

from flask import Flask, jsonify, request
from prometheus_flask_exporter import PrometheusMetrics
from werkzeug.exceptions import BadRequest

import oauthlib
import requests_oauthlib

app = Flask(__name__)
metrics = PrometheusMetrics(app)

logger = logging.getLogger(__name__)

TOKEN_URL = "https://services.sentinel-hub.com/oauth/token"

if __name__ != "__main__":
    gunicorn_logger = logging.getLogger("gunicorn.error")
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)


@app.route("/headers")
def headers():
    return jsonify(dict(request.headers))


SH_CLIENT_ID_HEADER = "X-SH-CLIENT-ID"
SH_CLIENT_SECRET_HEADER = "X-SH-CLIENT-SECRET"


@app.route("/token")
def retrieve_token():
    logger.info("Retrieving token")
    try:
        sh_client_id = request.headers[SH_CLIENT_ID_HEADER]
        sh_client_secret = request.headers[SH_CLIENT_SECRET_HEADER]
    except KeyError:
        raise BadRequest(
            f"Please specify the headers {SH_CLIENT_ID_HEADER} and "
            f"{SH_CLIENT_SECRET_HEADER}"
        )

    client = oauthlib.oauth2.BackendApplicationClient(client_id=sh_client_id)
    session = requests_oauthlib.OAuth2Session(client=client)

    token = session.fetch_token(
        token_url=TOKEN_URL, client_id=sh_client_id, client_secret=sh_client_secret
    )
    logger.info("Token successfully retrieved")
    return token
