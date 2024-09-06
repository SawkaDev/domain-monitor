from app.services.dns_service import DNSService

def test_add_entry(app):
    with app.app_context():
        entry = DNSService.add_entry('example.com')
        assert entry.domain == 'example.com'
        assert 'A' in entry.records

def test_get_entry(app):
    with app.app_context():
        DNSService.add_entry('example.com')
        entry = DNSService.get_entry('example.com')
        assert entry is not None
        assert entry.domain == 'example.com'
