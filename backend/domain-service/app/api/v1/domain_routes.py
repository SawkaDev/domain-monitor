from flask import jsonify, request, current_app
from app.api.v1 import bp
from app.services.domain_service import DomainService
from sqlalchemy.exc import IntegrityError
from app.tasks.rabbitmq_producer import send_message


@bp.route('/domains', methods=['GET'])
def get_all_domains():
    try:
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 20, type=int)
        domains, total = DomainService.get_domains_paginated(page, limit)
        return jsonify({
            'domains': [domain.to_dict() for domain in domains],
            'total': total,
            'page': page,
            'limit': limit
        }), 200
    except Exception as e:
        current_app.logger.error(f"Error retrieving domains: {str(e)}")
        return jsonify({'error': 'An unexpected error occurred'}), 500

@bp.route('/domain/stats/<string:domain_name>', methods=['GET'])
def get_domain_stats(domain_name):
    try:
        stats = DomainService.get_stats(domain_name)
        if stats is None:
            return jsonify({'error': 'Domain not found'}), 404
        return jsonify(stats), 200
    except Exception as e:
        current_app.logger.error(f"Error retrieving domain stats: {str(e)}")
        return jsonify({'error': 'An unexpected error occurred'}), 500

@bp.route('/heartbeat', methods=['GET'])
def heartbeat():
    return jsonify({'status': 'ok'}), 200

@bp.route('/domain/validate', methods=['POST'])
def validate_domain():
    data = request.json
    if not data or 'domain' not in data:
        return jsonify({'error': 'Invalid input'}), 400

    domain_name = data['domain']
    
    try:
        if DomainService.domain_exists(domain_name):
            # Check if DNS and WHOIS records exist
            dns_ready = DomainService.get_dns_changes(domain_name)
            whois_ready = DomainService.get_whois_changes(domain_name)
            return jsonify({'exists': True, 'records_ready': dns_ready and whois_ready}), 200
        
        # If domain doesn't exist, add it
        result = DomainService.add_entry(domain_name)

        send_message({
            'action': 'create_dns_records',
            'domain': domain_name,
            'domain_id': result.id
        })

        return jsonify({'exists': True, 'added': True, 'records_ready': False}), 201
    except IntegrityError:
        return jsonify({'exists': True, 'added': False, 'records_ready': True}), 200
    except Exception as e:
        current_app.logger.error(f"Error validating/adding domain: {str(e)}")
        return jsonify({'error': 'An unexpected error occurred'}), 500