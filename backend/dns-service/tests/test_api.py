def test_add_dns_entry(client):
    response = client.post('/api/v1/dns', json={'domain': 'example.com'})
    assert response.status_code == 201
    assert 'example.com' in response.json['domain']

def test_get_all_dns_entries(client):
    client.post('/api/v1/dns', json={'domain': 'example.com'})
    response = client.get('/api/v1/dns')
    assert response.status_code == 200
    assert len(response.json) > 0

def test_get_dns_entry(client):
    client.post('/api/v1/dns', json={'domain': 'example.com'})
    response = client.get('/api/v1/dns/example.com')
    assert response.status_code == 200
    assert response.json['domain'] == 'example.com'
