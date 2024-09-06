from flask import jsonify, request
from app.api.v1 import bp
from app.services.dns_service import DNSService
from app.models.dns_entry import DNSEntry

@bp.route('/dns', methods=['POST'])
def add_dns_entry():
    data = request.json
    if not data or 'domain' not in data:
        return jsonify({'error': 'Invalid input'}), 400

    # You can add more validation here if needed
    domain = data['domain']
    result = DNSService.add_entry(domain)
    return jsonify(result.to_dict()), 201

@bp.route('/dns', methods=['GET'])
def get_all_dns_entries():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    entries = DNSService.get_all_entries(page, per_page)
    return jsonify([entry.to_dict() for entry in entries.items]), 200

@bp.route('/dns/<string:domain>', methods=['GET'])
def get_dns_entry(domain):
    entry = DNSService.get_entry(domain)
    if entry is None:
        return jsonify({'error': 'Domain not found'}), 404
    return jsonify(entry.to_dict()), 200

@bp.route('/', methods=['GET'])
def hello():
    return jsonify({"message": "hello"}), 200
