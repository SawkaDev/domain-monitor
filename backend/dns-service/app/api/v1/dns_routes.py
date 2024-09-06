from flask import jsonify, request
from app.api.v1 import bp
from app.services.dns_service import DNSService

@bp.route('/dns/<string:domain_name>', methods=['GET'])
def get_dns_records(domain_name):
    records = DNSService.get_latest_dns_records(domain_name)
    if records is not None:
        return jsonify(records), 200
    else:
        return jsonify({"error": "Domain not found"}), 404

@bp.route('/dns/<string:domain_name>', methods=['POST'])
def update_dns_records(domain_name):
    if DNSService.update_dns_records(domain_name):
        return jsonify({"message": "DNS records updated successfully"}), 200
    else:
        return jsonify({"error": "Failed to update DNS records"}), 400

@bp.route('/dns/heartbeat', methods=['GET'])
def heartbeat():
    return jsonify({'status': 'ok'}), 200
