from flask import Blueprint, request, jsonify
import requests
import time
import uuid
import logging
from app.utils.logging_utils import log_request_info, log_response_info
from app.services.service_registry import services
from app.utils.rate_limiting import limiter
from functools import wraps 

logger = logging.getLogger(__name__)

api_bp = Blueprint('api', __name__)

def dynamic_limit(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        service = kwargs.get('service')

        if service == 'high_priority':
            limit = "100 per minute"
        elif service == 'low_priority':
            limit = "50 per minute"
        else:
            limit = "100 per minute"
        
        combined_limit = f"1000 per hour;{limit};5 per second"
        return limiter.limit(combined_limit)(f)(*args, **kwargs)
    return decorated_function

@api_bp.route('/<service>/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
@dynamic_limit
def gateway(service, path):
    request_id = str(uuid.uuid4())
    start_time = time.time()
    log_request_info(request_id, service, path)

    if service not in services:
        logger.warning(f"Request: {request_id} | Service not found: {service}")
        return jsonify({'error': 'Service not found'}), 404

    url = f"{services[service]['url']}/{service}/{path}"
    logger.warning(f"Request: {request_id} | Forwarding request to: {url}")
    try:
        response = requests.request(
            method=request.method,
            url=url,
            headers={key: value for (key, value) in request.headers if key != 'Host'},
            data=request.get_data(),
            cookies=request.cookies,
            allow_redirects=False
        )
        
        end_time = time.time()
        response_time = end_time - start_time
        
        log_response_info(request_id, service, response.status_code, response_time)
        
        return (response.content, response.status_code, response.headers.items())
    except requests.RequestException as e:
        logger.error(f"Request: {request_id} | Service unavailable: {service}. Error: {str(e)}")
        return jsonify({'error': 'Service unavailable'}), 503

@api_bp.errorhandler(429)
def ratelimit_handler(e):
    service = request.view_args.get('service', 'unknown')
    logger.warning(f"Rate limit hit for service: {service}")
    return jsonify({
        'error': 'Rate limit exceeded',
        'retry_after': e.description
    }), 429
