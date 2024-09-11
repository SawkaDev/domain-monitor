from flask import jsonify, request
from app.api.v1 import bp
from app.services.dns_service import DNSService

@bp.route('/<string:domain>', methods=['GET'])
def get_dns_records(domain):
    records = DNSService.get_current_dns_records(domain)
    if records:
        return jsonify([record.to_dict() for record in records]), 200
    else:
        return jsonify([]), 200

@bp.route('/history/<string:domain>', methods=['GET'])
def get_dns_history(domain):
    history = DNSService.get_dns_history(domain)
    if history:
        return jsonify([entry.to_dict() for entry in history]), 200
    else:
        return jsonify([]), 200


# TODO: helper route for now instead of using the scheduler
@bp.route('/<domain_name>', methods=['POST'])
def update_dns_records(domain_name):
    history = DNSService.update_dns_records(domain_name)
    return jsonify({"status": history}), history and 200 or 500

@bp.route('/heartbeat', methods=['GET'])
def heartbeat():
    return jsonify({'status': 'ok'}), 200

@bp.route('/changes/<string:domain>', methods=['GET'])
def get_dns_changes(domain):
    changes = DNSService.get_dns_changes(domain)
    if changes:
        return jsonify(changes.to_dict()), 200
    else:
        return jsonify({"error": "Domain not found"}), 404