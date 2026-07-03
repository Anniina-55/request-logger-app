from flask import jsonify, Blueprint
from collections import Counter
from utils.log_store import logs

analytics_bp = Blueprint("analytics", __name__)

@analytics_bp.route("/api/analytics")

def analytics():

    total_requests = len(logs)

    if total_requests == 0:
        return jsonify({
            "total_requests": 0,
            "requests_in_memory": 0,
            "average_latency": 0,
            "fastest_request": 0,
            "slowest_request": 0,
            "most_requested_endpoint": None,
            "endpoint_count": 0,
            "method_distribution": {},
            "status_distribution": {},
            "error_rate": 0,
            "peak_hour": None,
            "top_client_ip": None,
            "largest_response": 0,
            "top_user_agent": None
        })

    # Response times
    durations = [
        log.get("duration_ms", 0)
        for log in logs
    ]

    average_latency = round(sum(durations) / total_requests, 2)

    fastest_request = min(durations)
    slowest_request = max(durations)
    
    # Endpoint usage
    endpoint_counter = Counter(
        log["path"]
        for log in logs
    )

    most_requested_endpoint, endpoint_count = endpoint_counter.most_common(1)[0]

    # HTTP methods
    method_distribution = Counter(
        log["method"]
        for log in logs
    )

    # Status codes
    status_distribution = Counter(
        str(log["status"])
        for log in logs
    )

    # Error rate (4xx + 5xx)
    errors = sum(
        1
        for log in logs
        if log["status"] >= 400
    )
    error_rate = round(
        errors / total_requests * 100,
        2
    )

    # Peak hour
    hours = Counter(
        log["timestamp"][11:13]
        for log in logs
    )
    peak_hour = hours.most_common(1)[0][0] + ":00"
    
    # Top client IP
    ip_counter = Counter(
        log["remote_addr"]
        for log in logs
    )
    top_client_ip = ip_counter.most_common(1)[0][0]

    # Largest response
    largest_response = max(
        log.get("response_size", 0)
        for log in logs
    )
    # User agent
    ua_counter = Counter(
        log["user_agent"]
        for log in logs
    )
    top_user_agent = ua_counter.most_common(1)[0][0]

    return jsonify({
        "total_requests": total_requests,
        "requests_in_memory": total_requests,
        "average_latency": average_latency,
        "fastest_request": fastest_request,
        "slowest_request": slowest_request,
        "most_requested_endpoint": most_requested_endpoint,
        "endpoint_count": endpoint_count,
        "method_distribution": dict(method_distribution),
        "status_distribution": dict(status_distribution),
        "error_rate": error_rate,
        "peak_hour": peak_hour,
        "top_client_ip": top_client_ip,
        "largest_response": largest_response,
        "top_user_agent": top_user_agent
    })