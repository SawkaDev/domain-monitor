from flask import jsonify, request
from app.api.v1 import bp
from app.services.dns_service import DNSService

@bp.route('/dns/<string:domain_name>', methods=['GET'])
def get_dns_records(domain_name):
    records = DNSService.get_current_dns_records(domain_name)
    if records:
        return jsonify([record.to_dict() for record in records]), 200
    else:
        return jsonify({"error": "No DNS records found for this domain"}), 404

@bp.route('/dns/<domain_name>', methods=['POST'])
def process_dns_records(domain_name):
    # Check if the domain already has records
    existing_records = DNSService.get_current_dns_records(domain_name)
    
    if not existing_records:
        # First time, create initial records
        success = DNSService.create_initial_dns_records(domain_name)
        message = "created" if success else "failed to create"
    else:
        # Update existing records
        success = DNSService.update_dns_records(domain_name)
        message = "updated" if success else "failed to update"
    
    if success:
        return jsonify({"message": f"DNS records for {domain_name} {message} successfully"}), 200
    else:
        return jsonify({"error": f"Failed to process DNS records for {domain_name}"}), 500

@bp.route('/dns/history/<domain_name>', methods=['GET'])
def get_dns_history(domain_name):
    history = DNSService.get_dns_history(domain_name)
    if history:
        return jsonify([entry.to_dict() for entry in history]), 200
    else:
        return jsonify({"error": "No DNS history found for this domain"}), 404

@bp.route('/dns/heartbeat', methods=['GET'])
def heartbeat():
    return jsonify({'status': 'ok'}), 200
