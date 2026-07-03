from flask import Flask, request, jsonify, g, send_from_directory
from flask import Response
import logging
import time
import uuid
import socket
import json
from flask_cors import CORS

app = Flask(__name__, static_folder="frontend")

CORS(app)

logging.basicConfig(
    level=logging.INFO
)

logs = []

@app.before_request
def before_request():
    g.start_time = time.time()
    g.request_id = str(uuid.uuid4())


@app.after_request
def after_request(response):
    # Calculate duration of request in milliseconds
    duration = round((time.time() - g.start_time) * 1000, 2)

    log = {
        # Request identification
        "request_id": g.request_id,
        # Timestamp in ISO 8601 format
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),

        # Request
        "method": request.method,
        "path": request.path,
        "full_path": request.full_path,
        "url": request.url,
        "base_url": request.base_url,

        # Client
        "remote_addr": request.remote_addr,
        "remote_port": request.environ.get("REMOTE_PORT"),
        "user_agent": request.user_agent.string,
        "host": request.host,
        "scheme": request.scheme,

        # Proxy (if used)
        "forwarded_for": request.headers.get("X-Forwarded-For"),
        "forwarded_host": request.headers.get("X-Forwarded-Host"),
        "forwarded_proto": request.headers.get("X-Forwarded-Proto"),

        # Request metadata
        "content_type": request.content_type,
        "content_length": request.content_length,

        # Response
        "status": response.status_code,
        "response_size": response.calculate_content_length() or 0,
        "duration_ms": duration,

        # Server
        "server_hostname": socket.gethostname(),

        # All request headers
        "headers": dict(request.headers)
    }
    logs.append(log)
    #logging.info(json.dumps(log), default=str)

    return response


@app.route("/health")
def health():
    return jsonify({
        "service": "logging-api",
        "status": "running",
        "health_status": "ok"
    })

@app.route("/")
def index():
    return send_from_directory("frontend", "index.html")

@app.route("/api/logs")
def get_logs():
    return jsonify(logs[-200:])


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )