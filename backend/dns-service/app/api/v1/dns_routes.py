from flask import jsonify, request
from app.api.v1 import bp
from app.services.dns_service import DNSService

@bp.route('/dns/<string:domain>', methods=['GET'])
def get_dns_records(domain):
    records = DNSService.get_current_dns_records(domain)
    if records:
        return jsonify([record.to_dict() for record in records]), 200
    else:
        return jsonify({"error": "No DNS records found for this domain"}), 404

@bp.route('/dns/history/<domain_id>', methods=['GET'])
def get_dns_history(domain_id):
    history = DNSService.get_dns_history(domain_id)
    if history:
        return jsonify([entry.to_dict() for entry in history]), 200
    else:
        return jsonify({"error": "No DNS history found for this domain"}), 404


# TODO: helper route for now instead of using the scheduler
@bp.route('/dns/<domain_name>', methods=['POST'])
def update_dns_records(domain_name):
    history = DNSService.update_dns_records(domain_name)
    return jsonify({"status": history}), history and 200 or 500

@bp.route('/dns/heartbeat', methods=['GET'])
def heartbeat():
    return jsonify({'status': 'ok'}), 200
