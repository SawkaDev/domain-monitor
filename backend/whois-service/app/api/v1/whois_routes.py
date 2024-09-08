from flask import jsonify, request
from app.api.v1 import bp
from app.services.whois_service import WhoisService

@bp.route('/whois/<string:domain>', methods=['GET'])
def get_whois_record(domain):
    record = WhoisService.get_current_whois_record(domain)
    if record:
        return jsonify(record.to_dict()), 200
    else:
        return jsonify({}), 200

@bp.route('/whois/history/<string:domain>', methods=['GET'])
def get_whois_history(domain):
    history = WhoisService.get_whois_history(domain)
    if history:
        return jsonify([entry.to_dict() for entry in history]), 200
    else:
        return jsonify([]), 200

# TODO: Manual Trigger To Update. This will be removed in the future
@bp.route('/whois/<domain_name>', methods=['POST'])
def update_whois_record(domain_name):
    success = WhoisService.update_whois_record(domain_name)
    return jsonify({"status": success}), 200 if success else 500

@bp.route('/whois/heartbeat', methods=['GET'])
def whois_heartbeat():
    return jsonify({'status': 'ok'}), 200

# Additional route for creating initial WHOIS record
@bp.route('/whois/create/<string:domain>', methods=['POST'])
def create_initial_whois_record(domain):
    data = request.json
    domain_id = data.get('domain_id')
    if not domain_id:
        return jsonify({"error": "domain_id is required"}), 400
    
    success = WhoisService.create_initial_whois_record(domain, domain_id)
    return jsonify({"status": success}), 200 if success else 500
