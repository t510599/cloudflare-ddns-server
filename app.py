import socket
import logging
import hashlib
import configparser
from functools import wraps

from flask import Flask, request
from werkzeug.exceptions import HTTPException

from cloudflare import CloudflareAPI

app = Flask(__name__)
app.logger.setLevel(logging.INFO)

config = configparser.ConfigParser()
config.read("ddns.ini")

api = CloudflareAPI(config["cloudflare"]["token"], config["cloudflare"]["zone"])


def authorize(username, password):
    return password == hashlib.sha1((username + config["app"]["secret"]).encode()).hexdigest()


def basic_auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not authorize(auth.username, auth.password):
            return "badauth", 401
        return f(*args, **kwargs)
    return decorated


@app.route("/nic/update")
@basic_auth_required
def update():
    hostname = request.args.get("hostname")
    ip = request.args.get("myip")
    if not hostname or not ip:
        return "nohost", 400

    if socket.gethostbyname(hostname) == ip:
        app.logger.info(f"No update for domain = {hostname}")
        return f"nochg {ip}", 200
    else:
        if api.update_result(hostname, ip):
            app.logger.info(f"Update done for domain = {hostname}, ip = {ip}")
            return f"good {ip}", 200
        else:
            app.logger.error(f"Update failed for domain = {hostname}")
            return "nohost", 400


@app.errorhandler(Exception)
def handle_exception(e):
    # pass through HTTP errors
    if isinstance(e, HTTPException):
        return e

    # handling non-HTTP exceptions only
    app.log_exception(e)

    return "911", 500


if __name__ == "__main__":
    app.run("0.0.0.0", 5000)
