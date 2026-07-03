from flask import request, g
import time
import uuid
import socket
from utils.log_store import logs


def init_request_logging(app):

    @app.before_request
    def before_request():
        g.start_time = time.time()
        g.request_id = str(uuid.uuid4())

    @app.after_request
    def after_request(response):

        duration = round((time.time() - g.start_time) * 1000, 2)

        logs.append({
            "request_id": g.request_id,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),

            "method": request.method,
            "path": request.path,
            "full_path": request.full_path,
            "url": request.url,
            "base_url": request.base_url,

            "remote_addr": request.remote_addr,
            "remote_port": request.environ.get("REMOTE_PORT"),
            "user_agent": request.user_agent.string,
            "host": request.host,
            "scheme": request.scheme,

            "forwarded_for": request.headers.get("X-Forwarded-For"),
            "forwarded_host": request.headers.get("X-Forwarded-Host"),
            "forwarded_proto": request.headers.get("X-Forwarded-Proto"),

            "content_type": request.content_type,
            "content_length": request.content_length,

            "status": response.status_code,
            "response_size": response.calculate_content_length() or 0,
            "duration_ms": duration,

            "server_hostname": socket.gethostname(),
            "headers": dict(request.headers)
        })

        return response