from flask import jsonify, request
from app.api.v1 import bp
from app.services.dns_service import DNSService
from app.schemas.dns_schema import dns_entry_schema, dns_entries_schema
from marshmallow import ValidationError

@bp.route('/dns', methods=['POST'])
def add_dns_entry():
    try:
        data = dns_entry_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    result = DNSService.add_entry(data['domain'])
    return dns_entry_schema.jsonify(result), 201

@bp.route('/dns', methods=['GET'])
def get_all_dns_entries():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    entries = DNSService.get_all_entries(page, per_page)
    return dns_entries_schema.jsonify(entries), 200

@bp.route('/dns/<string:domain>', methods=['GET'])
def get_dns_entry(domain):
    entry = DNSService.get_entry(domain)
    if entry is None:
        return jsonify({'error': 'Domain not found'}), 404
    return dns_entry_schema.jsonify(entry), 200
