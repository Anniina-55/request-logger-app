from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS

from request_logging_mw import init_request_logging
from routes.logs_bp import logs_bp
from routes.analytics import analytics_bp

app = Flask(__name__, static_folder="frontend")

CORS(app)

# middleware
init_request_logging(app)

# blueprints
app.register_blueprint(logs_bp)
app.register_blueprint(analytics_bp)

# health check endpoint
@app.route("/health")
def health():
    return jsonify({
        "service": "logging-api",
        "status": "running",
        "health_status": "ok"
    })

# serve frontend
@app.route("/")
def index():
    return send_from_directory("frontend", "index.html")

# serve static files
@app.route("/<path:path>")
def serve_static(path):
    return send_from_directory("frontend", path)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)